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
    MATCH (n:Association)
    WITH n LIMIT 100
    OPTIONAL MATCH (n)<--(p1:BiologicalEntity)
    OPTIONAL MATCH (n)<--(p2:BiologicalEntity)
    OPTIONAL MATCH (n)-->(e:Experiment)-->(a:Article)
    OPTIONAL MATCH (p1)<-[r1:ExperimentToInteractorAssociation]-(e)
    OPTIONAL MATCH (p2)<-[r2:ExperimentToInteractorAssociation]-(e)
    OPTIONAL MATCH (e)-->(t:EvidenceType)
    OPTIONAL MATCH (e)-->(o:OrganismalEntity)
    RETURN n, p1, p2, r1, r2, e, a, t, o
    """

    result, summary = driver.query(query)

    if print_result:
        for res in result:
            print(res)


if __name__ == "__main__":
    main()
    # test_run(print_result=True)
