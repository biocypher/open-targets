"""Console capture and progress display for the parallel graph build."""

from __future__ import annotations

import os
import re
import sys
import threading
from collections import deque
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from shutil import get_terminal_size
from typing import TYPE_CHECKING, Final, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence
    from multiprocessing.pool import Pool
    from multiprocessing.queues import Queue as MPQueue
    from pathlib import Path
    from typing import TextIO

MIN_TERMINAL_WIDTH: Final[int] = 20
# Set to False to use fd-level capture when available.
FORCE_STREAM_CAPTURE: Final[bool] = False
_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
TTask = TypeVar("TTask")


def _can_use_fd_redirect() -> bool:
    """Return whether stdout/stderr have usable file descriptors."""
    try:
        sys.stdout.fileno()
        sys.stderr.fileno()
    except (AttributeError, OSError):
        return False
    return True


def _can_use_fd_capture() -> bool:
    """Return whether stdout/stderr can be redirected at the fd level."""
    if FORCE_STREAM_CAPTURE:
        return False
    return _can_use_fd_redirect()


def _can_use_ansi() -> bool:
    """Return whether ANSI cursor control is safe to emit."""
    if not sys.stdout.isatty():
        return False
    if os.name != "nt":
        return True
    return bool(os.environ.get("WT_SESSION") or os.environ.get("TERM"))


def _forward_output(read_fd: int, log_file: TextIO, name: str, event_queue: MPQueue) -> None:
    """Write captured output to the log and forward complete lines."""
    buffer = ""
    try:
        while True:
            chunk = os.read(read_fd, 8192)
            if not chunk:
                break
            text = chunk.decode(errors="replace")
            log_file.write(text)
            log_file.flush()
            buffer += text
            parts = re.split(r"[\r\n]", buffer)
            buffer = parts.pop()
            for part in parts:
                if part.strip():
                    event_queue.put(("output", name, part.strip(), ""))
        if buffer.strip():
            event_queue.put(("output", name, buffer.strip(), ""))
    finally:
        log_file.flush()


@contextmanager
def _redirect_fd(
    log_path: Path,
    *,
    name: str | None = None,
    event_queue: MPQueue | None = None,
) -> Iterator[None]:
    """Redirect stdout/stderr to a log, optionally forwarding output lines."""
    sys.stdout.flush()
    sys.stderr.flush()
    stdout_target = sys.stdout.fileno()
    stderr_target = sys.stderr.fileno()
    log_file = log_path.open("w", encoding="utf-8")
    stdout_fd = os.dup(stdout_target)
    stderr_fd = os.dup(stderr_target)
    read_fd: int | None = None
    thread: threading.Thread | None = None

    if name is not None and event_queue is not None:
        read_fd, write_fd = os.pipe()
        os.dup2(write_fd, stdout_target)
        os.dup2(write_fd, stderr_target)
        os.close(write_fd)
        thread = threading.Thread(
            target=_forward_output,
            args=(read_fd, log_file, name, event_queue),
            daemon=True,
        )
        thread.start()
    else:
        os.dup2(log_file.fileno(), stdout_target)
        os.dup2(log_file.fileno(), stderr_target)

    try:
        yield
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(stdout_fd, stdout_target)
        os.dup2(stderr_fd, stderr_target)
        os.close(stdout_fd)
        os.close(stderr_fd)
        if thread is not None:
            thread.join()
        if read_fd is not None:
            os.close(read_fd)
        log_file.close()


@contextmanager
def _redirect_output_python_to_file(log_path: Path) -> Iterator[None]:
    """Redirect Python-level stdout/stderr to a log file."""
    with log_path.open("w", encoding="utf-8") as log_file, redirect_stdout(log_file), redirect_stderr(log_file):
        yield


@contextmanager
def capture_output(log_path: Path, name: str, event_queue: MPQueue) -> Iterator[None]:
    """Capture output when possible; otherwise redirect it to a file only."""
    if _can_use_fd_capture():
        with _redirect_fd(log_path, name=name, event_queue=event_queue):
            yield
    elif _can_use_fd_redirect():
        with _redirect_fd(log_path):
            yield
    else:
        with _redirect_output_python_to_file(log_path):
            yield


def _truncate(text: str, width: int) -> str:
    """Truncate a line to the terminal width."""
    if len(text) <= width:
        return text
    return f"{text[: max(0, width - 3)]}..."


def _status_lines(
    running: Sequence[str],
    latest_output: dict[str, str],
    completed: int,
    failed: int,
    total: int,
) -> list[str]:
    """Build the dynamic running-label block."""
    terminal_width = max(MIN_TERMINAL_WIDTH, get_terminal_size((120, 20)).columns - 2)
    lines = [
        _truncate(
            f"[{completed}/{total}] labels completed | {failed} failed | {len(running)} running",
            terminal_width,
        ),
    ]
    for label in running:
        output = _ANSI_PATTERN.sub("", latest_output.get(label, "")).strip()
        line = f"{label} │ {output}" if output else label
        lines.append(_truncate(line, terminal_width))
    return lines


def _clear_dynamic(previous_line_count: int) -> None:
    """Clear only the dynamic running-label block."""
    if not _can_use_ansi() or not previous_line_count:
        return
    sys.stdout.write(f"\x1b[{previous_line_count}F")
    for _ in range(previous_line_count):
        sys.stdout.write("\x1b[2K\n")
    sys.stdout.write(f"\x1b[{previous_line_count}F")
    sys.stdout.flush()


def _render_dynamic(lines: list[str]) -> int:
    """Render the dynamic running-label block."""
    if not _can_use_ansi():
        return 0
    for line in lines:
        sys.stdout.write(f"\x1b[2K{line}\n")
    sys.stdout.flush()
    return len(lines)


def run_with_progress(  # noqa: C901, PLR0913, PLR0915, PLR0917
    pool: Pool,
    tasks: list[TTask],
    process_count: int,
    errors_path: Path,
    event_queue: MPQueue,
    run_task: Callable[[TTask, MPQueue], None],
    task_name: Callable[[TTask], str],
) -> tuple[int, int]:
    """Run tasks with a bounded pool and a label-level progress display."""
    pending = deque(tasks)
    running: list[str] = []
    latest_output: dict[str, str] = {}
    succeeded = 0
    failed = 0
    total = len(tasks)
    max_running = min(process_count, total)
    previous_line_count = 0
    live_display = _can_use_fd_capture() and _can_use_ansi()

    def submit_next() -> None:
        if not pending:
            return
        task = pending.popleft()
        name = task_name(task)
        running.append(name)
        if not live_display:
            print(f"{name} │ running", flush=True)  # noqa: T201
        pool.apply_async(run_task, (task, event_queue))

    def render() -> None:
        nonlocal previous_line_count
        if not live_display:
            return
        _clear_dynamic(previous_line_count)
        previous_line_count = _render_dynamic(
            _status_lines(
                running,
                latest_output,
                succeeded + failed,
                failed,
                total,
            ),
        )

    for _ in range(max_running):
        submit_next()
    render()

    while running:
        kind, name, value, detail = event_queue.get()
        if kind == "output":
            if name in running:
                previous_output = latest_output.get(name)
                latest_output[name] = value
                if live_display:
                    render()
                elif value != previous_output:
                    print(f"{name} │ {value}", flush=True)  # noqa: T201
            continue

        if live_display:
            _clear_dynamic(previous_line_count)
            previous_line_count = 0
        running.remove(name)
        latest_output.pop(name, None)
        if value == "ok":
            succeeded += 1
        else:
            failed += 1
            with errors_path.open("a", encoding="utf-8") as f:
                f.write(f"=== {name} ===\n{detail}\n")
        print(f"{name} │ {value.upper()}", flush=True)  # noqa: T201
        submit_next()
        render()

    if live_display:
        _clear_dynamic(previous_line_count)
    return succeeded, failed
