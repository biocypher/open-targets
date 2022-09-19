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
            skip_bad_relationships=True,
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

    def write_to_csv_for_admin_import(self):
        """
        Write nodes and edges to admin import csv files.
        """

        self.write_nodes()
        self.write_edges()
        self.bcy.write_import_call()
        self.bcy.log_missing_bl_types()

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
            # "GraphInteractionDetectionMethod",
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
            # writing of one type needs to be completed inside
            # this session
            session.read_transaction(
                self._get_interactor_ids_and_write_batches_tx,
                "GraphInteractor",
            )

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

    def _get_interactor_ids_and_write_batches_tx(
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
                self._write_interactors(id_batch, label)
                id_batch = []

            # check if result depleted
            elif result.peek() is None:

                # write last batch
                self._write_interactors(id_batch, label)

    def _get_binary_interaction_ids_and_write_batches_tx(self, tx):
        """
        Write edges to admin import csv files. Writer function needs to be
        performed inside the transaction.
        """

        result = tx.run(
            f"MATCH (n:GraphBinaryInteractionEvidence) "
            "RETURN id(n) as id"
            # " LIMIT 1000"
        )

        id_batch = []
        for record in result:
            # collect in batches
            if len(id_batch) < self.id_batch_size:
                id_batch.append(record["id"])

                # check if result depleted
                if result.peek() is None:
                    # write last batch
                    self._write_bin_int_edges(id_batch)

            # if full batch, trigger write process
            else:
                self._write_bin_int_edges(id_batch)
                id_batch = []

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
                    _id, _type = self._process_node_id_and_type(
                        res["n"], label
                    )
                    _props = res["n"]
                    yield (_id, _type, _props)

        self.bcy.write_nodes(
            nodes=node_gen(),
            db_name=self.db_name,
        )

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
                ) = self._process_node_id_and_type(res["n"], typ or label, src)

                _interactor_props = res["n"]

                nodes.append(
                    (_interactor_id, _interactor_type, _interactor_props)
                )

                if res.get("o"):
                    _organism_id, _ = self._process_node_id_and_type(
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
            db_name=self.db_name,
        )

        self.bcy.write_edges(
            edges=edges,
            db_name=self.db_name,
        )

    def _write_bin_int_edges(self, id_batch):
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

        def edge_gen():
            with self.driver.session() as session:
                results = session.read_transaction(
                    get_bin_int_rels_tx, id_batch
                )

                for res in results:
                    # TODO role -> relationship type

                    # extract relevant ids
                    _id = res["n"].get("ac")
                    # seems like all protein-protein interactions at
                    # least have an EBI identifier; however, these IDs
                    # are not unique to each pairwise interaction
                    if not _id:
                        logger.debug(
                            "No id found for binary interaction evidence: "
                            f"{res}"
                        )

                    ## primary interaction edge

                    # also carrying ac: efo, rcsb pdb, wwpdb
                    _src_id, _src_type = self._process_node_id_and_type(
                        res["a"], res["typ_a"], res["src_a"]
                    )
                    _tar_id, _tar_type = self._process_node_id_and_type(
                        res["b"], res["typ_b"], res["src_b"]
                    )

                    _source = res["source"]

                    # subtypes according to the type of association
                    # _type = "_".join(
                    #     [
                    #         res["typ_a"],
                    #         res["typ_b"],
                    #         _source,
                    #         res["nt"].get("shortName"),
                    #     ]
                    # )
                    _type = res["nt"].get("shortName")

                    # properties of BinaryInteractionEvidence
                    _props = res["n"]
                    # add interactionType properties (redundant, should
                    # later be encoded in labels)
                    _props["interactionTypeShortName"] = res["nt"].get(
                        "shortName"
                    )
                    _props["interactionTypeFullName"] = res["nt"].get(
                        "fullName"
                    )
                    _props["interactionTypeIdentifierStr"] = res["nt"].get(
                        "mIIdentifier"
                    )

                    _props["organism"]

                    # pass roles of a and b: is there a smarter way to do this?
                    _props["src_role"] = res["role_a"]
                    _props["tar_role"] = res["role_b"]

                    yield (_id, _src_id, _tar_id, _type, _props)

        self.bcy.write_edges(
            edges=edge_gen(),
            db_name=self.db_name,
        )

    def _process_node_id_and_type(
        self, _node: dict, _type: str, _source: str = None
    ) -> tuple:
        """
        Add prefixes to avoid multiple assignment.

        Split up nodes in case of Protein (includes Peptides).

        TODO pull regex safeguarding into BioCypher dataclasses

        TODO python 3.10: use patterns instead of elif chains
        """

        # regex patterns
        ebi_prefix_pattern = re.compile("^EBI-")
        cid_prefix_pattern = re.compile("^CID:")
        sid_prefix_pattern = re.compile("^SID:")
        hgnc_prefix_pattern = re.compile("^HGNC:")
        chebi_prefix_pattern = re.compile("^CHEBI:")
        chembl_prefix_pattern = re.compile("^CHEMBL")
        signor_prefix_pattern = re.compile("^SIGNOR-")
        chebi_no_prefix_pattern = re.compile("^\d{,6}$")
        drugbank_prefix_pattern = re.compile("^DB\d{5}$")
        intact_mint_prefix_pattern = re.compile("^MINT-")
        chembl_no_prefix_pattern = re.compile("^\d{,10}$")
        complexportal_prefix_pattern = re.compile("^CPX-[0-9]+$")
        mirbase_precursor_prefix_pattern = re.compile("^MI\d{7}$")
        dip_prefix_pattern = re.compile("^DIP(\:)?\-\d{1,}[ENXS]$")
        uniprot_archive_prefix_pattern = re.compile("^UPI[A-F0-9]{10}$")
        rnacentral_prefix_pattern = re.compile("^URS[0-9A-F]{10}(\_\d+)?$")
        reactome_prefix_pattern = re.compile("^R-[A-Z]{3}-\d+(-\d+)?(\.\d+)?$")
        uniprot_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?$"
        )
        uniprot_wrong_precursor_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?_PRO_\d+$"
        )
        # hyphen replaced by underscore, unify (TODO how to resolve? synonym?)
        uniprot_precursor_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?-PRO_\d+$"
        )
        # TODO uniprot.chain is only the "PRO-.." part, not the whole id
        uniprot_isoform_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?-\d+$"
        )
        ensembl_prefix_pattern = re.compile(
            "^((ENS[FPTG]\d{11}(\.\d+)?)|(FB\w{2}\d{7})|(Y[A-Z]{2}\d{3}[a-zA-Z](\-[A-Z])?)|([A-Z_a-z0-9]+(\.)?(t)?(\d+)?([a-z])?))$"
        )
        refseq_prefix_pattern = re.compile(
            "^(((AC|AP|NC|NG|NM|NP|NR|NT|NW|WP|XM|XP|XR|YP|ZP)_\d+)|(NZ\_[A-Z]{2,4}\d+))(\.\d+)?$"
        )

        _id = None
        # strip whitespace
        if _node.get("preferredIdentifierStr"):
            _pref_id = _node.get("preferredIdentifierStr").strip()

        ## Interactor types given by graph:

        # deoxyribonucleic acid,dna
        if _type == "dna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_dna"

            elif _source in ["ddbj/embl/genbank", "genbank identifier"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_dna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_dna"

            elif _source == "reactome" and reactome_prefix_pattern.match(
                _pref_id
            ):
                _id = "reactome:" + _pref_id
                _type = "reactome_dna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_dna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # double stranded ribonucleic acid,ds rna
        elif _type == "ds rna":
            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = _pref_id
                _type = "intact_dsrna"

            elif rnacentral_prefix_pattern.match(_pref_id):
                _id = _pref_id
                _type = "rnacentral_dsrna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_dsrna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # protein,protein
        elif _type == "protein":

            if _source == "uniprotkb":

                if uniprot_prefix_pattern.match(_pref_id):
                    _id = "uniprot:" + _node["uniprotName"]
                    _type = "uniprot_protein"

                elif uniprot_isoform_prefix_pattern.match(_pref_id):
                    _id = "uniprot:" + _node["uniprotName"]
                    _type = "uniprot_protein_isoform"

                elif uniprot_precursor_prefix_pattern.match(_pref_id):
                    _id = _pref_id
                    _type = "uniprot_protein_precursor"

                elif drugbank_prefix_pattern.match(_pref_id):
                    # TODO interesting case: biologicals are both proteins and drugs
                    _id = "drugbank:" + _pref_id
                    _type = "drugbank_protein"

                elif mirbase_precursor_prefix_pattern.match(_pref_id):
                    # TODO another interesting case: plain wrong assignment
                    # TODO precursor vs mature
                    _id = "mirbase:" + _pref_id
                    _type = "mirbase_mirna"

                elif uniprot_wrong_precursor_prefix_pattern.match(_pref_id):
                    # TODO resolve mapping/synonym with Signor?
                    _id = _pref_id.replace("_PRO", "-PRO")
                    _type = "uniprot_protein_precursor"

                elif _pref_id == "P17861_P17861-2":
                    # TODO resolve mapping/synonym with Signor?
                    _pref_id = "uniprot:P17861-2"
                    _type = "uniprot_protein_isoform"
                    _node["uniprotName"] = "P17861-2"

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            elif _source == "chembl compound":
                # TODO same as above - biologicals are both proteins and drugs

                if chembl_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEMBL", "chembl:")
                    _type = "chembl_protein"

                elif chembl_no_prefix_pattern.match(_pref_id):
                    _id = "chembl:" + _pref_id
                    _type = "chembl_protein"

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            elif _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_protein"

            elif _source == "intact" and intact_mint_prefix_pattern.match(
                _pref_id
            ):
                _id = "intact:" + _pref_id
                _type = "intact_protein"

            elif _source == "uniparc" and uniprot_archive_prefix_pattern.match(
                _pref_id
            ):
                _id = "uniparc:" + _pref_id
                _type = "uniprot_archive_protein"

            elif _source == "entrezgene/locuslink":
                _id = "ncbigene:" + _pref_id
                _type = "entrez_protein"

            elif _source in [
                "genbank_protein_gi",
                "genbank identifier",
                "ddbj/embl/genbank",
                "genbank_nucl_gi",  # why is this in protein?
            ]:
                _id = "genbank:" + _pref_id
                _type = "genbank_protein"

            elif _source == "dip" and dip_prefix_pattern.match(_pref_id):
                _id = "dip:" + _pref_id
                _type = "dip_protein"

            elif _source == "ipi":
                _id = "ipi:" + _pref_id
                _type = "ipi_protein"
                logger.warning("Legacy database IPI used.")

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_protein"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_protein"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # double stranded deoxyribonucleic acid,ds dna
        elif _type == "ds dna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_dsdna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_dsdna"

            elif uniprot_archive_prefix_pattern.match(_pref_id):
                _id = "uniparc:" + _pref_id
                _type = "uniprot_archive_dsdna"

            elif _source == "ddbj/embl/genbank":
                _id = "genbank:" + _pref_id
                _type = "genbank_dsdna"

            elif _source == "pubmed":
                _id = "pubmed:" + _pref_id
                _type = "pubmed_dsdna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_dsdna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # single stranded deoxyribonucleic acid,ss dna
        elif _type == "ss dna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_ssdna"

            elif _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chebi_ssdna"

            elif _source in ["genbank_nucl_gi", "ddbj/embl/genbank"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_ssdna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_ssdna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # small nuclear rna,snrna
        elif _type == "snrna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_snrna"

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_snrna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_snrna"

            elif _source == "ddbj/embl/genbank":
                _id = "genbank:" + _pref_id
                _type = "genbank_snrna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # small nucleolar rna,snorna
        elif _type == "snorna":

            if _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # long non-coding ribonucleic acid,lncrna
        elif _type == "lncrna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_lncrna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_lncrna"

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_lncrna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_lncrna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # xenobiotic,xenobiotic
        elif _type == "xenobiotic":

            if _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chebi_xenobiotic"

            elif _source == "pubchem":
                if cid_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CID:", "pubchem.compound:")
                    _type = "pubchem_xenobiotic"

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # poly adenine,poly a
        elif _type == "poly a":

            if _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chebi_poly_a"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # ribosomal rna,rrna
        elif _type == "rrna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_rrna"

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_rrna"

            elif _source == "ddbj/embl/genbank":
                _id = "genbank:" + _pref_id
                _type = "genbank_rrna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_rrna"

            elif _source == "entrezgene/locuslink":
                _id = "ncbigene:" + _pref_id
                _type = "entrez_rrna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # gene,gene
        elif _type == "gene":
            _id = "exac.gene:" + _pref_id

        # phenotype,phenotype
        elif _type == "phenotype":

            if _source == "signor" and signor_prefix_pattern.match(_pref_id):
                _id = "signor:" + _pref_id
                _type = "signor_phenotype"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # stable complex,stable complex
        elif _type == "stable complex":

            if (
                _source == "complex portal"
                and complexportal_prefix_pattern.match(_pref_id)
            ):
                _id = "complexportal:" + _pref_id
                _type = "complexportal_stable_complex"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # guide rna,grna
        elif _type == "grna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_grna"

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_grna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # messenger rna,mrna
        elif _type == "mrna":

            if _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_mrna"

            elif _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_mrna"

            elif _source in ["ddbj/embl/genbank", "genbank identifier"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_mrna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_mrna"

            elif _source == "hgnc":
                if hgnc_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("HGNC:", "hgnc:")
                    _type = "hgnc_mrna"
                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # small molecule,small molecule
        elif _type == "small molecule":

            if _source == "chebi":

                if chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                elif chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chebi_small_molecule"

            elif _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = _pref_id
                _type = "intact_small_molecule"

            elif _source == "pubchem":

                if cid_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CID:", "pubchem.compound:")
                    _type = "pubchem_compound"

                elif sid_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("SID:", "pubchem.substance:")
                    _type = "pubchem_substance"

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            elif _source == "chembl":

                if chembl_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEMBL", "chembl:")

                elif chembl_no_prefix_pattern.match(_pref_id):
                    _id = "chembl:" + _pref_id

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chembl_small_molecule"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # ribonucleic acid,rna
        elif _type == "rna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_rna"

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_rna"

            elif _source == "reactome" and reactome_prefix_pattern.match(
                _pref_id
            ):
                # TODO there are mirnas in there
                _id = "reactome:" + _pref_id
                _type = "reactome_rna"

            elif _source in ["genbank_nucl_gi", "ddbj/embl/genbank"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_rna"

            elif _source == "entrezgene/locuslink":
                _id = "ncbigene:" + _pref_id
                _type = "entrez_rna"

            elif _source == "refseq" and refseq_prefix_pattern.match(_pref_id):
                _id = "refseq:" + _pref_id
                _type = "refseq_rna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_rna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # molecule set,molecule set
        elif _type == "molecule set":

            if _source == "intact":
                _id = "intact:" + _pref_id
                _type = "intact_molecule_set"

            elif _source == "uniprotkb":
                _id = "uniprot:" + _pref_id
                _type = "uniprot_molecule_set"

            elif _source == "signor" and signor_prefix_pattern.match(_pref_id):
                _id = "signor:" + _pref_id
                _type = "signor_molecule_set"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # micro rna,mirna
        elif _type == "mirna":
            # TODO primary, pre, mature

            if _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_mirna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_mirna"

            elif (
                _source == "mirbase"
                and mirbase_precursor_prefix_pattern.match(_pref_id)
            ):
                _id = "mirbase:" + _pref_id
                _type = "mirbase_mirna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # stimulus,stimulus
        elif _type == "stimulus":

            if _source == "signor" and signor_prefix_pattern.match(_pref_id):
                _id = "signor:" + _pref_id
                _type = "signor_stimulus"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # peptide,peptide
        elif _type == "peptide":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_peptide"

            elif _source == "intact" and intact_mint_prefix_pattern.match(
                _pref_id
            ):
                _id = "intact:" + _pref_id
                _type = "intact_peptide"

            elif _source == "dip" and dip_prefix_pattern.match(_pref_id):
                _id = "dip:" + _pref_id
                _type = "dip_peptide"

            elif _source == "uniprotkb":

                if uniprot_prefix_pattern.match(_pref_id):
                    _id = "uniprot:" + _pref_id
                    _type = "uniprot_peptide"

                elif uniprot_precursor_prefix_pattern.match(_pref_id):
                    _id = "uniprot:" + _pref_id
                    _type = "uniprot_peptide_precursor"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # complex,complex
        elif _type == "complex":

            if _source == "signor" and signor_prefix_pattern.match(_pref_id):
                _id = "signor:" + _pref_id
                _type = "signor_complex"

            elif (
                _source == "complexportal"
                and complexportal_prefix_pattern.match(_pref_id)
            ):
                _id = "complexportal:" + _pref_id
                _type = "complexportal_complex"

            elif _source == "complexportal" and signor_prefix_pattern.match(
                _pref_id
            ):
                # probably wrongly assigned
                _id = "signor:" + _pref_id
                _type = "signor_complex"

            elif _node.get("preferredName") == "CLOCK/ARNTL2":
                # TODO manually corrected; should be fixed in the source
                # complexportal refers to CLOCK/BMAL2
                # only correcting id here, not name
                _id = "complexportal:CPX-3230"
                _type = "complexportal_complex"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # nucleic acid,nucleic acid
        elif _type == "nucleic acid":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_nucleic_acid"

            elif _source in ["ddbj/embl/genbank", "genbank identifier"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_nucleic_acid"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_nucleic_acid"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # bioactive entity,bioactive entity
        # only three in the graph, all have CHEBI ids
        elif _type == "bioactive entity":

            if _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

                _type = "chebi_small_molecule"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # transfer rna,trna
        elif _type == "trna":

            if _source == "ddbj/embl/genbank":
                _id = "genbank:" + _pref_id
                _type = "genbank_trna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_trna"

            elif _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")
                    _type = "chebi_trna"

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id
                    _type = "chebi_trna"

                else:
                    logger.debug(f"Encountered {_type}, {_node}, {_source}")

            elif _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id
                _type = "rnacentral_trna"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        # unknown participant,unknown participant
        elif _type == "unknown participant":
            # can be many things, from individual species to concepts
            # many have reactome IDs, some Signor
            # cast to BiologicalEntity

            if _source == "reactome" and reactome_prefix_pattern.match(
                _pref_id
            ):
                _id = "reactome:" + _pref_id
                _type = "reactome_unknown_participant"

            elif _source == "signor" and signor_prefix_pattern.match(_pref_id):
                _id = "signor:" + _pref_id
                _type = "signor_unknown_participant"

            else:
                logger.debug(f"Encountered {_type}, {_node}, {_source}")

        elif _type == "GraphPublication":
            if _node.get("pubmedIdStr"):
                _id = "pubmed:" + _node["pubmedIdStr"]
            else:
                print("Erroneous " + _type + " ==============================")
                print(_node)

        elif _type == "GraphOrganism":
            # need to resort to uniqueKeys because none of the others is
            # unique
            _id = _node.get("uniqueKey")

        return _id, _type


### TRANSACTIONS ###


def get_nodes_tx(tx, ids):
    result = tx.run(
        "MATCH (n) " "WHERE id(n) IN {ids} " "RETURN n",
        ids=ids,
    )
    return result.data()


def get_interactor_to_organism_edges_tx(tx, ids):
    result = tx.run(
        "MATCH (n) "
        "WHERE id(n) IN {ids} "
        "WITH n "
        "MATCH (n)-[:interactorType]->(t)"
        "OPTIONAL MATCH (n)-[:organism]->(o:GraphOrganism) "
        "OPTIONAL MATCH (n)-[:preferredIdentifier]->()-[:database]->(d) "
        "RETURN n, o, t.shortName as typ, d.shortName AS src",
        ids=ids,
    )
    return result.data()


def get_bin_int_rels_tx(tx, ids):
    result = tx.run(
        "MATCH (n) "
        "WHERE id(n) IN {ids} "
        "WITH n "
        "MATCH (bt:GraphCvTerm)<-[:interactorType]-(b:GraphInteractor)<-[:interactorB]-(n)-[:interactorA]->(a:GraphInteractor)-[:interactorType]->(at:GraphCvTerm) "
        "OPTIONAL MATCH (n)-[:interactionType]->(nt:GraphCvTerm) "
        "WITH n, a, b, nt, at, bt "
        "MATCH (n)-[:identifiers]->(:GraphXref)-[:database]->(nd:GraphCvTerm) "
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTA]->(pa:GraphEntity)-[:biologicalRole]->(ar:GraphCvTerm)"
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTB]->(pb:GraphEntity)-[:biologicalRole]->(br:GraphCvTerm)"
        "OPTIONAL MATCH (a)-[:preferredIdentifier]->(:GraphXref)-[:database]->(ad:GraphCvTerm) "
        "OPTIONAL MATCH (b)-[:preferredIdentifier]->(:GraphXref)-[:database]->(bd:GraphCvTerm) "
        "RETURN n, nd.shortName AS source, nt, "
        "a, ad.shortName AS src_a, at.shortName AS typ_a, ar.shortName AS role_a, "
        "b, bd.shortName AS src_b, bt.shortName AS typ_b, br.shortName AS role_b",
        ids=ids,
    )
    return result.data()
