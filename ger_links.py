import requests
import csv
from bs4 import BeautifulSoup
import re
import os

def normalize_url(url):
    """Normalize URLs to ensure they're complete and properly formatted"""
    if url.startswith('//'):
        return 'https:' + url
    elif not url.startswith('http'):
        # Handle newer format
        if url.startswith('/media/'):
            return 'https://apcentral.collegeboard.org' + url
        # Handle older format
        return 'https://' + url.lstrip('/')
    return url

def get_filename(year):
    """Generate standardized filename for a given year"""
    return f"ap_cs_a_frq_{year}.pdf"

def scrape_frq_links(url):
    """
    Scrape AP CS A FRQ links from AP Central webpage, accounting for all URL patterns
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dictionary to store year -> (link, filename) mapping
    year_data = {}

    # Find all links
    for link in soup.find_all('a'):
        href = link.get('href', '')
        
        # Skip non-PDF links
        if not href.endswith('.pdf'):
            continue
            
        # Various patterns to identify FRQ PDFs
        frq_patterns = [
            r'frq.*exam.*questions.*comp.*sci',
            r'computer.*science.*frq.*exam.*questions',
            r'ap\d{2}.*comp.*sci.*exam.*questions',
            r'comp.*sci.*a.*frq.*exam.*questions',
        ]
        
        if not any(re.search(pattern, href.lower()) for pattern in frq_patterns):
            continue

        # Extract year using various patterns
        year_patterns = [
            r'ap(\d{2})[_-]',  # ap24-, ap24_
            r'/ap(\d{2})[-_]',  # /ap24-
            r'ap20(\d{2})',    # ap2024
            r'20(\d{2})[_-]',  # 2024-, 2024_
            r'(\d{2})_frq',    # 24_frq
        ]
        
        year = None
        for pattern in year_patterns:
            match = re.search(pattern, href)
            if match:
                year_digits = match.group(1)
                # Convert 2-digit year to 4-digit
                if len(year_digits) == 2:
                    year = '20' + year_digits if int(year_digits) < 50 else '19' + year_digits
                else:
                    year = year_digits
                break

        # Skip if no year found or if it's 2020 (which doesn't exist)
        if not year or year == '2020':
            continue

        # Normalize URL and store with filename
        full_url = normalize_url(href)
        filename = get_filename(year)
        year_data[year] = (full_url, filename)

    # Delete existing CSV file if it exists
    csv_filename = 'ap_cs_frq_links.csv'
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
        print(f"Deleted existing {csv_filename}")

    # Write to new CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year', 'Link', 'Filename'])
        
        # Write sorted data
        for year in sorted(year_data.keys()):
            url, filename = year_data[year]
            writer.writerow([year, url, filename])
    
    print(f"Created new {csv_filename} with {len(year_data)} FRQ links by year")
    
    # Print all entries for verification
    for year in sorted(year_data.keys()):
        url, filename = year_data[year]
        print(f"{year}: {url} -> {filename}")
        
    return year_data

# URL for AP CS A past exam questions
url = "https://apcentral.collegeboard.org/courses/ap-computer-science-a/exam/past-exam-questions"

# Run the scraper
scrape_frq_links(url)