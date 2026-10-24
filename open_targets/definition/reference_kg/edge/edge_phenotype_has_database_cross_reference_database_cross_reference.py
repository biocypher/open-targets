"""Summary: PHENOTYPE -> DATABASE_CROSS_REFERENCE edges for HPO xrefs.

Definition for HAS_DATABASE_CROSS_REFERENCE edges (phenotype): explodes HPO
`dbXRefs` to link each PHENOTYPE node to a hashed DATABASE_CROSS_REFERENCE node
(raw xref stored on the target node), exposing external phenotype IDs in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseaseHpo,
    FieldDiseaseHpoDbXRefs,
    FieldDiseaseHpoDbXRefsElement,
    FieldDiseaseHpoId,
)
from open_targets.definition.helper import get_namespaced_expression, get_namespaced_hash_expression
from open_targets.definition.reference_kg.constant import EdgeLabel, Namespace

edge_phenotype_has_database_cross_reference_database_cross_reference: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetDiseaseHpo,
            exploded_field=FieldDiseaseHpoDbXRefs,
        ),
        primary_id=NewUuidExpression(),
        source=get_namespaced_expression("phenotype", FieldDiseaseHpoId),
        target=get_namespaced_hash_expression(
            Namespace.DATABASE_CROSS_REFERENCE,
            FieldDiseaseHpoDbXRefsElement,
        ),
        label=EdgeLabel.HAS_DATABASE_CROSS_REFERENCE,
        properties=[],
    )
)
