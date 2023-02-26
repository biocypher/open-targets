#!/bin/bash
sleep 10
echo "Starting to create the database"
cypher-shell -u neo4j -p neo4jpassword "create database test"
echo "Database created!"