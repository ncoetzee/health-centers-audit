from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://app.fac.gov/dissemination/search/")
    time.sleep(3)
    
    print("Initial URL:", page.url)
    
    # Attempt to click the actual search button
    try:
        page.locator("button#fac-search").click(timeout=3000)
        time.sleep(5)
    except Exception as e:
        print("Could not click search:", e)
        
    print("Current URL:", page.url)
    print(f"Found {len(page.frames)} frames.")
    
    for i, frame in enumerate(page.frames):
        print(f"\n--- Frame {i}: {frame.url} ---")
        try:
            html = frame.content()
            if 'PDF' in html or 'UEI' in html:
                print("  => CONTAINS 'PDF' or 'UEI'")
                
                # Check how many buttons are in this frame
                buttons = frame.locator('button').count()
                links = frame.locator('a').count()
                print(f"  => Buttons: {buttons}, Links: {links}")
        except Exception as e:
            print("  => Could not read frame:", e)
            
    browser.close()
