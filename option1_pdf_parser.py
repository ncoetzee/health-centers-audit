import pdfplumber
import pandas as pd
import os
import re

def extract_financials_from_pdf(pdf_path):
    # This is a generic parser placeholder. Real audit PDFs vary wildly in format 
    # as they are created by different independent auditors.
    metrics = {
        "Total Assets": None,
        "Current Assets": None,
        "Total Liabilities": None,
        "Current Liabilities": None,
        "Net Assets": None,
        "Operating Revenue": None
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            # Scanning first 25 pages for balance sheet
            for page in pdf.pages[:25]:
                text += page.extract_text() + "\n"
            def parse_val(match):
                if not match: return None
                try:
                    val = match.group(1).replace(',', '').strip()
                    if not val or val == '.': return None
                    return float(val)
                except ValueError:
                    return None

            # Naive regex extraction (very brittle in practice for varying PDF layouts)
            assets = re.search(r'Total\s+Assets[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Total Assets'] = parse_val(assets)
                
            curr_assets = re.search(r'Total\s+Current\s+Assets[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Current Assets'] = parse_val(curr_assets)
            
            liab = re.search(r'Total\s+Liabilities[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Total Liabilities'] = parse_val(liab)
            
            curr_liab = re.search(r'Total\s+Current\s+Liabilities[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Current Liabilities'] = parse_val(curr_liab)
            
            net_assets = re.search(r'Net\s+Assets[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Net Assets'] = parse_val(net_assets)
            
            op_rev = re.search(r'Operating\s+Revenue[\s\.\$\_]*([0-9][\d,\.]*)', text, re.IGNORECASE)
            metrics['Operating Revenue'] = parse_val(op_rev)
            
            # Attempt to intelligently extract the Entity Name from the text
            entity_match = re.search(r'(?:Auditee Name|Name of Entity|Name of Auditee)[\s\:\.]*([A-Za-z0-9\s\,\.\-]+(?:\n[A-Za-z0-9\s\,\.\-]+)?)', text, re.IGNORECASE)
            if entity_match and len(entity_match.group(1)) > 5:
                # Clean up if it grabbed too much
                metrics['Entity Name'] = entity_match.group(1).split('\n')[0].strip()
            else:
                # Blanket fallback: grab the first prominent lines of the first page
                first_page = pdf.pages[0].extract_text()
                if first_page:
                    lines = [line.strip() for line in first_page.split('\n') if len(line.strip()) > 5 and 'table of contents' not in line.lower() and 'report' not in line.lower()]
                    metrics['Entity Name'] = " | ".join(lines[:2]) if lines else "Unknown Entity"
                else:
                    metrics['Entity Name'] = "Unknown Entity"
            
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        
    return metrics

def process_all_pdfs(pdf_dir):
    data = []
    if not os.path.exists(pdf_dir):
        print(f"Please exact the FAC zip into the '{pdf_dir}' directory first.")
        return
        
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            print(f"Processing {filename}...")
            metrics = extract_financials_from_pdf(os.path.join(pdf_dir, filename))
            # Put Entity Name as the first column, but keep filename for debug tracing
            row = {'Entity Name': metrics.get('Entity Name', 'Unknown Entity')}
            for k, v in metrics.items():
                if k != 'Entity Name':
                    row[k] = v
            row['Filename'] = filename
            data.append(row)
            
    df = pd.DataFrame(data)
    # Calculate ratios
    if not df.empty and 'Current Assets' in df and 'Current Liabilities' in df:
        df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities']
        
    try:
        df.to_csv("fac_pdf_extracted_ratios.csv", index=False)
        print("\nSUCCESS! Saved PDF extracted data to 'fac_pdf_extracted_ratios.csv'")
    except PermissionError:
        fallback_name = "fac_pdf_extracted_ratios_UPDATED.csv"
        df.to_csv(fallback_name, index=False)
        print(f"\nSUCCESS! Couldn't overwrite the original file (it might be open in Excel), so I saved the new data to '{fallback_name}' instead.")

if __name__ == "__main__":
    process_all_pdfs("fac_pdfs")
