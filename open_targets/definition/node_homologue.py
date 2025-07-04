"""Acquisition definition that acquires nodes of homologues."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsHomologues,
    FieldTargetsHomologuesElementTargetGeneId,
    FieldTargetsHomologuesElementTargetGeneSymbol,
    FieldTargetsHomologuesElementHomologyType,
    FieldTargetsHomologuesElementIsHighConfidence,
    FieldTargetsHomologuesElementPriority,
    FieldTargetsHomologuesElementQueryPercentageIdentity,
    FieldTargetsHomologuesElementSpeciesId,
    FieldTargetsHomologuesElementSpeciesName,
    FieldTargetsHomologuesElementTargetPercentageIdentity,
)

node_homologue: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsHomologues,
    ),
    primary_id=FieldTargetsHomologuesElementTargetGeneId,
    label="HOMOLOGUE",
    properties=[
        FieldTargetsHomologuesElementTargetGeneSymbol,
        FieldTargetsHomologuesElementHomologyType,
        FieldTargetsHomologuesElementIsHighConfidence,
        FieldTargetsHomologuesElementPriority,
        FieldTargetsHomologuesElementQueryPercentageIdentity,
        FieldTargetsHomologuesElementSpeciesId,
        FieldTargetsHomologuesElementSpeciesName,
        FieldTargetsHomologuesElementTargetPercentageIdentity,
    ],
)
