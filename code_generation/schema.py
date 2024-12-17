from dataclasses import dataclass
from typing import Any

from pydantic.alias_generators import to_pascal, to_snake

from open_targets.data.metadata.model import OpenTargetsDatasetFormat


@dataclass
class LateAttribute:
    name: str
    type: str
    value: str


@dataclass
class ClassInfo:
    name: str
    late_attributes: list[LateAttribute]
    dependants: list["ClassInfo"]
    inherit_from: str


def capitalise_first(s: str) -> str:
    return s[0].upper() + s[1:]


def create_schema_render_context() -> dict[str, Any]:
    # Importing here to avoid circular dependency
    from open_targets.data.metadata import fetch_open_targets_dataset_metadata
    from open_targets.data.metadata.model import (
        OpenTargetsDatasetArrayTypeModel,
        OpenTargetsDatasetFieldModel,
        OpenTargetsDatasetMapTypeModel,
        OpenTargetsDatasetStructTypeModel,
    )

    dataset_metadata = fetch_open_targets_dataset_metadata(filter_format=[OpenTargetsDatasetFormat.PARQUET])

    def quote(s: str) -> str:
        return f'"{s}"'

    def recursive_get_class_info(
        dataset_class_name: str,
        field: OpenTargetsDatasetFieldModel,
        path: list[str],
    ) -> ClassInfo:
        # Naming in Open Targets data is inconsistent, normalise them to snake
        # case first
        normalised_name_in_snake_case = to_snake(field.name)
        class_name = (path[-1] if len(path) > 0 else "F" + dataset_class_name[1:]) + to_pascal(
            normalised_name_in_snake_case,
        )
        attributes = [
            LateAttribute("name", "Final[str]", quote(field.name)),
            LateAttribute(
                name="data_type",
                type="Final[OpenTargetsDatasetFieldType]",
                value=str(field.type.type)
                if isinstance(
                    field.type,
                    OpenTargetsDatasetArrayTypeModel
                    | OpenTargetsDatasetMapTypeModel
                    | OpenTargetsDatasetStructTypeModel,
                )
                else str(field.type),
            ),
            LateAttribute("dataset", "Final[type[Dataset]]", dataset_class_name),
            LateAttribute("path", "Final[list[type[DatasetField]]]", f"[{', '.join([*path, class_name])}]"),
        ]
        dependants = list[ClassInfo]()

        if isinstance(field.type, OpenTargetsDatasetStructTypeModel):
            fields = field.type.fields
        elif isinstance(field.type, OpenTargetsDatasetArrayTypeModel) and isinstance(
            field.type.element_type,
            OpenTargetsDatasetStructTypeModel,
        ):
            fields = field.type.element_type.fields
        else:
            fields = []

        for child_field in fields:
            child_class_info = recursive_get_class_info(dataset_class_name, child_field, [*path, class_name])
            dependants.append(child_class_info)
            attributes.append(
                LateAttribute(
                    name=f"f_{to_snake(child_field.name)}",
                    type=f"Final[type[{quote(child_class_info.name)}]]",
                    value=child_class_info.name,
                ),
            )

        return ClassInfo(
            name=class_name,
            late_attributes=attributes,
            dependants=dependants,
            inherit_from="DatasetField",
        )

    class_infos = list[ClassInfo]()
    for dataset_metadata in dataset_metadata:
        class_name = "D" + capitalise_first(dataset_metadata.id)
        attributes = [LateAttribute(name="id", type="Final[str]", value=quote(dataset_metadata.id))]
        dependants = list[ClassInfo]()

        for child_field in dataset_metadata.dataset_schema.fields:
            child_class_info = recursive_get_class_info(class_name, child_field, [])
            dependants.append(child_class_info)
            attributes.append(
                LateAttribute(
                    name=f"f_{to_snake(child_field.name)}",
                    type=f"Final[type[{quote(child_class_info.name)}]]",
                    value=child_class_info.name,
                ),
            )

        class_infos.append(
            ClassInfo(name=class_name, late_attributes=attributes, dependants=dependants, inherit_from="Dataset"),
        )

    return {
        "class_infos": class_infos,
    }
