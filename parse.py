#!/usr/bin/env python3

import re
from Bio import SeqIO
import pandas as pd
import os

def card():
    """
    Parses the CARD database files to extract gene information and add to my database
    """

    seq_file = "CARD/nucleotide_fasta_protein_homolog_model.fasta"
    metadata_file = "CARD/aro_index.tsv"

    # Initialize the dictionary of genes
    genes = {}

    # Parse the seq file
    for record in SeqIO.parse(seq_file, "fasta"):
        header = record.id
        seq = str(record.seq)

        # Extract the ID
        id = re.search(r"^[^|]+\|([A-Z0-9_]+)\.", header).group(1)
        name = re.search(r"\|([^|]+)$", header).group(1)

        genes[name] = {
            'id': id,
            'name': name,
            'class': None,
            'mechanism': None,
            'source': 'CARD',
            'sequence': seq,
        }

    # Parse the metadata file
    metadata = pd.read_csv(metadata_file, sep="\t", header=0)
    # Extract the relevant columns
    metadata = metadata[['CARD Short Name', 'DNA Accession', 'Drug Class', 'Resistance Mechanism']]
    # Rename the columns to match the genes dictionary
    metadata.columns = ['name', 'id', 'class', 'mechanism']
    # Merge the metadata with the genes dictionary
    for index, row in metadata.iterrows():
        name = row['name']
        if name in genes:
            genes[name]['class'] = row['class']
            genes[name]['mechanism'] = row['mechanism']

    return genes

def resFinder(genes):
    """
    Parses the ResFinder database files to extract gene information and add to my database
    """
    seq_folder = "ResFinder/"
    metadata_file = "ResFinder/phenotypes.txt"

    for filename in os.listdir(seq_folder):
        # Skip non-fasta files
        if filename.endswith(".fsa"):
            seq_file = os.path.join(seq_folder, filename)
            for record in SeqIO.parse(seq_file, "fasta"):
                header = record.id
                seq = str(record.seq)

                # Extract the ID
                id_match = re.search(r"^(.*?_[^_]*)_(.*)$", header)
                if id_match:
                    id = id_match.group(2)
                name_match = re.search(r"^(.*?_[^_]*)_(.*)$", header)
                if name_match:
                    name = name_match.group(1)

                # Check if the gene is already in the dictionary
                if name in genes:
                    # If it is, change the source to both and then skip
                    genes[name]['source'] = 'Both'
                    continue
                # If it is not, add it to the dictionary
                else:
                    genes[name] = {
                        'id': id,
                        'name': name,
                        'class': filename[:-4],
                        'mechanism': None,
                        'source': 'ResFinder',
                        'sequence': seq,
                    }

    # Parse the metadata file
    metadata = pd.read_csv(metadata_file, sep="\t", header=0)
    metadata = metadata.dropna(subset=['Gene_accession no.', 'Mechanism of resistance'])
    # Extract the relevant columns
    metadata = metadata[['Gene_accession no.',  'Mechanism of resistance']]
    # Rename the columns to match the genes dictionary
    metadata.columns = ['name', 'mechanism']
    # Merge the metadata with the genes dictionary
    for index, row in metadata.iterrows():
        name = row['name']
        name_match = re.search(r"^(.*?_[^_]*)_(.*)$", name)
        if name_match:
            name = name_match.group(1)

        for key in genes.keys():
            if (key == name) and (genes[key]['mechanism'] is None):
                # If the gene is in the dictionary, add the mechanism
                genes[key]['mechanism'] = row['mechanism']

                break
    return genes

genes = card()
genes = resFinder(genes)
