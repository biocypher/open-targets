from collections.abc import Callable
from typing import Any

from bioregistry.resolve import normalize_curie, normalize_parsed_curie, normalize_prefix

from open_targets.adapter.data_view import DataView
from open_targets.adapter.expression import (
    BuildCurieExpression,
    DataSourceToLicenceExpression,
    Expression,
    ExtractCuriePrefixExpression,
    ExtractSubstringExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
    StringLowerExpression,
    ToStringExpression,
    TransformExpression,
)
from open_targets.adapter.licence import get_datasource_license

CURIE_SEPARATORS = [":", "_", "/"]


def recursive_build_expression_function(
    expression: Expression[Any],
) -> Callable[[DataView], Any]:
    """Build a function chain that evaluates the expression."""
    match expression:
        case FieldExpression():
            return lambda data: data[expression.field]
        case LiteralExpression():
            return lambda _: expression.value
        case TransformExpression():
            if expression.expression is None:
                return lambda _: expression.function(None)
            func = recursive_build_expression_function(expression.expression)
            return lambda data: expression.function(func(data))
        case ToStringExpression():
            func = recursive_build_expression_function(expression.expression)
            return lambda data: str(func(data))
        case StringConcatenationExpression():
            funcs = [recursive_build_expression_function(e) for e in expression.expressions]
            return lambda data: "".join(func(data) for func in funcs)
        case StringLowerExpression():
            func = recursive_build_expression_function(expression.expression)
            return lambda data: func(data).lower()
        case BuildCurieExpression():
            return get_curie_builder(expression)
        case ExtractCuriePrefixExpression():
            func = recursive_build_expression_function(expression.expression)
            return (
                (lambda data: normalize_prefix(extract_curie_prefix(func(data))))
                if expression.normalise
                else (lambda data: extract_curie_prefix(func(data)))
            )
        case NormaliseCurieExpression():
            func = recursive_build_expression_function(expression.expression)
            return lambda data: normalise_curie(func(data))
        case ExtractSubstringExpression():
            func = recursive_build_expression_function(expression.expression)
            separator_func = recursive_build_expression_function(expression.separator)
            return lambda data: func(data).split(separator_func(data))[expression.index]
        case DataSourceToLicenceExpression():
            func = recursive_build_expression_function(expression.datasource)
            return lambda data: get_datasource_license(func(data))
        case _:
            msg = f"Unsupported expression: {expression}"
            raise ValueError(msg)


def get_curie_builder(
    expression: BuildCurieExpression,
) -> Callable[[DataView], str]:
    prefix_func = recursive_build_expression_function(expression.prefix)
    reference_func = recursive_build_expression_function(expression.reference)

    def normalise_curie_builder(data: DataView) -> str:
        prefix, reference = normalize_parsed_curie(prefix_func(data), reference_func(data))
        prefix = "" if prefix is None else prefix
        reference = "" if reference is None else reference
        return f"{prefix}:{reference}"

    return (
        normalise_curie_builder
        if expression.normalise
        else (lambda data: f"{prefix_func(data)}:{reference_func(data)}")
    )


def normalise_curie(string: str) -> str:
    for sep in CURIE_SEPARATORS:
        if sep in string:
            result = normalize_curie(string, sep=sep)
            if result is not None:
                return result
            msg = f"Failed to normalize curie: {string} with separator: {sep}"
            raise ValueError(msg)
    msg = f"Failed to normalize curie: {string}"
    raise ValueError(msg)


def extract_curie_prefix(string: str) -> str:
    for sep in CURIE_SEPARATORS:
        if sep in string:
            return string.split(sep)[0]
    msg = f"Failed to extract curie prefix from: {string}"
    raise ValueError(msg)
