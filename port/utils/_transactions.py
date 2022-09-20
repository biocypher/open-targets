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
        "MATCH (n) " "WHERE id(n) IN {ids} " "WITH n "
        # get interactors
        "MATCH (bt:GraphCvTerm)<-[:interactorType]-(b:GraphInteractor)<-[:interactorB]-(n)-[:interactorA]->(a:GraphInteractor)-[:interactorType]->(at:GraphCvTerm) "
        # get type of interaction
        "OPTIONAL MATCH (n)-[:interactionType]->(nt:GraphCvTerm) "
        "WITH n, a, b, nt, at, bt "
        # get source
        "MATCH (n)-[:identifiers]->(:GraphXref)-[:database]->(nd:GraphCvTerm) "
        # get cluster
        "OPTIONAL MATCH (n)-[:interactions]-(nc:GraphClusteredInteraction) "
        # get biological role
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTA]->(pa:GraphEntity)-[:biologicalRole]->(ar:GraphCvTerm)"
        "OPTIONAL MATCH (n)-[:BIE_PARTICIPANTB]->(pb:GraphEntity)-[:biologicalRole]->(br:GraphCvTerm)"
        # get sources of interactors
        "OPTIONAL MATCH (a)-[:preferredIdentifier]->(:GraphXref)-[:database]->(ad:GraphCvTerm) "
        "OPTIONAL MATCH (b)-[:preferredIdentifier]->(:GraphXref)-[:database]->(bd:GraphCvTerm) "
        # return
        "RETURN n, nd.shortName AS source, nt, nc.miscore AS mi_score, "
        "a, ad.shortName AS src_a, at.shortName AS typ_a, ar.shortName AS role_a, "
        "b, bd.shortName AS src_b, bt.shortName AS typ_b, br.shortName AS role_b",
        ids=ids,
    )
    return result.data()
