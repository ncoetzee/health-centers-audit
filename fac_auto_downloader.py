import os
import time
from playwright.sync_api import sync_playwright

def run_scraper():
    print("\nStarting the Federal Audit Clearinghouse PDF mass-downloader...")
    print("Launching Microsoft Edge via Playwright...\n")
    
    # Setup directory
    download_dir = os.path.join(os.getcwd(), "fac_pdfs")
    os.makedirs(download_dir, exist_ok=True)

    with sync_playwright() as p:
        try:
            # Launch edge, keeping it visible
            browser = p.chromium.launch(channel="msedge", headless=False)
        except Exception as e:
            print("Could not find Microsoft Edge. Launching default Chromium...")
            browser = p.chromium.launch(headless=False)
            
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Navigating to https://app.fac.gov/dissemination/search/...")
        page.goto("https://app.fac.gov/dissemination/search/")
        
        print("\n=======================================================")
        print("IMPORTANT ACTION REQUIRED:")
        print("1. Enter your search criteria (e.g. State: MA, Year: 2023, Health Center).")
        print("2. Click 'Search' to view the audit results table.")
        print("3. Ensure the results table is fully loaded.")
        print("=======================================================\n")
        
        input("PRESS ENTER HERE ONLY WHEN the results table is visible on the page to begin mass download... ")
        
        print("\nScanning page for PDF download links...")
        
        has_next_page = True
        page_num = 1
        total_downloads = 0
        
        while has_next_page:
            print(f"\nScraping Page {page_num}...")
            
            # Wait for any navigations to settle
            try:
                page.wait_for_load_state("networkidle", timeout=3000)
            except Exception:
                pass
            time.sleep(2)  # Extra buffer for rendering
            
            # Robust Strategy: Look for any button/link inside a table row that contains an SVG download icon, 
            # OR has an aria-label/title mentioning 'download' or 'pdf'.
            pdf_elements = page.locator("tbody tr, [role='row']").locator("a, button").filter(
                has=page.locator("svg use[href*='download' i], svg[class*='download' i], svg[data-icon*='download' i]")
            )
            
            # Fallback if SVG locator fails: look for explicit attributes
            if pdf_elements.count() == 0:
                pdf_elements = page.locator("tbody tr, [role='row']").locator(
                    "a[title*='download' i], button[title*='download' i], a[aria-label*='download' i], button[aria-label*='download' i], a[href*='/dissemination/download'], a[href$='.pdf']"
                )
            
            # Second fallback: The last column of the table (if it's exactly 7 columns like your screenshot)
            if pdf_elements.count() == 0:
                pdf_elements = page.locator("tbody tr td:nth-child(7) a, tbody tr td:nth-child(7) button")
            
            count = pdf_elements.count()
            print(f"  Found {count} potential PDF links on this page.")
            
            if count == 0:
                print("  [ERROR] I still couldn't find the buttons! Generating an HTML dump so my AI can inspect the exact code...")
                try:
                    with open("error_dump.html", "w", encoding="utf-8") as f:
                        f.write(page.content())
                    print("  => Saved page HTML to 'error_dump.html'. Please let me know you got this error, and I will read the file to fix it instantly!")
                except Exception as e:
                    print("  => Failed to save HTML dump.")
                break
            
            for i in range(count):
                el = pdf_elements.nth(i)
                try:
                    with page.expect_download(timeout=10000) as download_info:
                        el.click(timeout=3000)
                    download = download_info.value
                    
                    filename = download.suggested_filename
                    if not filename:
                        filename = f"fac_report_page{page_num}_{i}.pdf"
                        
                    download_path = os.path.join(download_dir, filename)
                    download.save_as(download_path)
                    print(f"    -> Successfully Downloaded: {filename}")
                    total_downloads += 1
                    time.sleep(1) # Be nice to their servers
                except Exception as e:
                    print(f"    -> [Skipped] Element {i} wasn't a downloadable file or timed out.")
            
            # Try to go to next page
            next_button = page.locator("button:has-text('Next'), a:has-text('Next'), [aria-label*='Next'], button[aria-label*='Next']")
            if next_button.count() > 0 and next_button.first.is_enabled() and next_button.first.is_visible():
                print("\nClicking next page...")
                try:
                    next_button.first.click()
                    page_num += 1
                except Exception:
                    has_next_page = False
            else:
                has_next_page = False
                
        print(f"\nDone! Successfully downloaded {total_downloads} PDFs to the '{download_dir}' directory.")
        input("Press Enter to close the browser and exit...")
        browser.close()

if __name__ == "__main__":
    run_scraper()
