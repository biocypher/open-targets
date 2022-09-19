import re

from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


def _process_node_id_and_type(
    _node: dict, _type: str, _source: str = None
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
            _id = "ensembl:" + _pref_id
            _type = "ensembl_dna"

        elif _source == "reactome" and reactome_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
            _id = "ensembl:" + _pref_id
            _type = "ensembl_protein"

        else:
            logger.debug(f"Encountered {_type}, {_node}, {_source}")

    # double stranded deoxyribonucleic acid,ds dna
    elif _type == "ds dna":

        if _source == "intact" and ebi_prefix_pattern.match(_pref_id):
            _id = "intact:" + _pref_id
            _type = "intact_dsdna"

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        if _source == "complex portal" and complexportal_prefix_pattern.match(
            _pref_id
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

        elif _source == "reactome" and reactome_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
            _id = "ensembl:" + _pref_id
            _type = "ensembl_mirna"

        elif _source == "mirbase" and mirbase_precursor_prefix_pattern.match(
            _pref_id
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

        elif _source == "complexportal" and complexportal_prefix_pattern.match(
            _pref_id
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        elif _source == "ensembl" and ensembl_prefix_pattern.match(_pref_id):
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

        if _source == "reactome" and reactome_prefix_pattern.match(_pref_id):
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
