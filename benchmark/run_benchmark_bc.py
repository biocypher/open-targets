import timeit

import neo4j_utils as nu

driver = nu.Driver(
    db_name="ppi2",
    db_uri="bolt://localhost:7687",
    db_user="neo4j",
    db_passwd="your_password_here",
    max_connection_lifetime=3600,
)


def main():

    num_runs = 5
    num_warmup_runs = 5

    # warmup
    print("warming up")
    timeit.Timer(test_run).timeit(number=num_warmup_runs)

    # run
    print("running")
    duration = timeit.Timer(test_run).timeit(number=num_runs)

    # calculate and save time
    average = duration / num_runs

    print(f"Average time taken: {average} seconds.")


def test_run(print_result=False):
    # run query
    query = """
    MATCH (association:Association)
    WITH association LIMIT 100
    OPTIONAL MATCH (association)<--(entity1:BiologicalEntity)
    OPTIONAL MATCH (association)<--(entity2:BiologicalEntity)
    OPTIONAL MATCH (association)-[:InteractionToExperimentAssociation]->(experiment:Experiment)-[:ExperimentToArticleAssociation]->(article:Article)
    OPTIONAL MATCH (entity1)<-[r1:ExperimentToInteractorAssociation]-(experiment)
    OPTIONAL MATCH (entity2)<-[r2:ExperimentToInteractorAssociation]-(experiment)
    OPTIONAL MATCH (experiment)-[:ExperimentToEvidenceTypeAssociation]->(type:EvidenceType)
    OPTIONAL MATCH (experiment)-[:ExperimentToOrganismalEntityAssociation]->(organism:OrganismalEntity)

    WITH
        {
            id:entity1.preferredName,
            organism: {
                scientific_name: organism.scientificName,
                taxon_id: organism.taxId,
                mnemonic: organism.commonName
                },
            biological_role: association.src_role
        } as interactorA,
        {
            id:entity2.preferredName,
            organism: {
                scientific_name: organism.scientificName,
                taxon_id: organism.taxId,
                mnemonic: organism.commonName
                },
            biological_role: association.tar_role
        } as interactorB,
        association.mi_score as mi_score,
        COLLECT(distinct
            {
                interaction_type_short_name: association.interactionTypeShortName,
                interaction_type_mi_identifier: association.interactionTypeIdentifierStr,
                interaction_detection_method_short_name: type.shortName,
                interaction_detection_method_mi_identifier: type.mIIdentifier,
                host_organism_scientific_name: organism.scientificName,
                host_organism_tax_id: organism.taxId,
                participant_detection_method_A:r1.shortName,
                participant_detection_method_B:r2.shortName,
                pubmed_id:article.pubmed
            } )  as interaction_evidences


    RETURN interactorA,interactorB,
                {interaction_score: mi_score,
                    causal_interaction:null,
                    evidence:interaction_evidences
                } as interaction

    ORDER BY interactorA.id
    """

    result, summary = driver.query(query)

    if print_result:
        for res in result:
            print(res)


if __name__ == "__main__":
    # main()
    test_run(print_result=True)
