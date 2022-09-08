from adapter import BioCypherAdapter

adapter = BioCypherAdapter(db_name="ppi1")

adapter.write_to_csv_for_admin_import()
