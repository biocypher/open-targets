from open_targets.data.schema import Targets


# Test the script is correctly generated and importable
def test_targets():
    assert Targets.id == "targets"
