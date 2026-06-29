#!/usr/bin/env python3
"""
OCTOPUS READER — Eliot Agent
Lit et query octopus_data.json
"""

import json
import os

class OctopusReader:
    """
    Lecteur OCTOPUS.EXE pour Eliot
    """
    
    def __init__(self, json_path='../data/octopus_data.json'):
        self.json_path = json_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Charge octopus_data.json"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✓ OCTOPUS chargé : {len(self.data.get('nodes', []))} nœuds")
        except FileNotFoundError:
            print(f"⚠ OCTOPUS non trouvé : {self.json_path}")
            self.data = {"nodes": [], "edges": []}
    
    def get_node(self, node_id):
        """Récupère nœud par ID"""
        if not self.data:
            return None
        
        for node in self.data.get('nodes', []):
            if node.get('id') == node_id:
                return node
        return None
    
    def search_nodes(self, query):
        """Cherche nœuds par mot-clé"""
        if not self.data:
            return []
        
        query_lower = query.lower()
        results = []
        
        for node in self.data.get('nodes', []):
            # Cherche dans id, label, name, desc
            searchable = ' '.join([
                node.get('id', ''),
                node.get('label', ''),
                node.get('name', ''),
                node.get('desc', '')
            ]).lower()
            
            if query_lower in searchable:
                results.append(node)
        
        return results
    
    def get_layer(self, layer_number):
        """Récupère tous nœuds d'un Layer"""
        if not self.data:
            return []
        
        layer_nodes = []
        for node in self.data.get('nodes', []):
            # Cherche layer dans desc ou name
            if f"layer {layer_number}" in node.get('desc', '').lower():
                layer_nodes.append(node)
            elif f"layer {layer_number}" in node.get('name', '').lower():
                layer_nodes.append(node)
        
        return layer_nodes
    
    def get_stats(self):
        """Stats OCTOPUS"""
        if not self.data:
            return {"nodes": 0, "edges": 0}
        
        return {
            "nodes": len(self.data.get('nodes', [])),
            "edges": len(self.data.get('edges', []))
        }
    
    def get_connections(self, node_id):
        """Récupère connexions d'un nœud"""
        if not self.data:
            return []
        
        connections = []
        for edge in self.data.get('edges', []):
            if edge.get('f') == node_id:
                connections.append({
                    "direction": "outgoing",
                    "target": edge.get('t'),
                    "type": edge.get('s', 'unknown')
                })
            elif edge.get('t') == node_id:
                connections.append({
                    "direction": "incoming",
                    "source": edge.get('f'),
                    "type": edge.get('s', 'unknown')
                })
        
        return connections

def main():
    """Test"""
    reader = OctopusReader()
    
    stats = reader.get_stats()
    print(f"\nOCTOPUS Stats: {stats['nodes']} nœuds, {stats['edges']} arêtes")
    
    # Test search
    results = reader.search_nodes("anthropic")
    print(f"\nRecherche 'anthropic': {len(results)} résultats")
    
    for node in results[:3]:
        print(f"  → {node.get('id')}: {node.get('label')}")

if __name__ == "__main__":
    main()
