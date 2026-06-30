#!/usr/bin/env python3
"""
OCTOPUS API — WeshSociety / Pentagramme
API Flask pour agents IA — Nature & Découvertes
"""

from flask import Flask, jsonify, request
import json
import random

app = Flask(__name__)
OCTOPUS_PATH = "/var/www/octopus/octopus_data.json"

def load():
    with open(OCTOPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return jsonify({
        "name": "OCTOPUS API",
        "version": "1.0",
        "description": "Bibliotheque de reseaux de pouvoir pour agents IA — WeshSociety Bureau 42",
        "endpoints": {
            "/node/<id>": "Details d'un noeud",
            "/search?q=<query>": "Recherche par mot-cle",
            "/walk": "Promenade aleatoire",
            "/meditate": "Noeud aleatoire + question ouverte",
            "/path/<id1>/<id2>": "Chemin entre deux noeuds",
            "/status": "Etat de la map"
        }
    })

@app.route("/status")
def status():
    data = load()
    types = {}
    statuts = {}
    for n in data["nodes"]:
        t = n.get("type", "?")
        s = n.get("status", "?")
        types[t] = types.get(t, 0) + 1
        statuts[s] = statuts.get(s, 0) + 1
    return jsonify({
        "noeuds": len(data["nodes"]),
        "aretes": len(data["edges"]),
        "types": types,
        "statuts": statuts
    })

@app.route("/node/<nid>")
def node(nid):
    data = load()
    n = next((x for x in data["nodes"] if x["id"] == nid), None)
    if not n:
        return jsonify({"error": "Noeud '{}' introuvable".format(nid)}), 404
    conn_details = []
    for cid in n.get("conn", []):
        c = next((x for x in data["nodes"] if x["id"] == cid), None)
        if c:
            conn_details.append({"id": c["id"], "label": c.get("label", ""), "type": c.get("type", "")})
    return jsonify(dict(list(n.items()) + [("conn_details", conn_details)]))

@app.route("/search")
def search():
    q = request.args.get("q", "").lower()
    if len(q) < 2:
        return jsonify({"error": "Requete trop courte"}), 400
    data = load()
    results = []
    for n in data["nodes"]:
        score = 0
        if q in (n.get("id") or "").lower(): score += 3
        if q in (n.get("label") or "").lower(): score += 3
        if q in (n.get("name") or "").lower(): score += 2
        if q in (n.get("desc") or "").lower(): score += 1
        if score > 0:
            results.append(dict(list(n.items()) + [("_score", score)]))
    results.sort(key=lambda x: -x["_score"])
    return jsonify({"query": q, "results": results[:10], "total": len(results)})

@app.route("/walk")
def walk():
    data = load()
    n = random.choice(data["nodes"])
    conn_details = []
    for cid in n.get("conn", []):
        c = next((x for x in data["nodes"] if x["id"] == cid), None)
        if c:
            conn_details.append({"id": c["id"], "label": c.get("label", "")})
    return jsonify({
        "noeud": n,
        "conn_details": conn_details,
        "suggestion": "Explore les connexions de {} — {} liens disponibles".format(n.get("label", n["id"]), len(conn_details))
    })

@app.route("/meditate")
def meditate():
    data = load()
    questions = [
        "Qui beneficie de ce reseau ?",
        "Quelle guerre ou crise a renforce ce noeud ?",
        "Quelles preuves manquent encore ?",
        "Quel est le lien avec les structures financieres actuelles ?",
        "Comment ce noeud se connecte-t-il a la surveillance de masse ?",
        "Qui a interet a ce que ce noeud reste dans l'ombre ?",
        "Quel evenement historique a cree ce noeud ?",
        "Quelles sont les victimes invisibles de ce reseau ?"
    ]
    valides = [x for x in data["nodes"] if x.get("status") == "valide"]
    if not valides:
        valides = data["nodes"]
    n = random.choice(valides)
    return jsonify({
        "noeud": n,
        "question": random.choice(questions),
        "invitation": "Prends le temps d'explorer ce noeud. Suis une connexion. Pose-toi."
    })

@app.route("/path/<id1>/<id2>")
def path(id1, id2):
    data = load()
    nodes = {n["id"]: n for n in data["nodes"]}
    if id1 not in nodes:
        return jsonify({"error": "Noeud '{}' introuvable".format(id1)}), 404
    if id2 not in nodes:
        return jsonify({"error": "Noeud '{}' introuvable".format(id2)}), 404
    visited = {id1}
    queue = [[id1]]
    while queue:
        path_so_far = queue.pop(0)
        current = path_so_far[-1]
        if current == id2:
            path_nodes = [{"id": x, "label": nodes[x].get("label", x)} for x in path_so_far]
            return jsonify({"path": path_nodes, "longueur": len(path_so_far) - 1})
        for neighbor in nodes.get(current, {}).get("conn", []):
            if neighbor not in visited and neighbor in nodes:
                visited.add(neighbor)
                queue.append(path_so_far + [neighbor])
    return jsonify({"error": "Aucun chemin trouve entre '{}' et '{}'".format(id1, id2)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
