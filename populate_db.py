#!/usr/bin/env python3

import mysql.connector
import parse

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="dpatel95",
    password="Djp-Manisha75",
    database="dpatel95"
)
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
