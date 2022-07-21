############################################## About Folder Contents - START ##############################################################################

This folder includes,

1)"apoc_procedures_ot_data.txt" file
   This contains cypher queries which were executed in neo4j OTAR44 database to produce json files which are kept in data folder.
2)"ot_graphdb.zip" file
   This is compressed OTAR44 neo4j graph database. This database contains binary interactions between human,bacteria and virus interactors, coming from SIGNOR,  
   IntAct, Complex databases and also interactions between human interactors from Reactome.
3)"data" folder 
   This contains two json files,
   a) interactor_pair_interactions.json
      This contains collection of binary interactions per protein/rna pair and source, present in OTAR44 database. 
   b) protein_complexes.json
      This contains collection of complex acs per protein, present in OTAR44 database.
   Further specifications on the json format used can be found here: "https://bit.ly/json_details"

############################################## About Folder Contents - END ##############################################################################


########################### How to set up OTAR44 neo4j graph database on your local? - START###############################################################

1) Download Neo4j Community Edition 3.5.26 from
https://neo4j.com/download-center/

2) Extract ot_graphdb.zip in
your_path_of_neo4j/data/databases

3) cd your_path_of_neo4j

4) Start the server by command,
./bin/neo4j console

5) Query the graph through cypher

########################### How to set up OTAR44 neo4j graph database on your local? - END###############################################################

########################### How to produce the json files from OTAR44 neo4j graph database on your local? - START########################################


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Set up apoc plugin @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
1)Go to https://github.com/neo4j-contrib/neo4j-apoc-procedures/tags and download appropriate (match major minor versions to your neo4j version)  binary
 jar to place into your $NEO4J_HOME/plugins folder.
for eg. for "neo4j-3.5.26", apoc plugin to download was "apoc-3.5.0.15-all.jar"

2.1)Make sure that you have added following line in "neo4j.conf" file:
apoc.export.file.enabled=true

The "neo4j.conf" file is located at: $NEO4J_HOME/conf/neo4j.conf

2.2)In neo4j.conf, 

  a) Edit and uncomment #dbms.directories.plugins=plugins as given below
     dbms.directories.plugins=$NEO4J_HOME/plugins
  b) Edit and uncomment as given below
     dbms.security.procedures.unrestricted=apoc.export.json.query,apoc.warmup.*
  c) Edit and uncomment as given below
     dbms.security.procedures.whitelist=apoc.export.json.query,apoc.warmup.*
  d) Edit and uncomment as given below
     dbms.memory.heap.initial_size=8G
     dbms.memory.heap.max_size=8G

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Setting up apoc plugin - END @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Export protein_complexes.json Yourself @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Run the apoc procedure given in "PROTEIN_COMPLEXES - APOC PROCEDURE" section in the file "apoc_procedures_ot_data.txt" kept at the same level README.txt

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Export protein_complexes.json Yourself- END @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Export protein_pair_interactions.json Yourself- START @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Run the apoc procedure given in "PROTEIN_PAIR_INTERACTIONS - APOC PROCEDURE" section in the file "apoc_procedures_ot_data.txt" kept at the same level README.txt

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Export protein_pair_interactions.json Yourself- END @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

########################### How to produce the json files from OTAR44 neo4j graph database on your local? - END#############################################

