"""Functions for generating the schema.py file."""

from dataclasses import dataclass
from typing import Any

from pydantic.alias_generators import to_pascal, to_snake

from open_targets.data.metadata.model import (
    OpenTargetsDatasetArrayTypeModel,
    OpenTargetsDatasetFieldModel,
    OpenTargetsDatasetFormat,
    OpenTargetsDatasetMapTypeModel,
    OpenTargetsDatasetStructTypeModel,
)


@dataclass
class InnerFieldClassInfo:
    """Info of an inner class named Field.

    An inner class named `Field` serving as an interface of fields under a
    parent class so that the type could be used to include the full set of
    fields under a dataset or field.

    Attributes:
        inherit_from: The class that this inner class inherits from.

    """

    inherit_from: str


@dataclass
class LateAttribute:
    """Key and value of a class attribute that is not immediately assigned.

    Information of an attribute of a class that is not immediately assigned
    when generating the corresponding class due to circular referencing. Values
    are assigned separately after class definitions.

    Attributes:
        name: The name of the attribute.
        type: The Python type of the attribute.
        value: The value of the attribute.

    """

    name: str
    type: str
    value: str


@dataclass
class PrefixedClassName:
    """A class name with a prefix."""

    prefix: str
    name: str

    def __str__(self) -> str:
        """Return the prefixed class name."""
        return f"{self.prefix}{self.name}"


@dataclass
class ClassInfo:
    """Information about a class to be generated.

    The dependency structure is tracked by the `dependants` attribute.
    Technically not necessary, but ordering classes by dependency makes the file
    more readable.

    Attributes:
        name: The name of the class.
        late_attributes: A list of late attributes.
        dependants: A list of classes that depend on this class.
        inherit_from: The class that this class inherits from.

    """

    name: PrefixedClassName
    late_attributes: list[LateAttribute]
    dependants: list["ClassInfo"]
    inherit_from: str
    inner_field_class: InnerFieldClassInfo | None


def capitalise_first(s: str) -> str:
    """Capitalise ONLY the first letter of a string."""
    return s[0].upper() + s[1:]


def quote(s: str) -> str:
    """Add quotes around a string."""
    return f'"{s}"'


def recursive_get_field_class_info(
    field: OpenTargetsDatasetFieldModel,
    path: list[PrefixedClassName],
) -> ClassInfo:
    """Recursively convert a field or dataset into a ClassInfo.

    Recursively convert a field or dataset and it's children into a ClassInfo
    object.

    """
    # Naming in Open Targets data is inconsistent, normalise them to snake
    # case first
    normalised_name_in_snake_case = to_snake(field.name)
    dataset_class_name = path[0]
    class_name = PrefixedClassName("Field", path[-1].name + to_pascal(normalised_name_in_snake_case))
    attributes = [
        LateAttribute("name", "Final[str]", quote(field.name)),
        LateAttribute(
            name="data_type",
            type="Final[OpenTargetsDatasetFieldType]",
            value=str(field.type.type)
            if isinstance(
                field.type,
                OpenTargetsDatasetArrayTypeModel | OpenTargetsDatasetMapTypeModel | OpenTargetsDatasetStructTypeModel,
            )
            else str(field.type),
        ),
        LateAttribute("dataset", "Final[type[Dataset]]", str(dataset_class_name)),
        LateAttribute("path", "Final[list[type[DatasetField]]]", f"[{', '.join(str(i) for i in [*path, class_name])}]"),
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

    child_class_infos = list[ClassInfo]()
    for child_field in fields:
        child_class_info = recursive_get_field_class_info(child_field, [*path, class_name])
        child_class_infos.append(child_class_info)
        dependants.append(child_class_info)
        attributes.append(
            LateAttribute(
                name=f"f_{to_snake(child_field.name)}",
                type=f"Final[type[{quote(str(child_class_info.name))}]]",
                value=str(child_class_info.name),
            ),
        )
    if len(child_class_infos) > 0:
        attributes.append(
            LateAttribute(
                name="fields",
                type=f'Final[list[type["{class_name}.Field"]]]',
                value=f"[{', '.join(str(i.name) for i in child_class_infos)}]",
            ),
        )

    return ClassInfo(
        name=class_name,
        late_attributes=attributes,
        dependants=dependants,
        inherit_from=f"{path[-1]}.Field",
        inner_field_class=InnerFieldClassInfo(inherit_from=f"{path[-1]}.Field") if len(dependants) > 0 else None,
    )


def create_schema_render_context() -> dict[str, Any]:
    """Return a jinja context for the schema.py file.

    Download and deserialise the metadata from Open Targets server and convert
    them into LateAttribute and ClassInfo objects.
    """
    # Importing here to avoid circular dependency
    from open_targets.data.metadata import fetch_open_targets_dataset_metadata

    datasets_metadata = fetch_open_targets_dataset_metadata(filter_format=[OpenTargetsDatasetFormat.PARQUET])

    class_infos = list[ClassInfo]()
    for dataset_metadata in datasets_metadata:
        class_name = PrefixedClassName(prefix="Dataset", name=capitalise_first(dataset_metadata.id))
        attributes = [LateAttribute(name="id", type="Final[str]", value=quote(dataset_metadata.id))]
        dependants = list[ClassInfo]()

        child_class_infos = list[ClassInfo]()
        for child_field in dataset_metadata.dataset_schema.fields:
            child_class_info = recursive_get_field_class_info(child_field, [class_name])
            child_class_infos.append(child_class_info)
            dependants.append(child_class_info)
            attributes.append(
                LateAttribute(
                    name=f"f_{to_snake(child_field.name)}",
                    type=f"Final[type[{quote(str(child_class_info.name))}]]",
                    value=str(child_class_info.name),
                ),
            )
        if len(child_class_infos) > 0:
            attributes.append(
                LateAttribute(
                    name="fields",
                    type=f'Final[list[type["{class_name}.Field"]]]',
                    value=f"[{', '.join(str(i.name) for i in child_class_infos)}]",
                ),
            )

        class_infos.append(
            ClassInfo(
                name=class_name,
                late_attributes=attributes,
                dependants=dependants,
                inherit_from="Dataset",
                inner_field_class=InnerFieldClassInfo(inherit_from="DatasetField"),
            ),
        )

    return {
        "class_infos": class_infos,
    }
