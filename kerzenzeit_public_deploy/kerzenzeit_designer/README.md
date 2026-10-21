# KERZENZEIT Kerzendesigner (MVP)

Ein erster deutschsprachiger, mobil nutzbarer Web-Prototyp für die Kreativ-Guide-Beilage des DIY-Kerzensets.

## Funktionen

- Auswahl aus 12 Wachsplattenfarben
- Auswahl von zwei Farben aus den 8 empfohlenen Wachsstrangfarben
- 6 Dekorationsstile passend zum Kreativ-Guide
- Vorschau einer schlanken, wabenstrukturierten Kerze
- Download der Designvorschau als SVG
- Download der gewählten Farbkombination als JSON

Die Vorschau ist ein stilisiertes 2D-Modell und keine technische Fertigungszeichnung. Hex-Farben sind Näherungen und sollten vor Veröffentlichung mit den physischen Wachsmustern abgeglichen werden.

## Lokal starten

Python 3.10 oder neuer wird empfohlen.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Der Browser öffnet normalerweise `http://localhost:8501`.

## Online veröffentlichen und QR-Code erstellen

1. Erstelle ein GitHub-Repository und lade `app.py`, `requirements.txt` und `README.md` hoch.
2. Öffne Streamlit Community Cloud und verbinde dein GitHub-Konto.
3. Erstelle eine neue App, wähle das Repository, den Branch und `app.py` als Einstiegspunkt.
4. Nach erfolgreicher Veröffentlichung erhältst du eine öffentliche `*.streamlit.app`-Adresse.
5. Erstelle erst danach den QR-Code für die endgültige URL und teste ihn auf mehreren Mobiltelefonen sowie über Mobilfunk.

Offizielle Bereitstellungsanleitung: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Vor kommerzieller Nutzung ergänzen

- Tatsächliche Produktfotos oder materialgetreu geprüfte Texturen
- Kalibrierung der Farbcodes anhand der freigegebenen Wachsmuster
- Deutsche Datenschutz- und Anbieterinformationen, soweit erforderlich
- Prüfung des QR-Ziels, Datenschutzes und der mobilen Darstellung
- Sicherheitshinweis entsprechend den tatsächlichen Tests der dekorierten Kerzen

## Lizenz

Dieser individuell erstellte Prototyp kann als Ausgangsbasis für das eigene Produkt weiterentwickelt werden. Drittanbieter-Bibliotheken behalten ihre jeweiligen Lizenzen.
