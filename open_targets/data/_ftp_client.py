"""FTP client module.

This module provides convenient functions listing and downloading files from the
Open Targets Platform FTP server.
"""

import contextlib
from collections.abc import Callable
from dataclasses import dataclass
from ftplib import FTP, error_reply
from io import BytesIO
from typing import Any, Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
Self = TypeVar("Self", bound="FTPClient")
_ftp_cache: dict["FTPClient", FTP] = {}


def _ftp_client_connect(
    func: Callable[Concatenate[Self, FTP, P], R],
) -> Callable[Concatenate[Self, P], R]:
    def wrapper(client: Self, *args: P.args, **kwargs: P.kwargs) -> R:
        if client in _ftp_cache:
            ftp = _ftp_cache[client]
        else:
            ftp = FTP(client.host)  # noqa: S321
            ftp.login()
            _ftp_cache[client] = ftp

        try:
            # Test if the connection is still valid
            ftp.voidcmd("NOOP")
        except error_reply:
            # Try to close the old connection anyway to avoid hanging
            # connections
            with contextlib.suppress(Exception):
                ftp.close()
            ftp = FTP(client.host)  # noqa: S321
            ftp.login()

        return func(client, ftp, *args, **kwargs)

    return wrapper


@dataclass(frozen=True)
class FTPClientListResult:
    files: list[str]
    dirs: list[str]


class FTPClient:
    host: str

    def __init__(self, host: str) -> None:
        self.host = host

    @_ftp_client_connect
    def list_directory(self, ftp: FTP, path: str) -> FTPClientListResult:
        return self._recursive_list(ftp, path, 0)

    @_ftp_client_connect
    def traverse_directory(self, ftp: FTP, path: str, depth: None | int = None) -> FTPClientListResult:
        return self._recursive_list(ftp, path, depth)

    @_ftp_client_connect
    def retrieve_file(self, ftp: FTP, path: str, stream_handler: None | Callable[[bytes], Any] = None) -> None | bytes:
        if stream_handler is None:
            stream = BytesIO()
            ftp.retrbinary(f"RETR {path}", stream.write)
            stream.flush()
            return stream.getvalue()

        ftp.retrbinary(f"RETR {path}", stream_handler)
        return None

    def _recursive_list(self, ftp: FTP, path: str, depth: None | int = None) -> FTPClientListResult:
        path = path.rstrip("/")
        all_files: list[str] = []
        all_dirs: list[str] = []
        files: list[str] = []
        dirs: list[str] = []

        def process_line(line: str) -> None:
            parts = line.split(maxsplit=8)
            full_path = f"{path}/{parts[-1]}"
            is_dir = parts[0].startswith("d")
            if is_dir:
                dirs.append(full_path)
            else:
                files.append(full_path)

        ftp.cwd(path)
        ftp.retrlines("LIST", process_line)

        all_files.extend(files)
        all_dirs.extend(dirs)

        if depth is None or depth > 0:
            for d in dirs:
                result = self._recursive_list(ftp, d, None if depth is None else depth - 1)
                all_files.extend(result.files)
                all_dirs.extend(result.dirs)

        return FTPClientListResult(files=all_files, dirs=all_dirs)
