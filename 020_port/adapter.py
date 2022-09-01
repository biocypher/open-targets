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

        # indicator of information loss (dict of lists)
        self.information_loss = {}

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
            # "GraphInteractor",
            # "GraphPublication",
            "GraphBinaryInteractionEvidence",
        ]

        # Interactors
        with self.driver.session() as session:
            # writing of one type needs to be completed inside
            # this session
            session.read_transaction(
                self._get_interactor_ids_and_write_batches_tx,
                "GraphInteractor",
            )

        for label in node_labels:
            with self.driver.session() as session:
                # writing of one type needs to be completed inside
                # this session
                session.read_transaction(
                    self._get_node_ids_and_write_batches_tx, label
                )

        if self.translation_needed:
            logger.warning("At least one node data type requires translation.")

        if self.information_loss:
            logger.warning(
                "At least one node data type has information loss: "
                f"{self.information_loss}"
            )

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

        result = tx.run(f"MATCH (n:{label}) " "RETURN id(n) as id LIMIT 20")

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

    def _write_interactors(self, id_batch, label):
        """
        Write edges to admin import csv files. Needs to be performed in a
        transaction.

        Args:

            id_batch: list of edge ids to write

            label: label of the node type
        """

        def node_gen():
            with self.driver.session() as session:
                results = session.read_transaction(
                    get_interactors_tx, id_batch
                )

                for res in results:

                    typ = res["typ"]
                    src = res["src"]

                    _id, _type = self._process_node_id_and_type(
                        res["n"], typ or label, src
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

    def _process_node_id_and_type(self, _node, _type, _source=None):
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
        hgnc_prefix_pattern = re.compile("^HGNC:")
        intact_mint_prefix_pattern = re.compile("^MINT-")
        signor_prefix_pattern = re.compile("^SIGNOR-")
        reactome_prefix_pattern = re.compile("^R-[A-Z]{3}-\d+(-\d+)?(\.\d+)?$")
        uniprot_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?$"
        )
        uniprot_hyphenated_prefix_pattern = re.compile(
            "^([A-N,R-Z][0-9]([A-Z][A-Z, 0-9][A-Z, 0-9][0-9]){1,2})|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?"
        )  # removed end of line character from regex to include proteins with hyphenated accessions
        ensembl_prefix_pattern = re.compile(
            "^((ENS[FPTG]\d{11}(\.\d+)?)|(FB\w{2}\d{7})|(Y[A-Z]{2}\d{3}[a-zA-Z](\-[A-Z])?)|([A-Z_a-z0-9]+(\.)?(t)?(\d+)?([a-z])?))$"
        )
        rnacentral_prefix_pattern = re.compile("^URS[0-9A-F]{10}(\_\d+)?$")
        uniprot_archive_prefix_pattern = re.compile("^UPI[A-F0-9]{10}$")
        dip_prefix_pattern = re.compile("^DIP(\:)?\-\d{1,}[ENXS]$")
        refseq_prefix_pattern = re.compile(
            "^(((AC|AP|NC|NG|NM|NP|NR|NT|NW|XM|XP|XR|YP|ZP)_\d+)|(NZ\_[A-Z]{2,4}\d+))(\.\d+)?$"
        )

        _id = None
        # strip whitespace
        _pref_id = _node.get("preferredIdentifierStr").strip()

        ## Interactor types given by graph:

        # deoxyribonucleic acid,dna
        if _type == "dna":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_dna"

            elif _source == "ddbj/embl/genbank":
                _id = "genbank:" + _pref_id
                _type = "genbank_dna"

            elif _source == "ensembl" and ensembl_prefix_pattern.match(
                _pref_id
            ):
                _id = "ensembl:" + _pref_id
                _type = "ensembl_dna"

            else:
                print(_type, _node)

        # double stranded ribonucleic acid,ds rna
        elif _type == "ds rna":
            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = _pref_id
                _type = "intact_dsrna"

            elif rnacentral_prefix_pattern.match(_pref_id):
                _id = _pref_id
                _type = "rnacentral_dsrna"
            else:
                print(_type, _node)

        # protein,protein
        elif _type == "protein":

            if _source == "uniprotkb" and uniprot_prefix_pattern.match(
                _pref_id
            ):
                _id = "uniprot:" + _node["uniprotName"]
                _type = "uniprot_protein"

            elif (
                _source == "uniprotkb"
                and uniprot_hyphenated_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                )
            ):
                # split id at hyphen and use only first part
                _id = _pref_id.split("-")[0]
                _type = "uniprot_protein"
                logger.debug(
                    f"Added protein {_id} from {_node['preferredIdentifierStr']}. "
                    "Information may be lost."
                )
                if not self.information_loss.get(_type):
                    self.information_loss[_type] = 1
                else:
                    self.information_loss[_type] += 1

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

            else:
                print(_type, _node)

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

            else:
                print(_type, _node)

        # single stranded deoxyribonucleic acid,ss dna
        elif _type == "ss dna":

            if ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_ssdna"

            elif _source in ["genbank_nucl_gi", "ddbj/embl/genbank"]:
                _id = "genbank:" + _pref_id
                _type = "genbank_ssdna"

            else:
                print(_type, _node)

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
                print(_type, _node)

        # small nucleolar rna,snorna
        elif _type == "snorna":

            if _source == "rnacentral" and rnacentral_prefix_pattern.match(
                _pref_id
            ):
                _id = "rnacentral:" + _pref_id

            else:
                print(_type, _node)

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
                print(_type, _node)

        # xenobiotic,xenobiotic
        elif _type == "xenobiotic":
            print(_type, _node)

        # poly adenine,poly a
        elif _type == "poly a":
            print(_type, _node)

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

            else:
                print(_type, _node)

        # gene,gene
        elif _type == "gene":
            _id = "exac.gene:" + _pref_id

        # phenotype,phenotype
        elif _type == "phenotype":
            print(_type, _node)

        # stable complex,stable complex
        elif _type == "stable complex":
            _id = "complexportal:" + _pref_id

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
                print(_type, _node)

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
                    print(_type, _node)

            else:
                print(_type, _node)

        # small molecule,small molecule
        elif _type == "small molecule":

            if _source == "chebi":

                if chebi_no_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "chebi:" + _pref_id

                elif chebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

            elif _source == "intact" and ebi_prefix_pattern.match(
                _node.get("preferredIdentifierStr")
            ):
                _id = _pref_id
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True

            elif cid_prefix_pattern.match(_node.get("preferredIdentifierStr")):
                _id = _pref_id
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True

            elif sid_prefix_pattern.match(_node.get("preferredIdentifierStr")):
                _id = _pref_id
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True

            elif _source == "chembl" and chembl_prefix_pattern.match(
                _node.get("preferredIdentifierStr")
            ):
                _id = _pref_id
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True

            else:
                print(_type, _node)

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

            else:
                print(_type, _node)

        # molecule set,molecule set
        elif _type == "molecule set":

            if _source == "intact":
                _id = "intact:" + _pref_id
                _type = "intact_molecule_set"

            elif _source == "uniprotkb":
                _id = "uniprot:" + _pref_id
                _type = "uniprot_molecule_set"

            else:
                print(_type, _node)

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

            else:
                print(_type, _node)

        # stimulus,stimulus
        elif _type == "stimulus":
            print(_type, _node)

        # peptide,peptide
        elif _type == "peptide":

            if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
                _id = "intact:" + _pref_id
                _type = "intact_peptide"

            elif _source == "dip" and dip_prefix_pattern.match(_pref_id):
                _id = "dip:" + _pref_id
                _type = "dip_peptide"

        # complex,complex
        elif _type == "complex":
            _id = "complexportal:" + _pref_id

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
                print(_type, _node)

        # bioactive entity,bioactive entity
        # only three in the graph, all have CHEBI ids
        elif _type == "bioactive entity":

            if _source == "chebi":

                if chebi_prefix_pattern.match(_pref_id):
                    _id = _pref_id.replace("CHEBI:", "chebi:")

                elif chebi_no_prefix_pattern.match(_pref_id):
                    _id = "chebi:" + _pref_id

                else:
                    print(_type, _node)

                _type = "small molecule"

            else:
                print(_type, _node)

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

            else:
                print(_type, _node)

        # unknown participant,unknown participant
        elif _type == "unknown participant":
            print(_type, _node)

        if _type == "GraphInteractor":
            # any kind of interaction participant

            _prefix = _node["uniqueKey"]

            if "nucleic acid" in _prefix:
                if _node.get("ac"):
                    _id = "intact:" + _node["ac"]
                    _type = "intact:GraphNucleicAcid"
                elif reactome_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "reactome:" + _pref_id
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
                    _id = "chebi:" + _pref_id

                elif chebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = "chebi:" + _pref_id.replace("CHEBI:", "")

                elif ebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif cid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif sid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif chembl_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                else:
                    print(_type, _node)

                _type = "GraphSmallMolecule"

            elif "polymer" in _prefix:
                # there is one small nuclear RNA with this prefix in the DB
                # however, it has NCBI id instead of ENSEMBL
                logger.debug(
                    f"Translation necessary for {_node['preferredIdentifierStr']}"
                )
                self.translation_needed = True
                _type = "GraphPolymer"

            elif "complex" in _prefix:
                _id = "complexportal:" + _pref_id
                _type = "GraphComplex"

            else:
                # generic interactor, but can include prefixes used above
                # prefixes included:
                # "CID:", "CHEBI:", "SIGNOR-", "R-", "EBI-", or uniprot

                if cid_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif chebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif signor_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif reactome_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif ebi_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                elif uniprot_prefix_pattern.match(
                    _node.get("preferredIdentifierStr")
                ):
                    _id = _pref_id
                    _type = "GraphProtein"
                    logger.debug(
                        f"Translation necessary for {_node['preferredIdentifierStr']}"
                    )
                    self.translation_needed = True

                else:
                    print(
                        "Erroneous "
                        + _type
                        + " =============================="
                    )
                    print(_node)

        elif _type == "GraphPublication":
            if _node.get("pubmedIdStr"):
                _id = "pubmed:" + _node["pubmedIdStr"]
            else:
                print("Erroneous " + _type + " ==============================")
                print(_node)

        elif _type == "GraphBinaryInteractionEvidence":
            if _node.get("imexId"):
                _id = "uk:" + _node["uniqueKey"]
            elif _node.get("ac"):
                _id = "uk:" + _node["uniqueKey"]
            else:
                print(_node)

        return _id, _type


def get_nodes_tx(tx, ids):
    result = tx.run(
        "MATCH (n) " "WHERE id(n) IN {ids} " "RETURN n",
        ids=ids,
    )
    return result.data()


def get_interactors_tx(tx, ids):
    result = tx.run(
        "MATCH (n) "
        "WHERE id(n) IN {ids} "
        "WITH n "
        "MATCH (n)-[:interactorType]->(t), (n)-[:preferredIdentifier]->()-[:database]->(d) "
        "RETURN n, t.shortName AS typ, d.shortName as src",
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
