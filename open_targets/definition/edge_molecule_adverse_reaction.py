"""Acquisition definition that acquires edges between molecules and adverse reactions."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAdverseDrugReactions,
    FieldAdverseDrugReactionsActerm,
    FieldAdverseDrugReactionsAterm,
    FieldAdverseDrugReactionsChemblId,
    FieldAdverseDrugReactionsCterm,
    FieldAdverseDrugReactionsLlr,
    FieldAdverseDrugReactionsMeddraCode,
    FieldAdverseDrugReactionsReactionReactionmeddrapt,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_adverse_reaction: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAdverseDrugReactions),
    primary_id=get_arrow_expression(FieldAdverseDrugReactionsChemblId, FieldAdverseDrugReactionsMeddraCode),
    source=FieldAdverseDrugReactionsChemblId,
    target=FieldAdverseDrugReactionsMeddraCode,
    label="MOLECULE_TO_ADVERSE_REACTION",
    properties=[
        FieldAdverseDrugReactionsActerm,
        FieldAdverseDrugReactionsAterm,
        FieldAdverseDrugReactionsCterm,
        FieldAdverseDrugReactionsLlr,
        FieldAdverseDrugReactionsReactionReactionmeddrapt,
        FieldAdverseDrugReactionsA,
        FieldAdverseDrugReactionsB,
        FieldAdverseDrugReactionsC,
        FieldAdverseDrugReactionsD,
        FieldAdverseDrugReactionsUniqReportIdsByDrug,
        FieldAdverseDrugReactionsUniqReportIdsByReaction,
    ],
)
