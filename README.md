# eLMSG Genome Downloader

A Python script for bulk downloading genome sequences from eLMSG (eLibrary of Microbial Systematics and Genomics) using accession numbers.

This script searches for each accession, navigates to the download page, and saves the genome sequences locally.

## Usage

### Prerequisites

- Python 3.6 or higher
- Internet connection

### Dependencies


```bash
pip install requests beautifulsoup4
```
### Usage

1. Prepare a text file containing accession numbers (one per line)
2. Run the script with your accession file:

```bash
python bulk_downloader.py your_accessions.txt
```

### Example

Using the provided example file:

```bash
python bulk_downloader.py example_accessions.txt
```

This will download three genomes from the example file.

