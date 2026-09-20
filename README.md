# Antibiotic Resistance Gene Finder

Web app that searches a DNA sequence against CARD and ResFinder antibiotic resistance genes and reports identity, location, and source.

Live class server: [http://bfx3.aap.jhu.edu/dpatel95/final/final.html](http://bfx3.aap.jhu.edu/dpatel95/final/final.html)

## Features

- Pairwise local alignment of a query sequence against genes in MySQL
- Optional gene-name filter with autocomplete
- Search CARD, ResFinder, or both
- Results include identity percentage, match position, and gene sequence

## Requirements

- Python 3
- MySQL
- Packages in `requirements.txt`

## Setup

1. Clone the repository and create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy the example config and add your MySQL credentials. **Do not commit `settings.ini`.**

```bash
cp settings.ini.example settings.ini
```

3. Create the table (edit the database name in `database.sql` so it matches `settings.ini`):

```bash
mysql -u YOUR_USER -p < database.sql
```

4. If you need to load CARD and ResFinder into the database (already done on the class server):

```bash
python populate_db.py
```

`parse.py` and `populate_db.py` are one-time setup scripts. They read the files under `CARD/` and `ResFinder/`.

5. Serve the site so CGI can run `gene_finder.cgi` (Apache on the class server, or any local CGI-capable server). Open `final.html` in the browser.

## Usage

1. Paste a DNA sequence (bases only).
2. Optionally type a gene name to limit the search.
3. Choose CARD, ResFinder, or Both.
4. Click **Search for Matches**.

Results show gene ID, name, drug class, resistance mechanism, source, identity, match position, and sequence.

## Project layout

| Path | Purpose |
| --- | --- |
| `final.html` | Front-end form and results table |
| `js/final.js` | Autocomplete and AJAX search |
| `css/final.css` | Page styles |
| `gene_finder.cgi` | Search and autocomplete backend |
| `db_config.py` | Loads MySQL settings from `settings.ini` |
| `settings.ini.example` | Template for local credentials |
| `database.sql` | Table schema |
| `parse.py` / `populate_db.py` | One-time CARD and ResFinder import |
| `CARD/` / `ResFinder/` | Source files used only for the initial import |

## Security

Database username and password live only in `settings.ini`, which is gitignored. Use `settings.ini.example` as the public template.

## Credits

Created by Dhwanil Patel

Data sources:

- [CARD (Comprehensive Antibiotic Resistance Database)](https://github.com/arpcard)
- [ResFinder](https://bitbucket.org/genomicepidemiology/resfinder_db/src/master/)
