"""Summary: DISEASE_PHENOTYPE_ASSOCIATION -> PHENOTYPE edges.

Definition for HAS_OBJECT edges (disease_phenotype_association -> phenotype):
explodes disease->HPO evidence to link each DISEASE_PHENOTYPE_ASSOCIATION node
to the PHENOTYPE (HPO term) it references, binding the phenotype endpoint of the
association in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseasePhenotype,
    FieldDiseasePhenotypeEvidence,
    FieldDiseasePhenotypePhenotype,
)
from open_targets.definition.helper import get_namespaced_expression
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import disease_phenotype_association_primary_id_expression

edge_disease_phenotype_association_has_object_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetDiseasePhenotype,
            exploded_field=FieldDiseasePhenotypeEvidence,
        ),
        primary_id=NewUuidExpression(),
        source=disease_phenotype_association_primary_id_expression,
        target=get_namespaced_expression("phenotype", FieldDiseasePhenotypePhenotype),
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
