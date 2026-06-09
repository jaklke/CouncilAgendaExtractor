import sys
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import win32clipboard

def extraheer_zitting_data(url):
    print("Browser opstarten en pagina laden...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        print("Wachten tot de agendapunten dynamisch zijn ingeladen...")
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        html_content = page.content()
        browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    html_output = ""
    
    # Zoek hoofdtitel (negeer "terug" knoppen)
    hoofdtitels = soup.find_all(['h1', 'h2'])
    zitting_titel = "Zitting Gemeenteraad"
    for t in hoofdtitels:
       txt = t.get_text(strip=True)
       if txt and "terug" not in txt.lower():
           zitting_titel = txt
           break
            
    html_output += f"<h1>{zitting_titel}</h1>\n\n"
    
    # Zoek alle overkoepelende themakoppen (h3)
    themakoppen = soup.find_all('h3')
    
    for kop in themakoppen:
        thema_tekst = kop.get_text(strip=True)
        if "terug" in thema_tekst.lower() or len(thema_tekst) < 3:
            continue
            
        volgend_element = kop.find_next_sibling()
        if not volgend_element:
            continue
            
        # Vind alle individuele agendapunten binnen de lijst onder de h3
        agendapunten = volgend_element.find_all('li', class_='agendapage')
        
        html_output += f"<h2>{thema_tekst}</h2>\n"

        for punt in agendapunten:
            titel_elem = punt.find('a', class_='title')
            if not titel_elem:
                titel_elem = punt.find(['h4', 'div'], class_='title')
                
            if not titel_elem:
                continue
                
            titel_tekst = titel_elem.get_text(strip=True)
            
            # Elk item wordt een Heading 2 in Confluence
            html_output += f"<h3>{titel_tekst}</h3>\n"
            
            # Zoek de summary container binnen dit lijstitem
            summary_div = punt.find('div', class_='summary')
            
            if summary_div:
                # AANPASSING: Neem de volledige HTML-inhoud inclusief alle tags (p, ul, li, etc.)
                # zonder de div-container zelf mee te kopiëren
                html_output += summary_div.decode_contents()
            else:
                html_output += "<p><em>Geen publieke tekst of besluitvorming beschikbaar voor dit punt.</em></p>\n"
                
            html_output += "\n\n"  # Ruimte tussen de punten
            
    return html_output

def kopieer_naar_windows_html_klembord(html_fragment):
    marker_start = 105
    marker_end = marker_start + len(html_fragment)
    
    cf_html_header = (
        "Version:0.9\r\n"
        f"StartHTML:{marker_start:08d}\r\n"
        f"EndHTML:{marker_end:08d}\r\n"
        f"StartFragment:{marker_start:08d}\r\n"
        f"EndFragment:{marker_end:08d}\r\n"
    )
    
    volledige_data = cf_html_header + html_fragment
    
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        cf_html_format = win32clipboard.RegisterClipboardFormat("HTML Format")
        win32clipboard.SetClipboardData(cf_html_format, volledige_data.encode("utf-8"))
        print("Succesvol naar het Windows-klembord geschreven als HTML-opmaak!")
    finally:
        win32clipboard.CloseClipboard()


# --- LOGICA VOOR ARGUMENTEN VIA TERMINAL ---
if __name__ == "__main__":
    # sys.argv[0] is altijd de naam van het script zelf (run.py)
    # sys.argv[1] is het eerste argument dat daarna komt
    if len(sys.argv) < 2:
        print("Fout: Geen URL meegegeven.")
        print("Gebruik: python run.py <URL_VAN_DE_ZITTING>")
        sys.exit(1)
        
    # Haal de URL op uit het terminal-argument
    url_zitting = sys.argv[1]
    
    # Voer het script uit met het meegegeven argument
    resultaat_html = extraheer_zitting_data(url_zitting)
    kopieer_naar_windows_html_klembord(resultaat_html)
    print("\nKlaar! U kunt de tekst met Ctrl+V in Confluence plakken.")

