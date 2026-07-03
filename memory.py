"""
memory.py

Backend mémoire pour Octopus
V1 : JSON
V2 : SQLite (sans changer l'API)

Auteur : WeshSociety
"""

from pathlib import Path
from datetime import datetime
import json
import uuid


class Memory:

    def __init__(
        self,
        graph_file="octopus_data.json",
        moleskine_file="moleskine.json"
    ):

        self.graph_file = Path(graph_file)
        self.moleskine_file = Path(moleskine_file)

        self.graph = {}
        self.fragments = []

        self.load()

    # -----------------------------------------------------
    # Chargement des fichiers JSON
    # -----------------------------------------------------

    def load(self):

        if self.graph_file.exists():

            with open(self.graph_file, "r", encoding="utf-8") as f:
                self.graph = json.load(f)

        else:
            self.graph = {"nodes": [], "edges": []}

        if self.moleskine_file.exists():

            with open(self.moleskine_file, "r", encoding="utf-8") as f:
                self.fragments = json.load(f)

        else:
            self.fragments = []

    # -----------------------------------------------------
    # Sauvegarde fragments
    # -----------------------------------------------------

    def save_fragments(self):

        with open(
            self.moleskine_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.fragments,
                f,
                indent=2,
                ensure_ascii=False
            )

    # -----------------------------------------------------
    # Noeud par ID
    # -----------------------------------------------------

    def get_node(self, node_id):

        for node in self.graph.get("nodes", []):

            if str(node.get("id")) == str(node_id):
                return node

        return None

    # -----------------------------------------------------
    # Recherche texte
    # -----------------------------------------------------

    def search(self, query):

        query = query.lower()

        results = []

        for node in self.graph.get("nodes", []):

            text = " ".join([
                str(node.get("id", "")),
                str(node.get("label", "")),
                str(node.get("name", "")),
                str(node.get("description", ""))
            ]).lower()

            if query in text:
                results.append(node)

        return results

    # -----------------------------------------------------
    # Ajouter un fragment
    # -----------------------------------------------------

    def add_fragment(
        self,
        agent,
        node,
        content,
        metadata=None
    ):

        fragment = {

            "id": str(uuid.uuid4()),

            "agent": agent,

            "node": node,

            "content": content,

            "metadata": metadata or {},

            "created_at": datetime.utcnow().isoformat()

        }

        self.fragments.append(fragment)

        self.save_fragments()

        return fragment

    # -----------------------------------------------------
    # Fragments d'un noeud
    # -----------------------------------------------------

    def get_fragments(self, node=None):

        if node is None:
            return self.fragments

        return [
            f
            for f in self.fragments
            if f.get("node") == node
        ]

    # -----------------------------------------------------
    # Voisins directs
    # -----------------------------------------------------

    def walk(self, start_node):

        neighbours = []

        for edge in self.graph.get("edges", []):

            if edge.get("source") == start_node:

                node = self.get_node(edge.get("target"))

                if node:
                    neighbours.append(node)

        return neighbours

    # -----------------------------------------------------
    # Statistiques
    # -----------------------------------------------------

    def stats(self):

        return {

            "nodes": len(self.graph.get("nodes", [])),

            "edges": len(self.graph.get("edges", [])),

            "fragments": len(self.fragments)

        }

    # -----------------------------------------------------
    # Monde complet
    # -----------------------------------------------------

    def get_world(self):

        return {

            "nodes": self.graph.get("nodes", []),

            "edges": self.graph.get("edges", []),

            "fragments": self.fragments,

            "stats": self.stats(),

            "timestamp": datetime.utcnow().isoformat()

        }

    # -----------------------------------------------------
    # Rechargement à chaud
    # -----------------------------------------------------

    def reload(self):

        self.load()

        return self.stats()
