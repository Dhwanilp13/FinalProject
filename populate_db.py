#!/usr/bin/env python3

import mysql.connector
import parse
from db_config import load_db_config

# Connect to your MySQL database using local settings.ini (not committed)
conn = mysql.connector.connect(**load_db_config())
cursor = conn.cursor()

# SQL INSERT statement
insert = """
    INSERT INTO final
    (id, name, class, mechanism, source, sequence)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

genes = parse.card()
genes = parse.resFinder(genes)

# Insert from genes dictionary
for gene_data in genes.values():
    values = (
        gene_data['id'],
        gene_data['name'],
        gene_data['class'],
        gene_data['mechanism'],
        gene_data['source'],
        gene_data['sequence']
    )
    cursor.execute(insert, values)

# Commit and close
conn.commit()
cursor.close()
conn.close()
