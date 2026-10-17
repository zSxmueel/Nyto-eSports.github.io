import json
import urllib.request
from bs4 import BeautifulSoup

URLS = {
    "ecl": "https://eafcstats.es/competitions/271",
    "vpcl": "https://eafcstats.es/competitions/267",
    "afj": "https://eafcstats.es/competitions/256"
}

def fetch_ranking(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        teams = []
        rows = soup.find_all('tr')
        pos = 1
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = cols[1].text.strip()
                pj = int(cols[2].text.strip() or 0)
                dg = int(cols[3].text.strip() or 0)
                pts = int(cols[4].text.strip() or 0) if len(cols) > 4 else 0
                is_nyto = "nyto" in name.lower()
                teams.append({"pos": pos, "name": name, "pj": pj, "dg": dg, "pts": pts, "isNyto": is_nyto})
                pos += 1
        return teams
    except Exception as e:
        print(f"Error cargando {url}: {e}")
        return []

data = {}
for league, url in URLS.items():
    teams = fetch_ranking(url)
    if teams:
        data[league] = teams

if data:
    with open('clasificaciones.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Clasificaciones actualizadas con éxito.")
