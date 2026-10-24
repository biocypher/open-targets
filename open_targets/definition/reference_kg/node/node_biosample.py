"""Summary: BIOSAMPLE nodes from Biosample dataset.

Definition for BIOSAMPLE nodes: represents biological samples (e.g., cell types, tissues)
derived from the Biosample ontology/dataset, providing a standardized vocabulary for
sample attribution in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetBiosample,
    FieldBiosampleBiosampleId,
    FieldBiosampleBiosampleName,
    FieldBiosampleDescription,
    FieldBiosampleSynonyms,
)
from open_targets.definition.helper import get_namespaced_expression

node_biosample: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetBiosample),
    primary_id=get_namespaced_expression("biosample", FieldBiosampleBiosampleId),
    label="BIOSAMPLE",
    properties=[
        FieldBiosampleBiosampleName,
        FieldBiosampleDescription,
        FieldBiosampleSynonyms,
    ],
)
