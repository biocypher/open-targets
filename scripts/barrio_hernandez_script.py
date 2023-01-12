import cProfile
import io
import pstats

# VSCode does not add the root directory to the path (by default?). Not sure why
# this works sometimes and not others. This is a workaround.
import sys

sys.path.append("")

from adapters.barrio_hernandez_adapter import BarrioHernandezAdapter

PROFILE = False


def main():
    """
    Run adapter to import data into Neo4j.

    Optionally, run with profiling.
    """
    if PROFILE:
        profile = cProfile.Profile()
        profile.enable()

    # create and run adapter
    adapter = BarrioHernandezAdapter(
        user_schema_config_path="config/barrio_hernandez_schema_config.yaml",
        db_name="ppi1",
        id_batch_size=int(1e5),
    )

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
