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


# TODO why is there no ID field?
# TODO make role edge generic name


def get_bin_int_rels_tx(tx, ids):
    result = tx.run(
        "MATCH (n) " "WHERE id(n) IN {ids} " "WITH n "
        # get interactors
        "OPTIONAL MATCH (n)-[:interactorA]->(a:GraphInteractor)-[:interactorType]->(at:GraphCvTerm) "
        "OPTIONAL MATCH (n)-[:interactorB]->(b:GraphInteractor)-[:interactorType]->(bt:GraphCvTerm) "
        # get participants
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTA]->(ap:GraphEntity) "
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTB]->(bp:GraphEntity) "
        # get type of interaction
        "OPTIONAL MATCH (n)-[:interactionType]->(nt:GraphCvTerm) "
        # get experiment
        "OPTIONAL MATCH (n)-[:experiment]->(e:GraphExperiment) "
        # get expansion type
        "OPTIONAL MATCH (n)-[:complexExpansion]->(ce:GraphCvTerm) "
        # with
        "WITH n, a, b, nt, at, bt, ap, bp, e, ce "
        # get source
        "MATCH (n)-[:identifiers]->(:GraphXref)-[:database]->(nd:GraphCvTerm) "
        # get cluster
        "OPTIONAL MATCH (n)-[:interactions]-(nc:GraphClusteredInteraction) "
        # get biological role
        "OPTIONAL MATCH (ap)-[:biologicalRole]->(ar:GraphCvTerm) "
        "OPTIONAL MATCH (bp)-[:biologicalRole]->(br:GraphCvTerm) "
        # get interactor detection method
        "OPTIONAL MATCH (ap)-[:identificationMethods]->(idm_a:GraphCvTerm) "
        "OPTIONAL MATCH (bp)-[:identificationMethods]->(idm_b:GraphCvTerm) "
        # get sources of interactors
        "OPTIONAL MATCH (a)-[:preferredIdentifier]->(:GraphXref)-[:database]->(ad:GraphCvTerm) "
        "OPTIONAL MATCH (b)-[:preferredIdentifier]->(:GraphXref)-[:database]->(bd:GraphCvTerm) "
        # experiment associations
        "OPTIONAL MATCH (e)<-[:PUB_EXP]-(p:GraphPublication) "
        "OPTIONAL MATCH (e)-[:hostOrganism]->(o:GraphOrganism) "
        "OPTIONAL MATCH (e)-[:interactionDetectionMethod]->(d:GraphCvTerm) "
        # return
        "RETURN n, nd.shortName AS source, nt, nc.miscore AS mi_score, "
        "ce.shortName AS expansion, ce.mIIdentifier AS expansion_id, "
        "a, ad.shortName AS src_a, at.shortName AS typ_a, "
        "ar.shortName AS role_a, idm_a, "
        "b, bd.shortName AS src_b, bt.shortName AS typ_b, "
        "br.shortName AS role_b, idm_b, "
        "e, p, o, d",
        ids=ids,
    )
    return result.data()
