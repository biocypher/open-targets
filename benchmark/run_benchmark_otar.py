import timeit

import neo4j_utils as nu

driver = nu.Driver(
    db_name="neo4j",
    db_uri="bolt://localhost:7687",
    multi_db=False,
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
    MATCH (interaction:GraphBinaryInteractionEvidence)
    WITH interaction LIMIT 100
    MATCH (typeAN:GraphCvTerm)<-[:interactorType]-(interactorA:GraphInteractor)<-[:interactorA]-(interaction)-[:interactorB]->(interactorB:GraphInteractor)-[:interactorType]->(typeBN:GraphCvTerm) # noqa:E501
    WHERE  ID(interactorA)<>ID(interactorB) AND (EXISTS(interactorA.uniprotName)
                    OR typeAN.mIIdentifier IN ['MI:0320','MI:0321','MI:0322','MI:0323','MI:2190','MI:0324','MI:2204','MI:0679','MI:0608','MI:0611','MI:0610','MI:0609','MI_0325'])
        AND (EXISTS(interactorB.uniprotName)
                    OR typeBN.mIIdentifier IN ['MI:0320','MI:0321','MI:0322','MI:0323','MI:2190','MI:0324','MI:2204','MI:0679','MI:0608','MI:0611','MI:0610','MI:0609','MI_0325'])

    MATCH (interaction)-[identifiersR:identifiers]-(identifiersN:GraphXref)-[sourceR:database]-(sourceN:GraphCvTerm) WHERE sourceN.shortName IN ['reactome','signor','intact']

    WITH COLLECT(distinct interaction) as interactionColl,interactorA,interactorB,sourceN,identifiersN,typeAN,typeBN
    UNWIND interactionColl as interactionN

    OPTIONAL MATCH (interactionN)-[:BIE_PARTICIPANTA]-(entityA:GraphEntity)
    OPTIONAL MATCH (interactionN)-[:BIE_PARTICIPANTB]-(entityB:GraphEntity)

    WITH CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN interactorA
                        ELSE interactorB
                        END as interactorAN,

        CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN interactorB
                        ELSE interactorA
                        END as interactorBN,

        CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN entityA
                        ELSE entityB
                        END as entityAN,

        CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN entityB
                        ELSE entityA
                        END as entityBN,

        CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN typeAN
                        ELSE typeBN
                        END as typeA,

        CASE ID(interactorA)<ID(interactorB)
                        WHEN true THEN typeBN
                        ELSE typeAN
                        END as typeB,

                        interactionN,
                        sourceN,
                        identifiersN

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)


    WITH interactionN,
        entityAN,
        entityBN,
        interactorAN,
        interactorBN,
        sourceN,
        identifiersN,
        typeA,
        typeB,
        COLLECT(
                {short_name:participantIdentificationMethodAN.shortName,
                mi_identifier:participantIdentificationMethodAN.mIIdentifier}) as participantIdentificationMethodAColl

    OPTIONAL MATCH (entityBN)-[identificationMethodsBR:identificationMethods]->(participantIdentificationMethodBN:GraphCvTerm)

    WITH interactionN,
        entityAN,
        entityBN,
        interactorAN,
        interactorBN,
        sourceN,
        identifiersN,
        typeA,
        typeB,
        participantIdentificationMethodAColl,
        COLLECT(
                {short_name:participantIdentificationMethodBN.shortName,
                mi_identifier:participantIdentificationMethodBN.mIIdentifier}) as participantIdentificationMethodBColl

    OPTIONAL MATCH (interactorAN)-[:preferredIdentifier]->(identifierAN:GraphXref)-[:database]->(identifierDatabaseAN:GraphCvTerm)
    OPTIONAL MATCH (interactorBN)-[:preferredIdentifier]->(identifierBN:GraphXref)-[:database]->(identifierDatabaseBN:GraphCvTerm)
    OPTIONAL MATCH (interactorAN)-[:organism]->(organismAN:GraphOrganism)
    OPTIONAL MATCH (interactorBN)-[:organism]->(organismBN:GraphOrganism)

    OPTIONAL MATCH (entityAN)-[:biologicalRole]-(biologicalRoleAN:GraphCvTerm)
    OPTIONAL MATCH (entityBN)-[:biologicalRole]-(biologicalRoleBN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[clusteredInteractionR:interactions]-(clusteredInteractionN:GraphClusteredInteraction)

    OPTIONAL MATCH (interactionN)-[interactiontypeR:interactionType]-(interactiontypeN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[experimentR:experiment]-(experimentN:GraphExperiment)-[interactionDetectionMethodR:interactionDetectionMethod]-(interactionDetectionMethodN:GraphCvTerm) # noqa:E501

    OPTIONAL MATCH (experimentN)-[hostOrganismR:hostOrganism]-(hostOrganismN:GraphOrganism)

    OPTIONAL MATCH (experimentN)-[publicationR:PUB_EXP]-(publicationN:GraphPublication)-[pubmedIdXrefR:pubmedId]-(pubmedIdXrefN:GraphXref)

    OPTIONAL MATCH (interactionN)-[complexExpansionR:complexExpansion]-(complexExpansionN:GraphCvTerm)

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)
    OPTIONAL MATCH (entityBN)-[identificationMethodsBR:identificationMethods]->(participantIdentificationMethodBN:GraphCvTerm)

    WITH
        {
            id:identifierAN.identifier,
            id_source: identifierDatabaseAN.shortName,
            organism: {
                scientific_name: organismAN.scientificName,
                taxon_id: organismAN.taxId,
                mnemonic: organismAN.commonName
                },
            biological_role: biologicalRoleAN.shortName,
            type: {
                short_name: typeA.shortName,
                mi_identifier: typeA.mIIdentifier
            }
            } as interactorA,
            {
            id:identifierBN.identifier,
            id_source: identifierDatabaseBN.shortName,
            organism: {
                scientific_name: organismBN.scientificName,
                taxon_id: organismBN.taxId,
                mnemonic: organismBN.commonName
                },
            biological_role: biologicalRoleBN.shortName,
            type: {
                short_name: typeB.shortName,
                mi_identifier: typeB.mIIdentifier
            }
            } as interactorB,
            {
            source_database:sourceN.shortName,
            database_version:CASE sourceN.shortName
                                WHEN 'reactome' THEN '77'
                                WHEN 'signor' THEN 'Not Available'
                                ELSE '240' END
            } as source_info,
            clusteredInteractionN.miscore as mi_score,
            COLLECT(distinct
                {interaction_identifier: CASE sourceN.shortName
                                            WHEN 'intact'
                                            THEN interactionN.ac
                                            ELSE identifiersN.identifier END,
                    interaction_type_short_name: interactiontypeN.shortName,
                    interaction_type_mi_identifier: interactiontypeN.mIIdentifier,
                    interaction_detection_method_short_name: interactionDetectionMethodN.shortName,
                    interaction_detection_method_mi_identifier: interactionDetectionMethodN.mIIdentifier,
                    host_organism_scientific_name: hostOrganismN.scientificName,
                    host_organism_tax_id: hostOrganismN.taxId,
                    participant_detection_method_A:participantIdentificationMethodAColl,
                    participant_detection_method_B:participantIdentificationMethodBColl,
                    pubmed_id:pubmedIdXrefN.identifier,
                    expansion_method_short_name: complexExpansionN.shortName,
                    expansion_method_mi_identifier: complexExpansionN.mIIdentifier
                } )  as interaction_evidences


    RETURN interactorA,interactorB,source_info,
                {interaction_score: mi_score,
                    causal_interaction:null,
                    evidence:interaction_evidences
                } as interaction

    UNION

    MATCH (interaction:GraphBinaryInteractionEvidence)
    WITH interaction LIMIT 100
    MATCH (typeAN:GraphCvTerm)<-[:interactorType]-(interactorAN:GraphInteractor)<-[:interactorA]-(interaction)-[:interactorB]->(interactorBN:GraphInteractor)
    WHERE  (ID(interactorAN)=ID(interactorBN))
        AND (EXISTS(interactorAN.uniprotName)
                    OR typeAN.mIIdentifier IN ['MI:0320','MI:0321','MI:0322','MI:0323','MI:2190','MI:0324','MI:2204','MI:0679','MI:0608','MI:0611','MI:0610','MI:0609','MI_0325'])

    MATCH (interaction)-[identifiersR:identifiers]-(identifiersN:GraphXref)-[sourceR:database]-(sourceN:GraphCvTerm) WHERE sourceN.shortName IN ['reactome','signor','intact']

    WITH COLLECT(distinct interaction) as interactionColl,interactorAN,interactorBN,sourceN,identifiersN,typeAN
    UNWIND interactionColl as interactionN

    OPTIONAL MATCH (interactionN)-[:BIE_PARTICIPANTA]-(entityAN:GraphEntity)
    OPTIONAL MATCH (interactionN)-[:BIE_PARTICIPANTB]-(entityBN:GraphEntity)

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)


    WITH interactionN,
        entityAN,
        entityBN,
        interactorAN,
        interactorBN,
        sourceN,
        identifiersN,
        typeAN,
        COLLECT(
                {short_name:participantIdentificationMethodAN.shortName,
                mi_identifier:participantIdentificationMethodAN.mIIdentifier}) as participantIdentificationMethodAColl

    OPTIONAL MATCH (entityBN)-[identificationMethodsBR:identificationMethods]->(participantIdentificationMethodBN:GraphCvTerm)

    WITH interactionN,
        entityAN,
        entityBN,
        interactorAN,
        interactorBN,
        sourceN,
        identifiersN,
        typeAN,
        participantIdentificationMethodAColl,
        COLLECT(
                {short_name:participantIdentificationMethodBN.shortName,
                mi_identifier:participantIdentificationMethodBN.mIIdentifier}) as participantIdentificationMethodBColl

    OPTIONAL MATCH (interactorAN)-[:preferredIdentifier]->(identifierAN:GraphXref)-[:database]->(identifierDatabaseAN:GraphCvTerm)
    OPTIONAL MATCH (interactorBN)-[:preferredIdentifier]->(identifierBN:GraphXref)-[:database]->(identifierDatabaseBN:GraphCvTerm)
    OPTIONAL MATCH (interactorAN)-[:organism]->(organismAN:GraphOrganism)
    OPTIONAL MATCH (interactorBN)-[:organism]->(organismBN:GraphOrganism)

    OPTIONAL MATCH (entityAN)-[:biologicalRole]-(biologicalRoleAN:GraphCvTerm)
    OPTIONAL MATCH (entityBN)-[:biologicalRole]-(biologicalRoleBN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[clusteredInteractionR:interactions]-(clusteredInteractionN:GraphClusteredInteraction)

    OPTIONAL MATCH (interactionN)-[interactiontypeR:interactionType]-(interactiontypeN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[experimentR:experiment]-(experimentN:GraphExperiment)-[interactionDetectionMethodR:interactionDetectionMethod]-(interactionDetectionMethodN:GraphCvTerm)

    OPTIONAL MATCH (experimentN)-[hostOrganismR:hostOrganism]-(hostOrganismN:GraphOrganism)

    OPTIONAL MATCH (experimentN)-[publicationR:PUB_EXP]-(publicationN:GraphPublication)-[pubmedIdXrefR:pubmedId]-(pubmedIdXrefN:GraphXref)

    OPTIONAL MATCH (interactionN)-[complexExpansionR:complexExpansion]-(complexExpansionN:GraphCvTerm)

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)
    OPTIONAL MATCH (entityBN)-[identificationMethodsBR:identificationMethods]->(participantIdentificationMethodBN:GraphCvTerm)

    WITH
        {
            id:identifierAN.identifier,
            id_source: identifierDatabaseAN.shortName,
            organism: {
                scientific_name: organismAN.scientificName,
                taxon_id: organismAN.taxId,
                mnemonic: organismAN.commonName
                },
            biological_role: biologicalRoleAN.shortName,
            type: {
                short_name: typeAN.shortName,
                mi_identifier: typeAN.mIIdentifier
            }
            } as interactorA,
            {
            id:identifierBN.identifier,
            id_source: identifierDatabaseBN.shortName,
            organism: {
                scientific_name: organismBN.scientificName,
                taxon_id: organismBN.taxId,
                mnemonic: organismBN.commonName
                },
            biological_role: biologicalRoleBN.shortName,
            type: {
                short_name: typeAN.shortName,
                mi_identifier: typeAN.mIIdentifier
            }
            } as interactorB,
            {
            source_database:sourceN.shortName,
            database_version:CASE sourceN.shortName
                                WHEN 'reactome' THEN '77'
                                WHEN 'signor' THEN 'Not Available'
                                ELSE '240' END
            } as source_info,
            clusteredInteractionN.miscore as mi_score,
            COLLECT(distinct
                {interaction_identifier: CASE sourceN.shortName
                                            WHEN 'intact'
                                            THEN interactionN.ac
                                            ELSE identifiersN.identifier END,
                    interaction_type_short_name: interactiontypeN.shortName,
                    interaction_type_mi_identifier: interactiontypeN.mIIdentifier,
                    interaction_detection_method_short_name: interactionDetectionMethodN.shortName,
                    interaction_detection_method_mi_identifier: interactionDetectionMethodN.mIIdentifier,
                    host_organism_scientific_name: hostOrganismN.scientificName,
                    host_organism_tax_id: hostOrganismN.taxId,
                    participant_detection_method_A:participantIdentificationMethodAColl,
                    participant_detection_method_B:participantIdentificationMethodBColl,
                    pubmed_id:pubmedIdXrefN.identifier,
                    expansion_method_short_name: complexExpansionN.shortName,
                    expansion_method_mi_identifier: complexExpansionN.mIIdentifier
                } )  as interaction_evidences


    RETURN interactorA,interactorB,source_info,
                {interaction_score: mi_score,
                    causal_interaction:null,
                    evidence:interaction_evidences
                } as interaction

    ORDER BY interactorA.id

    UNION

    MATCH (interaction:GraphBinaryInteractionEvidence)
    WITH interaction LIMIT 100
    MATCH (typeAN:GraphCvTerm)<-[:interactorType]-(interactorAN:GraphInteractor)-[:interactorA]-(interaction)
    WHERE  (NOT (interaction)-[:interactorB]-(:GraphInteractor))
        AND (EXISTS(interactorAN.uniprotName)
                    OR typeAN.mIIdentifier IN ['MI:0320','MI:0321','MI:0322','MI:0323','MI:2190','MI:0324','MI:2204','MI:0679','MI:0608','MI:0611','MI:0610','MI:0609','MI_0325'])

    MATCH (interaction)-[identifiersR:identifiers]-(identifiersN:GraphXref)-[sourceR:database]-(sourceN:GraphCvTerm) WHERE sourceN.shortName IN ['reactome','signor','intact']

    WITH COLLECT(distinct interaction) as interactionColl,interactorAN,sourceN,identifiersN,typeAN
    UNWIND interactionColl as interactionN

    OPTIONAL MATCH (interactionN)-[:BIE_PARTICIPANTA]-(entityAN:GraphEntity)

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)


    WITH interactionN,
        entityAN,
        interactorAN,
        sourceN,
        identifiersN,
        typeAN,
        COLLECT(
                {short_name:participantIdentificationMethodAN.shortName,
                mi_identifier:participantIdentificationMethodAN.mIIdentifier}) as participantIdentificationMethodAColl

    OPTIONAL MATCH (interactorAN)-[:preferredIdentifier]->(identifierAN:GraphXref)-[:database]->(identifierDatabaseAN:GraphCvTerm)
    OPTIONAL MATCH (interactorAN)-[:organism]->(organismAN:GraphOrganism)

    OPTIONAL MATCH (entityAN)-[:biologicalRole]-(biologicalRoleAN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[clusteredInteractionR:interactions]-(clusteredInteractionN:GraphClusteredInteraction)

    OPTIONAL MATCH (interactionN)-[interactiontypeR:interactionType]-(interactiontypeN:GraphCvTerm)

    OPTIONAL MATCH (interactionN)-[experimentR:experiment]-(experimentN:GraphExperiment)-[interactionDetectionMethodR:interactionDetectionMethod]-(interactionDetectionMethodN:GraphCvTerm) # noqa:E501

    OPTIONAL MATCH (experimentN)-[hostOrganismR:hostOrganism]-(hostOrganismN:GraphOrganism)

    OPTIONAL MATCH (experimentN)-[publicationR:PUB_EXP]-(publicationN:GraphPublication)-[pubmedIdXrefR:pubmedId]-(pubmedIdXrefN:GraphXref)  # noqa:E501

    OPTIONAL MATCH (interactionN)-[complexExpansionR:complexExpansion]-(complexExpansionN:GraphCvTerm)

    OPTIONAL MATCH (entityAN)-[identificationMethodsAR:identificationMethods]->(participantIdentificationMethodAN:GraphCvTerm)

    WITH
        {
            id:identifierAN.identifier,
            id_source: identifierDatabaseAN.shortName,
            organism: {
                scientific_name: organismAN.scientificName,
                taxon_id: organismAN.taxId,
                mnemonic: organismAN.commonName
                },
            biological_role: biologicalRoleAN.shortName,
            type: {
                short_name: typeAN.shortName,
                mi_identifier: typeAN.mIIdentifier
            }
            } as interactorA,
            null as interactorB,
            {
            source_database:sourceN.shortName,
            database_version:CASE sourceN.shortName
                                WHEN 'reactome' THEN '77'
                                WHEN 'signor' THEN 'Not Available'
                                ELSE '240' END
            } as source_info,
            clusteredInteractionN.miscore as mi_score,
            COLLECT(distinct
                {interaction_identifier: CASE sourceN.shortName
                                            WHEN 'intact'
                                            THEN interactionN.ac
                                            ELSE identifiersN.identifier END,
                    interaction_type_short_name: interactiontypeN.shortName,
                    interaction_type_mi_identifier: interactiontypeN.mIIdentifier,
                    interaction_detection_method_short_name: interactionDetectionMethodN.shortName,
                    interaction_detection_method_mi_identifier: interactionDetectionMethodN.mIIdentifier,
                    host_organism_scientific_name: hostOrganismN.scientificName,
                    host_organism_tax_id: hostOrganismN.taxId,
                    participant_detection_method_A:participantIdentificationMethodAColl,
                    participant_detection_method_B:null,
                    pubmed_id:pubmedIdXrefN.identifier,
                    expansion_method_short_name: complexExpansionN.shortName,
                    expansion_method_mi_identifier: complexExpansionN.mIIdentifier
                } )  as interaction_evidences


    RETURN interactorA,interactorB,source_info,
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
    main()
    # test_run(print_result=True)
