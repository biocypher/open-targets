"""Acquisition definition that acquires nodes of pharmacogenomics drugs."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetPharmacogenomics,
    FieldPharmacogenomicsDrugs,
    FieldPharmacogenomicsDrugsElementDrugId,
    FieldPharmacogenomicsDrugsElementDrugFromSource,
)

node_pharmacogenomics_drug: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetPharmacogenomics,
        exploded_field=FieldPharmacogenomicsDrugs,
    ),
    primary_id=FieldPharmacogenomicsDrugsElementDrugId,
    label="PHARMACOGENOMICS_DRUG",
    properties=[
        FieldPharmacogenomicsDrugsElementDrugFromSource,
    ],
)
