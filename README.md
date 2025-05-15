# Antibiotic Resistance Gene Finder

This web application allows users to search for antibiotic resistance genes by comparing input DNA sequences against the CARD and ResFinder databases.

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. The database is already set up on the bfx server. The following files are only used for initial database creation and are not needed for running the application:
- `parse.py` - Used only for parsing of CARD and ResFinder databases
- `populate_db.py` - Used only for population of the database
- Database creation files in CARD/ and ResFinder/ directories

## File Structure

- `final.html` - Main web interface
- `gene_finder.cgi` - CGI script handling the gene search functionality
- `js/final.js` - JavaScript for handling user interactions and AJAX calls
- `css/final.css` - Styling for the web interface
- `settings.ini` - Database configuration file
- `requirements.txt` - Python package dependencies

## Usage

1. Access the web application using this link:
```
http://bfx3.aap.jhu.edu/dpatel95/final/final.html
```

2. Using the interface:
   - Enter a DNA sequence in the main text area
   - Optionally, enter a specific gene name to search for. This is used when searching for a specific gene rather than all the genes in the database
   - Select the database to search in (CARD, ResFinder, or Both)
   - Click "Search for Matches" to find matching genes

3. Results will display:
   - Gene ID
   - Gene Name
   - Drug Class
   - Resistance Mechanism
   - Source Database
   - Identity Percentage
   - Match Position
   - Gene Sequence

## Credits

Created by Dhwanil Patel

Uses data from:
- CARD (Comprehensive Antibiotic Resistance Database)
    -https://github.com/arpcard
- ResFinder Database
    https://bitbucket.org/genomicepidemiology/resfinder_db/src/master/
