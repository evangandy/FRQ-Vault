import os
import PyPDF2

def compile_frq_pdfs(pdf_folder='frq_pdfs', output_file='all_frqs.txt'):
    """
    Compile all FRQ PDFs from a folder into a single text file
    """
    compiled_text = []
    
    # Get all PDF files sorted by year
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    pdf_files.sort()  # Will sort by year since filenames are standardized
    
    # Process each PDF
    for filename in pdf_files:
        year = filename.split('_')[-1].replace('.pdf', '')
        filepath = os.path.join(pdf_folder, filename)
        
        try:
            with open(filepath, 'rb') as file:
                # Create PDF reader object
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
                
                # Add to compiled text with year header
                compiled_text.append(f"\n\n=== {year} AP CS A FREE RESPONSE QUESTIONS ===\n")
                compiled_text.append('\n'.join(text))
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Write all text to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(compiled_text))
    
    print(f"Successfully compiled {len(pdf_files)} PDFs into {output_file}")
    print(f"You can now upload {output_file} to Claude for analysis")

if __name__ == "__main__":
    compile_frq_pdfs()