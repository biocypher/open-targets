#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BioCypher - OTAR prototype
"""

from biocypher import BioCypher
import neo4j_utils as nu
import pandas as pd
from biocypher._logger import logger
from otar_biocypher.utils.id_type_processing import _process_node_id_and_type
from otar_biocypher.utils.transactions import (
    get_bin_int_rels_tx,
    get_interactor_to_organism_edges_tx,
    get_nodes_tx,
)

logger.debug(f"Loading module {__name__}.")


class BarrioHernandezAdapter:
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
        self.bcy = BioCypher(
            biocypher_config_path="config/biocypher_config_barrio.yaml",
        )
        # start writer
        self.bcy._get_writer()

        # read driver
        self.driver = nu.Driver(
            db_name="neo4j",
            db_uri="bolt://localhost:7687",
            db_passwd="your_password_here",
            multi_db=False,
            max_connection_lifetime=7200,
        )

    def write_to_csv_for_admin_import(self):
        """
        Write nodes and edges to admin import csv files.
        """

        self.write_nodes()
        self.write_edges()
        self.bcy.write_import_call()
        self.bcy.log_missing_bl_types()
        self.bcy.log_duplicates()

    ############################## NODES ####################################

    def write_nodes(self):
        """
        Write nodes to admin import csv files.
        """

        # get node labels from csv
        with open("data/node_labels.csv", "r") as f:
            # import to pandas dataframe
            node_labels = pd.read_csv(f)

        node_labels = [
            "GraphPublication",
            "GraphOrganism",
            "GraphExperiment",
        ]

        # Single labels other than Interactors
        for label in node_labels:
            with self.driver.session() as session:
                # writing of one type needs to be completed inside
                # this session
                session.read_transaction(
                    self._get_node_ids_and_write_batches_tx, label
                )

        # Interactors
        with self.driver.session() as session:
            # also writes edges from interactors to organisms
            session.read_transaction(
                self._get_interactor_ids_and_write_batches_tx
            )

        # Interaction/participant detection method
        with self.driver.session() as session:
            session.read_transaction(self._get_detection_method_nodes_tx)

    ## regular nodes ##

    def _get_node_ids_and_write_batches_tx(
        self,
        tx,
        label,
    ):
        """
        Write nodes to admin import csv files. Writer function needs to be
        performed inside the transaction. Write edges from interactors to
        organisms.
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

    def _write_nodes(self, id_batch, label):
        """
        Write nodes to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            label: label of the node type
        """

        def node_gen():
            with self.driver.session() as session:
                results = session.read_transaction(get_nodes_tx, id_batch)

                for res in results:
                    # TODO source
                    _id, _type = _process_node_id_and_type(res["n"], label)
                    _props = res["n"]
                    yield (_id, _type, _props)

        self.bcy.write_nodes(
            nodes=node_gen(),
        )

    ## interactors ##

    def _get_interactor_ids_and_write_batches_tx(
        self,
        tx,
    ):
        """
        Write nodes to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(f"MATCH (n:GraphInteractor) " "RETURN id(n) as id")

        id_batch = []
        for record in result:
            # collect in batches
            id_batch.append(record["id"])
            if len(id_batch) == self.id_batch_size:
                # if full batch, trigger write process
                self._write_interactors(id_batch, "GraphInteractor")
                id_batch = []

            # check if result depleted
            elif result.peek() is None:
                # write last batch
                self._write_interactors(id_batch, "GraphInteractor")

    def _write_interactors(self, id_batch, label):
        """
        Write interactor nodes to admin import csv files. Also write
        interactor to organism edges. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of node ids to write

            label: label of the node type
        """

        nodes = []
        edges = []

        with self.driver.session() as session:
            results = session.read_transaction(
                get_interactor_to_organism_edges_tx, id_batch
            )

            for res in results:
                typ = res["typ"]
                src = res["src"]

                (
                    _interactor_id,
                    _interactor_type,
                ) = _process_node_id_and_type(res["n"], typ or label, src)

                _interactor_props = res["n"]
                _interactor_props["type"] = typ
                _interactor_props["source"] = src

                nodes.append(
                    (_interactor_id, _interactor_type, _interactor_props)
                )

                if res.get("o"):
                    _organism_id, _ = _process_node_id_and_type(
                        res["o"], "GraphOrganism"
                    )

                    _interaction_type = "INTERACTOR_TO_ORGANISM"
                    _interaction_props = {}

                    edges.append(
                        (
                            None,
                            _interactor_id,
                            _organism_id,
                            _interaction_type,
                            _interaction_props,
                        )
                    )
                else:
                    logger.debug(
                        f"No organism found for interactor {_interactor_props}"
                    )

        self.bcy.write_nodes(
            nodes=nodes,
        )

        self.bcy.write_edges(
            edges=edges,
        )

    ## detection method nodes ##

    def _get_detection_method_nodes_tx(
        self,
        tx,
    ):
        """
        Write nodes to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(
            "MATCH ()-[:interactionDetectionMethod]->(idm:GraphCvTerm) "
            "WITH DISTINCT idm LIMIT 100 "
            "RETURN idm.ac as ac, idm.shortName as shortName, "
            "idm.fullName as fullName, idm.mIIdentifier as mIIdentifier"
        )
        # need to do this because the distinct returns a "Node" object instead
        # of a dict and I don't know how to convert it to one.

        det_nodes = []

        for res in result:
            _detection_props = {
                "ac": res["ac"],
                "shortName": res["shortName"],
                "fullName": res["fullName"],
                "mIIdentifier": res["mIIdentifier"],
            }

            _detection_id, _detection_type = _process_node_id_and_type(
                _detection_props, "GraphEvidenceType"
            )

            det_nodes.append((_detection_id, _detection_type, _detection_props))

        self.bcy.write_nodes(
            nodes=det_nodes,
        )

    ############################## EDGES ####################################

    def write_edges(self) -> None:
        """
        Write edges to admin import csv files.
        """

        # dedicated function for binary interactions
        with self.driver.session() as session:
            # writing of one type needs to be completed inside
            # this session
            session.read_transaction(
                self._get_binary_interaction_ids_and_write_batches_tx
            )

    def _get_binary_interaction_ids_and_write_batches_tx(self, tx):
        """
        Write edges to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(
            f"MATCH (n:GraphBinaryInteractionEvidence) "
            "RETURN id(n) as id"
            " LIMIT 100000"
        )

        id_batch = []
        for record in result:
            # collect in batches
            id_batch.append(record["id"])
            if len(id_batch) == self.id_batch_size:
                # if full batch, trigger write process
                self._write_binary_interactions(id_batch)
                id_batch = []

            # check if result depleted
            elif result.peek() is None:
                # write last batch
                self._write_binary_interactions(id_batch)

    def _write_binary_interactions(self, id_batch):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

        """

        # TODO: IntAct interaction IDs refer to multiple binary interactions;
        # as is, nodes connected to multiple targets will have multiple edges
        # to the same interaction node. What is the biological meaning behind
        # this? Complexes, experiments, etc.?

        # TODO: separate query into smaller ones? (eg primary and experiment)

        with self.driver.session() as session:
            results = session.read_transaction(get_bin_int_rels_tx, id_batch)

            # main interaction edges
            int_edges = []
            # experiment edges
            bin_edges = []
            pub_edges = []
            org_edges = []
            det_edges = []
            int_det_edges = []

            for res in results:
                # TODO role -> relationship type

                # Barrio-Hernandez et al. use only reactome, intact, and signor
                # optional filter here; could also be done in the query
                if res["source"] not in ["reactome", "intact", "signor"]:
                    continue

                # extract relevant ids
                _id = res["n"].get("ac")
                # seems like all protein-protein interactions at
                # least have an EBI identifier; however, these IDs
                # are not unique to each pairwise interaction
                if not _id:
                    logger.debug(
                        "No id found for binary interaction evidence: " f"{res}"
                    )

                ## primary interaction edge
                if not (res.get("a") and res.get("b")):
                    logger.debug(
                        "No interactors found for binary interaction evidence: "
                        f"{res}"
                    )
                    continue

                # account for self-interactions, use same id for both if one
                # does not exist
                _src_id, _ = (
                    _process_node_id_and_type(
                        res["a"], res["typ_a"], res["src_a"]
                    )
                    if res.get("a")
                    else _process_node_id_and_type(
                        res["b"], res["typ_b"], res["src_b"]
                    )
                )
                _tar_id, _ = (
                    _process_node_id_and_type(
                        res["b"], res["typ_b"], res["src_b"]
                    )
                    if res.get("b")
                    else _process_node_id_and_type(
                        res["a"], res["typ_a"], res["src_a"]
                    )
                )

                _type = res["nt"].get("shortName")

                # properties of BinaryInteractionEvidence
                _props = res["n"]

                # add interactionType properties (redundant, should
                # later be encoded in labels)
                _props["interactionTypeShortName"] = res["nt"].get("shortName")
                _props["interactionTypeFullName"] = res["nt"].get("fullName")
                _props["interactionTypeIdentifierStr"] = res["nt"].get(
                    "mIIdentifier"
                )

                _props["mi_score"] = res["mi_score"]
                _props["source"] = res["source"]

                _props["expansion"] = res["expansion"]
                _props["expansion_id"] = res["expansion_id"]

                # TODO pass roles of a and b: is there a smarter way to do
                # this?
                _props["src_role"] = res["role_a"]
                _props["tar_role"] = res["role_b"]

                int_edges.append((_id, _src_id, _tar_id, _type, _props))

                ## experiment edges
                _experiment_id, _ = _process_node_id_and_type(
                    res["e"], "GraphExperiment"
                )

                # edges to binary interaction evidence
                _interaction_type = "INTERACTION_TO_EXPERIMENT"
                _interaction_props = {}

                bin_edges.append(
                    (
                        None,
                        _id,
                        _experiment_id,
                        _interaction_type,
                        _interaction_props,
                    )
                )

                # edges to publications
                if res.get("p"):
                    _publication_id, _ = _process_node_id_and_type(
                        res["p"], "GraphPublication"
                    )

                    _pub_edge_type = "EXPERIMENT_TO_PUBLICATION"
                    _pub_edge_props = {}

                    pub_edges.append(
                        (
                            None,
                            _experiment_id,
                            _publication_id,
                            _pub_edge_type,
                            _pub_edge_props,
                        )
                    )

                # edges to organisms
                if res.get("o"):
                    _organism_id, _ = _process_node_id_and_type(
                        res["o"], "GraphOrganism"
                    )

                    _org_edge_type = "EXPERIMENT_TO_ORGANISM"
                    _org_edge_props = {}

                    org_edges.append(
                        (
                            None,
                            _experiment_id,
                            _organism_id,
                            _org_edge_type,
                            _org_edge_props,
                        )
                    )

                # detection method edges to participants
                if res.get("idm_a") and res.get("idm_b"):
                    _int_det_edge_type = "PARTICIPANT_DETECTION_METHOD"
                    _int_det_edge_props_a = res["idm_a"]
                    _int_det_edge_props_b = res["idm_b"]

                    int_det_edges.append(
                        (
                            None,
                            _experiment_id,
                            _src_id,
                            _int_det_edge_type,
                            _int_det_edge_props_a,
                        )
                    )
                    int_det_edges.append(
                        (
                            None,
                            _experiment_id,
                            _tar_id,
                            _int_det_edge_type,
                            _int_det_edge_props_b,
                        )
                    )

                # edges to detection methods and nodes
                if res.get("d"):
                    _detection_id, _ = _process_node_id_and_type(
                        res["d"], "GraphEvidenceType"
                    )

                    _det_edge_type = "EXPERIMENT_TO_DETECTION_METHOD"
                    _det_edge_props = {}

                    det_edges.append(
                        (
                            None,
                            _experiment_id,
                            _detection_id,
                            _det_edge_type,
                            _det_edge_props,
                        )
                    )

        # finally, write
        for edge_set in [
            int_edges,
            bin_edges,
            pub_edges,
            org_edges,
            det_edges,
            int_det_edges,
        ]:
            self.bcy.write_edges(
                edge_set,
            )
