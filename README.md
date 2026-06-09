# Council Agenda Extractor

Dit Python-script automatiseert het ophalen van agendapunten en besluitvorming van de dynamische raadpleegomgeving (Cipal Schaubroeck). Het script transformeert de data naar rijke HTML-opmaak en plaatst deze direct op het Windows-klembord, zodat de inhoud naadloos en met behoud van lay-out (inclusief titels en opsommingstekens) in Confluence geplakt kan worden.

## Kenmerken

* Dynamische Scraping: Maakt gebruik van Playwright om de door JavaScript gegenereerde inhoud (samenvattingen en besluiten) correct in te laden.
* Structuurbehoud: Converteert hoofdtielemanyveaus en agendapunten naar hiërarchische HTML-titels (h1, h2).
* Volledige Inhoud: Behoudt alle geneste HTML-elementen binnen de samenvattingen, zoals paragrafen en opsommingstekens.
* Windows Clipboard Integratie: Schrijft de output dwingend weg naar het Windows-klembord als HTML Format, waardoor Confluence de opmaak direct herkent bij het plakken (Ctrl+V).

## Vereisten

Dit script vereist een Windows-omgeving (voor de klembord-API) en Python 3.8 of hoger.

## Installatie

1. Kloon de repository of download het run.py bestand naar uw lokale machine.
2. Open de terminal in de projectmap en installeer de vereiste Python-bibliotheken via het volgende commando:
   pip install playwright beautifulsoup4 pywin32
3. Installeer de vereiste browser-binaries voor Playwright met het volgende commando:
   playwright install chromium

## Gebruik

U kunt het script uitvoeren vanuit de terminal door het script aan te roepen met de specifieke URL van de zitting als argument:

python run.py <URL_VAN_DE_ZITTING>

### Voorbeeld van uitvoering

python run.py https://beernem-echo.cipalschaubroeck.be/raadpleegomgeving/zittingen/62f18d90-c9e8-4a69-8ecc-03f3ececcdba

### Plakken in Confluence

1. Wacht tot het script in de terminal meldt: *Succesvol naar het Windows-klembord geschreven als HTML-opmaak!*.
2. Open de gewenste Confluence-pagina in de bewerkmodus.
3. Plaats de cursor op de juiste plek (bijvoorbeeld binnen een sectie of tabelcel) en druk op Ctrl+V.
4. Confluence herkent de opmaak automatisch: titels worden omgezet in echte Confluence-headings en opsommingen worden native lijstitems.

## Hoe het werkt

1. Playwright start een onzichtbare (headless) Chromium-browser en navigeert naar de meegegeven URL.
2. Het script wacht tot het netwerk stilvalt (networkidle) plus een extra buffer van 5 seconden om te garanderen dat de achterliggende API van de raadpleegomgeving alle data heeft ingeladen.
3. BeautifulSoup parseert de pagina och isoleert de themakoppen (h3) and de onderliggende agendapunten (li met klasse agendapage).
4. De titel uit de title-klasse en de volledige inhoud binnen de summary-klasse worden samengevoegd tot een HTML-string.
5. De bibliotheek pywin32 opent het Windows-klembord en registreert de data met de officielle Windows HTML-header, zodat applicaties zoals Confluence weten dat het om opgemaakte tekst gaat.

## Ontwikkeling

Deze tool werd via vibe coding ontwikkeld in samenwerking met Gemini.
