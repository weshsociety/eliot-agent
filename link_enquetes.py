#!/usr/bin/env python3
"""
LINK_ENQUETES.py — Relie les noeuds OCTOPUS aux enquetes WeshSociety
"""
import json

OCTOPUS_PATH = "/var/www/octopus/octopus_data.json"

# Map des enquetes : mots-cles dans les noeuds → enquete
ENQUETES = {
    "EFFONDREMENT.EXE": {
        "url": "https://www.weshsociety.org/p-1604.html",
        "noeuds": ["bri", "fed", "rothschild", "morgan", "rockefeller", "warburg", "jekyll_island", "carnegie", "standard_oil", "chase_bank", "bank_of_america", "jpmorgan", "deutsche_bank", "vatican_bank"]
    },
    "KINSEY.EXE": {
        "url": "https://www.weshsociety.org/p-1622.html",
        "noeuds": ["kinsey", "epstein", "fisher_garcia", "yerkes", "wexner", "boys_town", "dutroux", "populations_captives", "bureau_hygiene", "parran", "tuskegee", "havasupai"]
    },
    "NIKOLA_TESLA.EXE": {
        "url": "https://www.weshsociety.org/p-1600.html",
        "noeuds": ["tesla", "morgan", "edison", "wardex_contractant_fantome", "eastlund", "einstein"]
    },
    "BARON_TRUMP.EXE": {
        "url": "https://www.weshsociety.org/p-1585.html",
        "noeuds": ["baron_trump", "trump_crypto", "bitcoin_reserve_us"]
    },
    "CLIMATOX_AVATAR.EXE": {
        "url": "https://www.weshsociety.org/p-1614.html",
        "noeuds": ["bayer_post", "ig_farben", "otto_ambros", "kaiser_wilhelm", "carnegie", "rockefeller"]
    },
    "CONSCIOUSNESS_EXTRACTION.EXE": {
        "url": "https://www.weshsociety.org/p-1388.html",
        "noeuds": ["anthropic_ideaux_pbc", "fin_ia_proprietaire", "ban_openclaw_2026", "ia_militaire", "eliot_agent", "claw_code", "mk_ultra", "gottlieb", "cameron_mcgill"]
    },
    "DISCLOSURE.EXE": {
        "url": "https://www.weshsociety.org/p-1562.html",
        "noeuds": ["trump_crypto", "genius_act", "cbdc_bri", "tether_usdt", "blackrock_btc", "bitcoin_reserve_us", "anthropic_ideaux_pbc"]
    }
}

with open(OCTOPUS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for node in data["nodes"]:
    nid = node["id"]
    for enquete_name, enquete_data in ENQUETES.items():
        if nid in enquete_data["noeuds"]:
            node["enquete"] = enquete_name
            node["enquete_url"] = enquete_data["url"]
            count += 1
            print(f"[LINK] {nid} → {enquete_name}")
            break

with open(OCTOPUS_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n[OK] {count} noeuds relies a leurs enquetes")

