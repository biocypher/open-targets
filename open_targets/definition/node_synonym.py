"""Acquisition definition that acquires nodes of synonyms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesSynonyms,
    FieldDiseasesSynonymsHasBroadSynonym,
    FieldDiseasesSynonymsHasExactSynonym,
    FieldDiseasesSynonymsHasNarrowSynonym,
    FieldDiseasesSynonymsHasRelatedSynonym,
    DatasetMolecule,
    FieldMoleculeSynonyms,
)
from open_targets.adapter.expression import BuildCurieExpression, LiteralExpression, FieldExpression

node_disease_synonym_broad: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonyms.f_has_broad_synonym,
    ),
    primary_id=FieldDiseasesSynonymsHasBroadSynonym.element,
    label="SYNONYM",
    properties=[],
)

node_disease_synonym_exact: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonyms.f_has_exact_synonym,
    ),
    primary_id=FieldDiseasesSynonymsHasExactSynonym.element,
    label="SYNONYM",
    properties=[],
)

node_disease_synonym_narrow: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonyms.f_has_narrow_synonym,
    ),
    primary_id=FieldDiseasesSynonymsHasNarrowSynonym.element,
    label="SYNONYM",
    properties=[],
)

node_disease_synonym_related: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonyms.f_has_related_synonym,
    ),
    primary_id=FieldDiseasesSynonymsHasRelatedSynonym.element,
    label="SYNONYM",
    properties=[],
)

node_molecule_synonym: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeSynonyms,
    ),
    primary_id=FieldMoleculeSynonyms.element,
    label="SYNONYM",
    properties=[],
)
