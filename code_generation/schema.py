"""Functions for generating the schema.py file.

To ease the use of the adaptor and move as many errors as possible to edit time,
the schema of the Open Targets datasets are represented as Python accurately
typed classes in `schema.py`. By referencing these classes instead of hard
coding the information such as dataset or field names, errors are caught at
edit time instead of run time. This is particularly useful when the targeted
Open Targets version is updated. The schema in Python domain is also useful for
code completion, type checking and dataset discovery, especially for LLM
integration.

To generate the schema, metadata from the Open Targets server is downloaded
and deserialised into Python objects. Jinja then is used to generate the schema
classes from the metadata.
"""

from dataclasses import dataclass, replace
from typing import Any

from pydantic.alias_generators import to_pascal, to_snake

from open_targets.data.metadata.model import (
    OpenTargetsDatasetArrayTypeModel,
    OpenTargetsDatasetComplexTypeModel,
    OpenTargetsDatasetFieldModelTypeModel,
    OpenTargetsDatasetFieldType,
    OpenTargetsDatasetFormat,
    OpenTargetsDatasetMapTypeModel,
    OpenTargetsDatasetStructTypeModel,
)
from open_targets.data.schema_base import Dataset, Field, MapField, ScalarField, SequenceField, StructField


@dataclass(frozen=True)
class FieldInfo:
    """Intermediate class for fields and intrinsic fields of complex type."""

    name: str
    type: OpenTargetsDatasetFieldModelTypeModel
    nullable: bool


@dataclass(frozen=True)
class InnerClassInfo:
    """Info of an inner class named Field.

    An inner class named `Field` serving as an interface of fields under a
    parent class so that the type could be used to include the full set of
    fields under a dataset or field.

    Attributes:
        inherit_from: The class that this inner class inherits from.

    """

    inherit_from: str


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class PrefixedClassName:
    """A class name with a prefix."""

    prefix: str
    name: str

    def __str__(self) -> str:
        """Return the prefixed class name."""
        return f"{self.prefix}{self.name}"


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class FieldsHandlerResult:
    """Result of recursive_handle_fields."""

    class_infos: list[ClassInfo]
    fields_attribute: LateAttribute
    field_attributes: list[LateAttribute]


def capitalise_first(s: str) -> str:
    """Capitalise ONLY the first letter of a string."""
    return s[0].upper() + s[1:]


def quote(s: str) -> str:
    """Add quotes around a string."""
    return f'"{s}"'


def get_fields(type_model: OpenTargetsDatasetFieldModelTypeModel) -> list[FieldInfo]:
    """Get the fields or intrinsic fields of a complex type.

    For struct type, get the fields. For other complex types, get their intrisic
    fields such as `element`, `key` and `value`
    """
    if isinstance(type_model, OpenTargetsDatasetComplexTypeModel):
        if isinstance(type_model, OpenTargetsDatasetStructTypeModel):
            return [FieldInfo(name=field.name, type=field.type, nullable=field.nullable) for field in type_model.fields]
        if isinstance(type_model, OpenTargetsDatasetArrayTypeModel):
            return [FieldInfo(name="element", type=type_model.element_type, nullable=type_model.contains_null)]
        if isinstance(type_model, OpenTargetsDatasetMapTypeModel):
            return [
                FieldInfo(name="key", type=type_model.key_type, nullable=False),
                FieldInfo(name="value", type=type_model.value_type, nullable=type_model.value_contains_null),
            ]
    return []


def prefix_field_attributes(attributes: list[LateAttribute]) -> list[LateAttribute]:
    """Prefix the name of the attributes with `f_`."""
    return [replace(i, name=f"f_{i.name}") for i in attributes]


def recursive_handle_fields(
    fields: list[FieldInfo],
    owner_path: list[PrefixedClassName],
) -> FieldsHandlerResult:
    """Generate and sort attributes and class information for fields."""
    field_class_infos = list[ClassInfo]()
    field_attributes = list[LateAttribute]()

    for field in fields:
        field_class_info = recursive_get_field_class_info(field, owner_path)
        field_class_infos.append(field_class_info)
        field_attributes.append(
            LateAttribute(
                name=f"{to_snake(field.name)}",
                type=f"Final[type[{quote(str(field_class_info.name))}]]",
                value=str(field_class_info.name),
            ),
        )

    field_class_infos = sorted(field_class_infos, key=lambda i: str(i.name))
    fields_attribute = LateAttribute(
        name="fields",
        type=f"Final[Sequence[type[{Field.__name__}]]]",
        value=f"[{', '.join(str(i.name) for i in field_class_infos)}]",
    )
    field_attributes = sorted(field_attributes, key=lambda i: i.name)

    return FieldsHandlerResult(
        class_infos=field_class_infos,
        fields_attribute=fields_attribute,
        field_attributes=field_attributes,
    )


def recursive_get_field_class_info(
    field: FieldInfo,
    owner_path: list[PrefixedClassName],
) -> ClassInfo:
    """Convert a field to a ClassInfo.

    Convert a field to a ClassInfo and it's children fields to ClassInfos
    recursively.
    """
    dataset_class_name = owner_path[0]
    owner_class_name = owner_path[-1]

    # Naming in Open Targets data is inconsistent, normalise them to snake
    # case first
    normalised_name_in_snake_case = to_snake(field.name)
    field_class_name = PrefixedClassName("Field", owner_class_name.name + to_pascal(normalised_name_in_snake_case))
    field_path = [*owner_path, field_class_name]

    attributes = [
        LateAttribute("name", "Final[str]", quote(field.name)),
        LateAttribute(
            name="data_type",
            type=f"Final[{OpenTargetsDatasetFieldType.__name__}]",
            value=str(field.type.type)
            if isinstance(field.type, OpenTargetsDatasetComplexTypeModel)
            else str(field.type),
        ),
        LateAttribute("dataset", f"Final[type[{Dataset.__name__}]]", str(dataset_class_name)),
        LateAttribute(
            "path",
            f"Final[Sequence[type[{Field.__name__}]]]",
            f"[{', '.join(str(i) for i in field_path)}]",
        ),
    ]
    dependants = list[ClassInfo]()
    fields = get_fields(field.type)

    if len(fields) > 0:
        result = recursive_handle_fields(fields, field_path)
        dependants.extend(result.class_infos)
        if isinstance(field.type, OpenTargetsDatasetStructTypeModel):
            attributes.append(result.fields_attribute)
        attributes.extend(
            prefix_field_attributes(result.field_attributes)
            if isinstance(field.type, OpenTargetsDatasetStructTypeModel)
            else result.field_attributes,
        )

    match field.type:
        case OpenTargetsDatasetStructTypeModel():
            inherit_from = f"{StructField.__name__}"
        case OpenTargetsDatasetArrayTypeModel():
            inherit_from = f"{SequenceField.__name__}"
        case OpenTargetsDatasetMapTypeModel():
            inherit_from = f"{MapField.__name__}"
        case _:
            inherit_from = f"{ScalarField.__name__}"

    return ClassInfo(
        name=field_class_name,
        late_attributes=attributes,
        dependants=dependants,
        inherit_from=inherit_from,
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

        fields = [
            FieldInfo(name=field.name, type=field.type, nullable=field.nullable)
            for field in dataset_metadata.dataset_schema.fields
        ]
        result = recursive_handle_fields(fields, [class_name])
        dependants.extend(result.class_infos)
        attributes.append(result.fields_attribute)
        attributes.extend(prefix_field_attributes(result.field_attributes))

        class_infos.append(
            ClassInfo(
                name=class_name,
                late_attributes=attributes,
                dependants=dependants,
                inherit_from=f"{Dataset.__name__}",
            ),
        )

    return {
        "class_infos": class_infos,
    }
