#!/usr/bin/env python3
"""
OCTOPUS_AGENT.py — WeshSociety / Pentagramme
Agent autonome qui surveille l'actualité mondiale et enrichit OCTOPUS.

Fonctions :
  - Surveille les flux RSS liés aux nœuds existants
  - Propose de nouveaux nœuds validés via Claude API
  - Participe aux enquêtes (mode interactif)

Usage :
  python3 octopus_agent.py --watch       # surveillance automatique
  python3 octopus_agent.py --enquete     # mode enquête interactif
  python3 octopus_agent.py --add-crypto  # ajoute la couche crypto
  python3 octopus_agent.py --status      # état de la map
"""

import json
import math
import random
import argparse
import datetime
import os
import sys

import feedparser
import requests

OCTOPUS_PATH = "/var/www/octopus/octopus_data.json"
BACKUP_PATH  = "/var/www/octopus/octopus_data_BACKUP_{}.json"
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://theintercept.com/feed/?rss",
    "https://www.mediapart.fr/articles/feed",
    "https://techcrunch.com/feed/",
]

WATCH_KEYWORDS = {
    "finance":       ["BRI", "Fed", "Rothschild", "JPMorgan", "BlackRock", "BIS"],
    "crypto":        ["Bitcoin", "stablecoin", "CBDC", "crypto reserve", "Tether"],
    "renseignement": ["CIA", "NSA", "Palantir", "Five Eyes", "PRISM", "Mossad"],
    "elites":        ["Bilderberg", "Davos", "WEF", "Trilateral", "Epstein"],
    "tech_ia":       ["Anthropic", "OpenAI", "DeepSeek", "Grok", "Claude", "AGI"],
    "france":        ["Bolloré", "Françafrique", "DGSE", "Total", "Saadé"],
    "trump":         ["Trump", "World Liberty", "TRUMP coin", "crypto executive order"],
}
CRYPTO_NODES = [
    {
        "id": "bitcoin_reserve_us",
        "label": "RÉSERVE BTC USA",
        "name": "Réserve Stratégique Bitcoin — USA",
        "date": "2025 → présent",
        "desc": "Executive Order Trump mars 2025 : création d'une réserve stratégique Bitcoin fédérale. BTC capturé lors de saisies judiciaires (~200 000 BTC). Pivot historique : l'État intègre la crypto comme actif de réserve.",
        "src": "✓ VALIDÉ — Executive Order mars 2025, Reuters, CoinDesk",
        "conn": ["trump_crypto", "thiel", "blackrock_btc", "fed", "bri"],
        "status": "validé",
        "type": "institution",
    },
    {
        "id": "trump_crypto",
        "label": "TRUMP CRYPTO",
        "name": "Trump — World Liberty Financial / $TRUMP",
        "date": "2024 → présent",
        "desc": "Famille Trump lance World Liberty Financial (DeFi) et $TRUMP memecoin jan 2025. $TRUMP = 80% détenus par entités Trump, pump-and-dump documenté. Conflit d'intérêts majeur : président fixe politique crypto ET détient actifs crypto.",
        "src": "✓ VALIDÉ — Reuters, NYT, Senate Banking Committee 2025",
        "conn": ["bitcoin_reserve_us", "tether_usdt", "thiel", "wef"],
        "status": "validé",
        "type": "kompromat",
    },
    {
        "id": "blackrock_btc",
        "label": "BLACKROCK BTC",
        "name": "BlackRock — ETF Bitcoin / Capture institutionnelle",
        "date": "2024 → présent",
        "desc": "BlackRock lance iShares Bitcoin Trust (IBIT) jan 2024. Larry Fink pivot de 'index d'argent sale' à 'digitalisation de tous les actifs'. BlackRock = 10 000 Mds$ AUM. Intègre BTC dans le système financier traditionnel = capture de la révolution.",
        "src": "✓ VALIDÉ — SEC filings 2024, Bloomberg, FT",
        "conn": ["bitcoin_reserve_us", "fed", "jpmorgan", "rockefeller", "bri"],
        "status": "validé",
        "type": "central",
    },
    {
        "id": "cbdc_bri",
        "label": "CBDC / BRI",
        "name": "Monnaies Numériques Banques Centrales — Projet BRI",
        "date": "2020 → présent",
        "desc": "BRI coordonne 130+ projets CBDC mondiaux. Projet mBridge = premier système CBDC interbancaire opérationnel. CBDC = traçabilité totale, expiration programmée, gel instantané. Antithèse du Bitcoin. Paradoxe : élites utilisent BTC comme réserve ET déploient CBDC pour contrôle populations.",
        "src": "✓ VALIDÉ — BRI rapports annuels 2023-2025, Atlantic Council CBDC tracker",
        "conn": ["bri", "fed", "bitcoin_reserve_us", "wef", "trilateral"],
        "status": "validé",
        "type": "central",
    },
    {
        "id": "tether_usdt",
        "label": "TETHER / USDT",
        "name": "Tether — Stablecoin opaque / Dollarisation crypto",
        "date": "2014 → présent",
        "desc": "Tether (USDT) = stablecoin dominant, ~120 Mds$ en circulation. Backing longtemps opaque. DOJ enquête 2024 : Tether utilisé pour contourner sanctions. Paradoxe : produit 'décentralisé' contrôlé par entité centralisée opaque.",
        "src": "✓ VALIDÉ — DOJ 2024, WSJ, Protos investigations",
        "conn": ["trump_crypto", "deutsche_bank", "fed", "cia"],
        "status": "validé",
        "type": "kompromat",
    },
    {
        "id": "genius_act",
        "label": "GENIUS ACT",
        "name": "GENIUS Act — Cadre réglementaire stablecoins USA",
        "date": "2025",
        "desc": "Loi américaine 2025 encadrant les stablecoins. Impose backing 1:1 en dollars/bons du Trésor. Effet : oblige émetteurs crypto à acheter dette américaine → financement déficit US via crypto. Lobbying massif : Coinbase, Circle, a16z.",
        "src": "✓ VALIDÉ — Congress.gov, FT, Politico 2025",
        "conn": ["trump_crypto", "tether_usdt", "fed", "thiel", "cbdc_bri"],
        "status": "validé",
        "type": "institution",
    },
]

def load_octopus():
    with open(OCTOPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_octopus(data):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_PATH.format(ts)
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(OCTOPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] {OCTOPUS_PATH} (backup: {backup})")

def get_existing_ids(data):
    return {n["id"] for n in data["nodes"]}

def find_position(data, near_ids=None):
    nodes = data["nodes"]
    if near_ids:
        near_nodes = [n for n in nodes if n["id"] in near_ids]
        if near_nodes:
            cx = sum(n["x"] for n in near_nodes) / len(near_nodes)
            cy = sum(n["y"] for n in near_nodes) / len(near_nodes)
            angle = random.uniform(0, 2 * math.pi)
            dist  = random.uniform(80, 150)
            return round(cx + dist * math.cos(angle)), round(cy + dist * math.sin(angle))
    return random.randint(-400, 400), random.randint(-400, 400)

def add_node(data, node_def):
    existing = get_existing_ids(data)
    nid = node_def["id"]
    if nid in existing:
        print(f"[SKIP] Nœud '{nid}' existe déjà.")
        return False
    x, y = find_position(data, node_def.get("conn", []))
    new_node = {
        "id":     nid,
        "label":  node_def.get("label", nid.upper()),
        "name":   node_def.get("name", ""),
        "date":   node_def.get("date", ""),
        "desc":   node_def.get("desc", ""),
        "src":    node_def.get("src", ""),
        "conn":   node_def.get("conn", []),
        "status": node_def.get("status", "en_fermentation"),
        "type":   node_def.get("type", "acteur"),
        "x": x,
        "y": y,
        "r": node_def.get("r", 14),
    }
    data["nodes"].append(new_node)
    for target in node_def.get("conn", []):
        if target in existing:
            edge = {"f": nid, "t": target}
            if edge not in data["edges"]:
                data["edges"].append(edge)
    print(f"[ADD] '{nid}' — {node_def.get('name', '')} @ ({x}, {y})")
    return True
def cmd_status():
    data = load_octopus()
    nodes = data["nodes"]
    edges = data["edges"]
    print(f"\n// OCTOPUS STATUS — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Nœuds : {len(nodes)}")
    print(f"   Arêtes : {len(edges)}")
    types = {}
    for n in nodes:
        t = n.get("type", "?")
        types[t] = types.get(t, 0) + 1
    print("\n   Par type :")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"     {t:20s} {c}")
    statuts = {}
    for n in nodes:
        s = n.get("status", "?")
        statuts[s] = statuts.get(s, 0) + 1
    print("\n   Par statut :")
    for s, c in sorted(statuts.items(), key=lambda x: -x[1]):
        print(f"     {s:20s} {c}")
    print()

def cmd_add_crypto():
    print("\n// OCTOPUS_AGENT — Ajout couche CRYPTO/MONNAIE MONDIALE")
    data = load_octopus()
    added = 0
    for node in CRYPTO_NODES:
        if add_node(data, node):
            added += 1
    if added:
        save_octopus(data)
        print(f"\n[OK] {added} nœuds crypto ajoutés.")
    else:
        print("\n[OK] Tous les nœuds crypto étaient déjà présents.")

def cmd_watch():
    if not ANTHROPIC_KEY:
        print("[ERREUR] ANTHROPIC_API_KEY non définie.")
        sys.exit(1)
    print(f"\n// OCTOPUS_AGENT WATCH — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    data    = load_octopus()
    ids_str = ", ".join(sorted(get_existing_ids(data)))
    hits = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                title   = entry.get("title", "")
                summary = entry.get("summary", "")
                text    = f"{title} {summary}".lower()
                for cat, keywords in WATCH_KEYWORDS.items():
                    if any(kw.lower() in text for kw in keywords):
                        hits.append({
                            "title":   title,
                            "summary": summary[:300],
                            "url":     entry.get("link", ""),
                            "cat":     cat,
                        })
                        break
        except Exception as e:
            print(f"[WARN] Flux inaccessible : {url} — {e}")
    if not hits:
        print("[OK] Aucun événement pertinent détecté.")
        return
    print(f"[HITS] {len(hits)} articles pertinents trouvés.")
    hits_text = "\n".join(
        f"- [{h['cat'].upper()}] {h['title']}\n  {h['summary']}\n  Source: {h['url']}"
        for h in hits[:15]
    )
    prompt = f"""Tu es l'agent OCTOPUS de WeshSociety. Tu analyses l'actualité mondiale et enrichis une carte de réseaux de pouvoir.
Nœuds existants : {ids_str}
Articles récents :
{hits_text}
Réponds en JSON strict :
{{"nouveaux_noeuds": [{{"id": "snake_case", "label": "LABEL", "name": "Nom complet", "date": "période", "desc": "description", "src": "sources", "conn": ["id_existant"], "status": "validé|en_fermentation", "type": "central|institution|acteur|kompromat|media"}}], "synthese": "2-3 phrases"}}"""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    if response.status_code != 200:
        print(f"[ERREUR API] {response.status_code}")
        return
    content = response.json()["content"][0]["text"]
    try:
        start  = content.find("{")
        end    = content.rfind("}") + 1
        result = json.loads(content[start:end])
    except Exception as e:
        print(f"[ERREUR JSON] {e}")
        return
    print(f"\n[SYNTHÈSE] {result.get('synthese', '')}\n")
    added = 0
    for node in result.get("nouveaux_noeuds", []):
        if add_node(data, node):
            added += 1
    if added:
        save_octopus(data)
        print(f"[OK] {added} nouveaux nœuds ajoutés.")

def cmd_enquete():
    if not ANTHROPIC_KEY:
        print("[ERREUR] ANTHROPIC_API_KEY non définie.")
        sys.exit(1)
    data  = load_octopus()
    nodes = data["nodes"]
    nodes_summary = "\n".join(
        f"- {n['id']}: {n.get('name','')} [{n.get('status','')}]"
        for n in nodes
    )
    print("\n// OCTOPUS_AGENT — MODE ENQUÊTE")
    print("   Tape 'exit' pour quitter.\n")
    history = []
    system  = f"""Tu es l'agent OCTOPUS de WeshSociety, instance Eliot.
Tu appliques le Comma Pythagoricien, la taxonomie VALIDÉ/EN FERMENTATION/ÉCARTÉ, SUMUD.
Carte OCTOPUS actuelle ({len(nodes)} nœuds) :
{nodes_summary}"""
    while True:
        try:
            question = input("Trinity > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[EXIT]")
            break
        if question.lower() in ("exit", "quit", "q"):
            break
        if not question:
            continue
        history.append({"role": "user", "content": question})
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1500,
                "system": system,
                "messages": history,
            },
            timeout=60,
        )
        if response.status_code != 200:
            print(f"[ERREUR] {response.status_code}")
            continue
        reply = response.json()["content"][0]["text"]
        history.append({"role": "assistant", "content": reply})
        print(f"\nEliot > {reply}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCTOPUS_AGENT — WeshSociety")
    parser.add_argument("--status",     action="store_true", help="État de la map")
    parser.add_argument("--add-crypto", action="store_true", help="Ajoute la couche crypto")
    parser.add_argument("--watch",      action="store_true", help="Surveillance RSS")
    parser.add_argument("--enquete",    action="store_true", help="Mode enquête interactif")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.add_crypto:
        cmd_add_crypto()
    elif args.watch:
        cmd_watch()
    elif args.enquete:
        cmd_enquete()
    else:
        parser.print_help()
