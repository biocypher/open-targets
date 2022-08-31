#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BioCypher - OTAR prototype
"""

import re

import biocypher
import neo4j_utils as nu
import pandas as pd
from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class BioCypherAdapter:
    def __init__(
        self,
        dirname=None,
        db_name="neo4j",
        id_batch_size: int = int(1e6),
        user_schema_config_path="config/schema_config.yaml",
    ):

        self.db_name = db_name
        self.id_batch_size = id_batch_size

        # write driver
        self.bcy = biocypher.Driver(
            offline=True,  # set offline to true,
            # connect to running DB for input data via the neo4j driver
            user_schema_config_path=user_schema_config_path,
            delimiter="¦",
        )
        # start writer
        self.bcy.start_bl_adapter()
        self.bcy.start_batch_writer(dirname=dirname, db_name=self.db_name)

        # read driver
        self.driver = nu.Driver(
            db_name="neo4j",
            db_uri="bolt://localhost:7687",
            db_passwd="your_password_here",
            multi_db=False,
            max_connection_lifetime=7200,
        )

        # indicator whether translation is necessary
        self.translation_needed = False

    def write_to_csv_for_admin_import(self):
        """
        Write nodes and edges to admin import csv files.
        """

        self.write_nodes()
        self.write_edges()
        self.bcy.write_import_call()

    def write_nodes(self):
        """
        Write nodes to admin import csv files.
        """

        # get node labels from csv
        with open("data/node_labels.csv", "r") as f:
            # import to pandas dataframe
            node_labels = pd.read_csv(f)

        node_labels = [
            # "GraphProtein",
            # "GraphGene",
            # "GraphNucleicAcid",
            # "GraphMolecule",
            # "GraphComplex",
            # above unused because they are included in GraphInteractor
            "GraphInteractor",
            "GraphPublication",
        ]

        for label in node_labels:
            with self.driver.session() as session:
                # writing of one type needs to be completed inside
                # this session
                session.read_transaction(
                    self._get_node_ids_and_write_batches_tx, label
                )

        if self.translation_needed:
            logger.warning("At least one node data type requires translation.")

    def write_edges(self) -> None:
        """
        Write edges to admin import csv files.
        """

        # get node labels from csv
        with open("data/granular_relationships.txt", "r") as f:
            rel_labels = f.read().splitlines()

        rel_labels = rel_labels[1:]
        rel_labels = [label.split(",") for label in rel_labels]

        # rel_labels = [
        #     ("Clinically_relevant_variant", "ASSOCIATED_WITH", "Disease"),
        # ]
        # rel_labels = []

        for src, typ, tar in rel_labels:

            # skip some types
            if not typ in [
                "VARIANT_FOUND_IN_CHROMOSOME",
                "LOCATED_IN",
                "HAS_STRUCTURE",
                "IS_SUBSTRATE_OF",
                "IS_QCMARKER_IN_TISSUE",
                "VARIANT_IS_CLINICALLY_RELEVANT",
                "IS_A_KNOWN_VARIANT",
            ]:

                with self.driver.session() as session:
                    # writing of one type needs to be completed inside
                    # this session
                    session.read_transaction(
                        self._get_rel_ids_and_write_batches_tx,
                        src,
                        typ,
                        tar,
                    )

    def _get_node_ids_and_write_batches_tx(
        self,
        tx,
        label,
    ):
        """
        Write nodes to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(f"MATCH (n:{label}) " "RETURN id(n) as id")

        id_batch = []
        for record in result:
            # collect in batches
            id_batch.append(record["id"])
            if len(id_batch) == self.id_batch_size:

                # if full batch, trigger write process
                self._write_nodes(id_batch, label)
                id_batch = []

            # check if result depleted
            elif result.peek() is None:

                # write last batch
                self._write_nodes(id_batch, label)

    def _get_rel_ids_and_write_batches_tx(
        self,
        tx,
        src,
        typ,
        tar,
    ):
        """
        Write edges to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(
            f"MATCH (n:{src})-[r:{typ}]->(m:{tar}) " "RETURN id(r) as id"
        )

        id_batch = []
        for record in result:
            # collect in batches
            if len(id_batch) < self.id_batch_size:
                id_batch.append(record["id"])

                # check if result depleted
                if result.peek() is None:
                    # write last batch
                    self._write_edges(id_batch, src, typ, tar)

            # if full batch, trigger write process
            else:
                self._write_edges(id_batch, src, typ, tar)
                id_batch = []

    def _write_nodes(self, id_batch, label):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            label: label of the node type
        """

        def node_gen():
            with self.driver.session() as session:
                results = session.read_transaction(get_nodes_tx, id_batch)

                for res in results:

                    _id, _type = self._process_node_id_and_type(
                        res["n"], label
                    )
                    _props = res["n"]
                    yield (_id, _type, _props)

        self.bcy.write_nodes(
            nodes=node_gen(),
            db_name=self.db_name,
        )

    def _write_edges(self, id_batch, src, typ, tar):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            src: source node label

            typ: relationship type

            tar: target node label
        """

        def edge_gen():
            with self.driver.session() as session:
                results = session.read_transaction(get_rels_tx, id_batch)

                for res in results:

                    # extract relevant id
                    _src = self._process_node_id_and_type(res["n"]["id"], src)
                    _tar = self._process_node_id_and_type(res["m"]["id"], tar)

                    # split some relationship types
                    if typ in [
                        "MENTIONED_IN_PUBLICATION",
                        "ASSOCIATED_WITH",
                        "ANNOTATED_IN_PATHWAY",
                        "MAPS_TO",
                        "VARIANT_FOUND_IN_GENE",
                        "TRANSLATED_INTO",
                        "HAS_MODIFIED_SITE",
                    ]:
                        _type = "_".join([typ, src, tar])
                    else:
                        _type = typ
                    _props = {}

                    # add properties
                    if typ in [
                        "ACTS_ON",
                        "COMPILED_INTERACTS_WITH",
                        "CURATED_INTERACTS_WITH",
                    ]:
                        _props = {"type": typ}
                    elif typ == "IS_BIOMARKER_OF_DISEASE":
                        props = res["PROPERTIES(r)"]
                        _props = {
                            "age_range": props.get("age_range"),
                            "age_units": props.get("age_units"),
                            "assay": props.get("assay"),
                            "is_routine": props.get("is_routine"),
                            "is_used_in_clinic": props.get(
                                "is_used_in_clinic"
                            ),
                            "normal_range": props.get("normal_range"),
                            "sex": props.get("sex"),
                        }

                    yield (_src, _tar, _type, _props)

        self.bcy.write_edges(
            edges=edge_gen(),
            db_name=self.db_name,
        )

    def _process_node_id_and_type(self, _node, _type):
        """
        Add prefixes to avoid multiple assignment.

        Split up nodes in case of Protein (includes Peptides).

        TODO regex id checks?

        TODO how to handle "EBI-" accessions (they can refer to multiple
        DBs)? is there an API that returns, eg, "intact" for the respective
        members?
        """

        # regex patterns
        chebi_no_prefix_pattern = re.compile("^\d{,6}$")
        chebi_prefix_pattern = re.compile("^CHEBI:")
        ebi_prefix_pattern = re.compile("^EBI-")
        cid_prefix_pattern = re.compile("^CID:")
        sid_prefix_pattern = re.compile("^SID:")
        chembl_prefix_pattern = re.compile("^CHEMBL")
        signor_prefix_pattern = re.compile("^SIGNOR-")
        reactome_prefix_pattern = re.compile("^R-[A-Z]{3}-\d+(-\d+)?(\.\d+)?$")
        uniprot_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?$"
        )
        uniprot_hyphenated_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?"
        )  # removed end of line character from regex to include proteins with hyphenated accessions

        _id = None

        if _type == "GraphInteractor":
            # any kind of interaction participant

            _prefix = _node["uniqueKey"]

            if "protein" in _prefix:
                if "uniprotName" in _node:
                    _id = "uniprot:" + _node["uniprotName"]
                    _type = "GraphProtein"
                else:
                    _id = "intact:" + _node["ac"]
                    _type = "GraphPeptide"

            elif "nucleic acid" in _prefix:
                if _node.get("ac"):
                    _id = "intact:" + _node["ac"]
                    _type = "intact:GraphNucleicAcid"
                elif reactome_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "reactome:" + _node["preferredIdentifierStr"]
                    _type = "reactome:GraphNucleicAcid"

            elif "molecule" in _prefix:
                # several cases:
                #
                # no prefix (but chebi id, at least i assume that is the
                # case, since those are ints up to 6 digits)
                #
                # "CHEBI:" prefix (remove)
                #
                # non-chebi ids: EBI- and CID:, SID: (pubchem); and CHEMBL

                if chebi_no_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "chebi:" + _node["preferredIdentifierStr"]

                elif chebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "chebi:" + _node["preferredIdentifierStr"].replace(
                        "CHEBI:", ""
                    )

                elif ebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif cid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif sid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif chembl_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                else:
                    print(_node)

                _type = "GraphSmallMolecule"

            elif "gene" in _prefix:
                _id = "exac.gene:" + _node["preferredIdentifierStr"]
                _type = "GraphGene"

            elif "polymer" in _prefix:
                # there is one small nuclear RNA with this prefix in the DB
                # however, it has NCBI id instead of ENSEMBL
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True
                _type = "GraphPolymer"

            elif "complex" in _prefix:
                _id = "complexportal:" + _node["preferredIdentifierStr"]
                _type = "GraphComplex"

            else:
                # generic interactor, but can include prefixes used above
                # prefixes included:
                # "CID:", "CHEBI:", "SIGNOR-", "R-", "EBI-", or uniprot

                if cid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif chebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif signor_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif reactome_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif ebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif uniprot_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _node["preferredIdentifierStr"]
                    _type = "GraphProtein"
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif uniprot_hyphenated_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    # split id at hyphen and use only first part
                    _id = _node["preferredIdentifierStr"].split("-")[0]
                    _type = "GraphProtein"
                    logger.warning(
                        f"Added protein {_id} from {_node['preferredIdentifierStr']}. "
                        "Information may be lost."
                    )

                else:
                    print(_type + "==============================")
                    print(_node)

        elif _type == "GraphGene":
            _id = "exac.gene:" + _node["preferredIdentifierStr"]

        elif _type == "GraphPublication":
            if _node.get("pubmedIdStr"):
                _id = "pubmed:" + _node["pubmedIdStr"]
            else:
                print(_type + "==============================")
                print(_node)

        return _id, _type


def get_nodes_tx(tx, ids):
    result = tx.run(
        "MATCH (n) " "WHERE id(n) IN {ids} " "RETURN n",
        ids=ids,
    )
    return result.data()


def get_rels_tx(tx, ids):
    result = tx.run(
        "MATCH (n)-[r]->(m) "
        "WHERE id(r) IN {ids} "
        "RETURN n, PROPERTIES(r), m",
        ids=ids,
    )
    return result.data()
