import sys
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


keyword_file = sys.argv[1]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

with open(keyword_file, encoding='utf-8') as f:
    keywords = [line.strip() for line in f if line.strip()]

session = requests.Session()
session.headers.update(headers)

for keyword in keywords:
    print(f"downloading {keyword}")
    try:
        # 1) Search page
        resp = session.get(
            "https://www.biosino.org/elmsg/search",
            params={"keyword": keyword},
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"search failed for {keyword}: HTTP {resp.status_code}")
            continue
        first_soup = BeautifulSoup(resp.text, "html.parser")

        a = first_soup.select_one('a.title[href]')
        if not a:
            print(f"no record link found for {keyword}")
            continue
        first_url = urljoin("https://www.biosino.org", a.get('href'))

        # 2) Record page
        resp2 = session.get(first_url, timeout=30)
        if resp2.status_code != 200:
            print(f"record page failed for {keyword}: HTTP {resp2.status_code}")
            continue
        second_soup = BeautifulSoup(resp2.text, "html.parser")

        b = second_soup.select_one('a.btn.btn-success.btn-sm[href]')
        if not b:
            print(f"no download link found for {keyword}")
            continue
        second_url = urljoin("https://www.biosino.org", b.get('href'))

        # 3) Download FASTA
        resp3 = session.get(second_url, timeout=60)
        if resp3.status_code != 200:
            print(f"download failed for {keyword}: HTTP {resp3.status_code}")
            continue
        fasta_text = resp3.text

        # 4) Report and save
        print(f"the number of contigs in {keyword} is {fasta_text.count('>')}")
        out_path = f"{keyword}.fasta"
        with open(out_path, "w", encoding='utf-8') as out_f:
            out_f.write(fasta_text)
        print(f"downloaded {keyword}")

        time.sleep(1)
    except Exception as e:
        print(f"error downloading {keyword}: {e}")