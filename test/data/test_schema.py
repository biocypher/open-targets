from open_targets.data.schema import DTargets


# Test the script is correctly generated and importable
def test_targets() -> None:
    assert DTargets.id == "targets"
