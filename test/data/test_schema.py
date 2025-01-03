from open_targets.data import schema
from open_targets.data.schema import DatasetTargets


def test_dataset_importable() -> None:
    assert DatasetTargets.id == "targets"


def test_all_fields_are_assigned() -> None:
    class_names = [
        i
        for i in dir(schema)
        if (i.startswith("Dataset") and i != "Dataset") or (i.startswith("Field") and i != "Field")
    ]
    classes = [getattr(schema, i) for i in class_names]
    for class_ in classes:
        fields = [i for i in vars(class_) if not i.startswith("__")]
        for field in fields:
            assert getattr(class_, field) is not None
