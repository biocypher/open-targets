"""Summary: namespaced study ID for PHARMACOGENOMICS_ANNOTATION IDs.

Primary ID expression for PHARMACOGENOMICS_ANNOTATION
nodes: namespaces the ClinPGx study ID to create a
stable identifier used by pharmacogenomics annotation
nodes/edges.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
)
from open_targets.data.schema import FieldPharmacogenomicsStudyId
from open_targets.definition.helper import get_namespaced_expression

pharmacogenomics_annotation_primary_id_expression: Final[Expression[str]] = get_namespaced_expression(
    "pharmacogenomics_annotation",
    FieldPharmacogenomicsStudyId,
)
