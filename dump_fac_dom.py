from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://app.fac.gov/dissemination/search/")
    time.sleep(3)
    
    # Perform empty search to bring up results
    page.click("#fac-search")
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except:
        pass
    time.sleep(5)
    
    html = page.evaluate('''() => {
        let links = Array.from(document.querySelectorAll('a[href], button'));
        return links.map(el => {
            if (el.tagName === 'A') return `LINK: ${el.href} CLASS: ${el.className} HTML: ${el.innerHTML.substring(0,100)}`;
            return `BUTTON: ${el.id} CLASS: ${el.className} HTML: ${el.innerHTML.substring(0,100)}`;
        }).join("\\n");
    }''')
    
    with open("detailed_links.txt", "w", encoding="utf-8") as f:
        f.write(html)
