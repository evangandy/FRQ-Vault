import csv
import requests
import os
from pathlib import Path
import time

def download_frq_pdfs(csv_file, output_folder='frq_pdfs'):
    """
    Download FRQ PDFs from links in CSV file to specified folder
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        total_files = sum(1 for row in reader)  # Count total files
        file.seek(0)  # Reset file pointer
        next(reader)  # Skip header row
        
        print(f"Found {total_files} PDFs to download")
        
        # Download each PDF
        for i, row in enumerate(reader, 1):
            year = row['Year']
            url = row['Link']
            filename = f"ap_cs_a_frq_{year}.pdf"
            filepath = os.path.join(output_folder, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"[{i}/{total_files}] {filename} already exists, skipping...")
                continue
            
            try:
                print(f"[{i}/{total_files}] Downloading {filename}...", end=' ', flush=True)
                
                # Download with headers and timeout
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Save PDF
                with open(filepath, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                
                print("Done")
                
                # Short delay between downloads to be respectful
                time.sleep(0.5)
                
            except requests.RequestException as e:
                print(f"Failed: {str(e)}")
                continue
            
    print("\nDownload complete! PDFs saved to:", os.path.abspath(output_folder))

if __name__ == "__main__":
    # Download PDFs from the CSV file
    download_frq_pdfs('ap_cs_frq_links.csv')