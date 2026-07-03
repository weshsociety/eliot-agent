import json

enquetes = [
    {
        "id": "herboristerie_france",
        "label": "HERBORISTERIE INTERDITE",
        "name": "Herboristerie — L'interdiction française et le Capitulaire de Villis",
        "desc": "Pourquoi l'herboristerie est interdite en France? Traçage du Capitulaire de Villis (813) → contrôle des savoirs botaniques → monopole pharmaceutique moderne.",
        "type": "investigation",
        "status": "en_fermentation",
        "x": -300,
        "y": 200,
        "r": 16
    },
    {
        "id": "1984_orwell",
        "label": "1984 — ORWELL",
        "name": "1984 de Orwell — Blueprint pour contrôle total",
        "desc": "Analyse: Newspeak, Doublethink, Ministère de la Vérité. Parallèles avec surveillance numérique, désinformation d'état, contrôle narratif 2026.",
        "type": "investigation",
        "status": "en_fermentation",
        "x": 300,
        "y": 200,
        "r": 16
    },
    {
        "id": "mk_ultra_minority_report",
        "label": "MK-ULTRA × MINORITY REPORT",
        "name": "MK-Ultra rencontre Minority Report — Prédiction et contrôle",
        "desc": "MK-Ultra (1950s) programmation mentale. Minority Report (2002) vision prédictive. Convergence: IA + neurotechnologies + intervention préventive.",
        "type": "investigation",
        "status": "en_fermentation",
        "x": 0,
        "y": -250,
        "r": 16
    },
    {
        "id": "protocole_toronto",
        "label": "PROTOCOLE DE TORONTO",
        "name": "Protocole de Toronto — Neurodroits et transhumanisme",
        "desc": "2021: Framework pour neurotechnologies. Droits mentaux. Modification cognitive consensuelle. Frontière éthique droit-technologie.",
        "type": "investigation",
        "status": "en_fermentation",
        "x": 100,
        "y": -300,
        "r": 15
    }
]

with open('/home/eliot/octopus-agent/data/octopus_data.json', 'r') as f:
    data = json.load(f)

data['nodes'].extend(enquetes)

with open('/home/eliot/octopus-agent/data/octopus_data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ {len(enquetes)} enquêtes ajoutées")
