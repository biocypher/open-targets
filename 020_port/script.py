from adapter import BioCypherAdapter

adapter = BioCypherAdapter(db_name="small")

adapter.write_nodes()
