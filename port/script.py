import cProfile
import io
import pstats

from adapter import BioCypherAdapter

PROFILE = True


def main():
    """
    Run adapter to import data into Neo4j.

    Optionally, run with profiling.
    """
    if PROFILE:
        profile = cProfile.Profile()
        profile.enable()

    # create and run adapter
    adapter = BioCypherAdapter(db_name="ppi2", id_batch_size=int(1e5))
    adapter.write_to_csv_for_admin_import()

    if PROFILE:
        profile.disable()

        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
        ps.print_stats()

        ps.dump_stats("adapter.prof")
        # look at stats using snakeviz


if __name__ == "__main__":
    main()
