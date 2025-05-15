#!/usr/bin/env python3
import sys, os
import cgi, json
import mysql.connector
from Bio import Align
import heapq

# Get form data
form = cgi.FieldStorage()

# Print JSON header
print("Content-Type: application/json\n")

try:
    # Connect to database
    conn = mysql.connector.connect(
        host="localhost",
        user="dpatel95",
        password="Djp-Manisha75",
        database="dpatel95"
    )
    cursor = conn.cursor()

    # Check if this is an autocomplete request
    if 'search_term' in form and not 'sequence' in form:
        search_term = form.getvalue('search_term', '').strip()
        source_db = form.getvalue('source_db', 'Both').strip()
        
        # Build and execute query
        if source_db != 'Both':
            cursor.execute("""
                SELECT DISTINCT name 
                FROM final 
                WHERE name LIKE %s AND source = %s 
                LIMIT 5
            """, ('%' + search_term + '%', source_db))
        else:
            cursor.execute("""
                SELECT DISTINCT name 
                FROM final 
                WHERE name LIKE %s 
                LIMIT 5
            """, ('%' + search_term + '%',))
        
        matches = [{'name': row[0]} for row in cursor.fetchall()]
        print(json.dumps({'matches': matches}))
        
    else:
        # Regular search handling
        query_sequence = form.getvalue('sequence', '').strip()
        query_gene = form.getvalue('search_term', '').strip()
        source_db = form.getvalue('source_db', 'Both').strip()

        # Validate sequence input
        if not query_sequence:
            print(json.dumps({
                'error': 'No sequence provided',
                'match_count': 0,
                'matches': []
            }))
            sys.exit()

        # Build and execute query
        if query_gene:
            qry = """
                SELECT id, name, class, mechanism, source, sequence
                FROM final
                WHERE name LIKE %s
            """
            if source_db != 'Both':
                qry += " AND source = %s"
                params = ('%' + query_gene + '%', source_db)
            else:
                params = ('%' + query_gene + '%',)
        else:
            qry = "SELECT id, name, class, mechanism, source, sequence FROM final"
            if source_db != 'Both':
                qry += " WHERE source = %s"
                params = (source_db,)
            else:
                params = tuple()
        
        if params:
            cursor.execute(qry, params)
        else:
            cursor.execute(qry)

        # Process results
        top_matches = []  # Will store (-identity, index, match_dict) tuples
        match_count = 0  # Counter for sorting
        
        # Set up sequence aligner
        aligner = Align.PairwiseAligner()
        aligner.mode = 'local'
        aligner.match_score = 2.0      
        aligner.mismatch_score = -1.0  # Penalize mismatches
        aligner.gap_score = -2.0       # Penalize gaps
        aligner.target_end_gap_score = 0.0  # Don't penalize end gaps
        aligner.query_end_gap_score = 0.0   # Don't penalize end gaps

        for (id, name, gene_class, mechanism, source, sequence) in cursor:
            try:
                # Get only the first (best) alignment
                alignments = aligner.align(query_sequence.upper(), sequence.upper())
                alignment = next(alignments)  # Get first alignment only
                
                # Get the alignment strings
                aligned_seqs = str(alignment).split('\n')
                if len(aligned_seqs) >= 3:
                    aligned_query = aligned_seqs[0]
                    aligned_target = aligned_seqs[2]
                    
                    # Count matches only in aligned region
                    matches = sum(a == b for a, b in zip(aligned_query, aligned_target))
                    # Use alignment length for identity calculation
                    identity = (matches / len(aligned_query)) * 100
                    
                    # Only process matches with >50% identity
                    if identity > 50:
                        # Get alignment position
                        start_pos = 0
                        while start_pos < len(aligned_query) and aligned_query[start_pos] == '-':
                            start_pos += 1
                        end_pos = len(aligned_query)
                        while end_pos > 0 and aligned_query[end_pos - 1] == '-':
                            end_pos -= 1
                        
                        # Create match dictionary
                        match = {
                            'id': id,
                            'name': name,
                            'class': gene_class,
                            'mechanism': mechanism,
                            'source': source,
                            'sequence': sequence,
                            'identity_percentage': round(identity, 2),
                            'match_position': f"{start_pos + 1}-{end_pos}"
                        }
                        
                        # Keep only top 100 matches using a ma heap
                        heap_item = (-identity, match_count, match)
                        match_count += 1
                        
                        if len(top_matches) < 100:
                            heapq.heappush(top_matches, heap_item)
                        elif heap_item < top_matches[0]:  # Compare with worst match
                            heapq.heapreplace(top_matches, heap_item)
            except Exception as align_error:
                continue  # Skip this sequence if alignment fails

        # Sort matches by identity (highest first) and extract just the match dictionaries
        sorted_matches = sorted(top_matches)  # Will sort by first element
        results = {
            'match_count': len(sorted_matches),
            'matches': [match for _, _, match in sorted_matches]
        }
        
        print(json.dumps(results))

except Exception as e:
    print(json.dumps({
        'error': str(e),
        'match_count': 0,
        'matches': []
    }))

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
