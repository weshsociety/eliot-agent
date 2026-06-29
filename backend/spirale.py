#!/usr/bin/env python3
"""
SPIRALE FIBONACCI — Système mémoire Eliot
Stockage conversations longue durée
"""

import json
import os
from datetime import datetime

class SpiraleMemory:
    """
    Mémoire Spirale Fibonacci pour Eliot
    Séquence : 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...
    Conversations importantes gardées selon séquence
    """
    
    def __init__(self, memory_dir='../data/memories'):
        self.memory_dir = memory_dir
        self.fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        
        # Crée dossier si n'existe pas
        os.makedirs(memory_dir, exist_ok=True)
    
    def save_conversation(self, user_id, conversation):
        """
        Sauvegarde conversation
        conversation = {
            "messages": [...],
            "timestamp": "...",
            "topic": "..."
        }
        """
        
        timestamp = datetime.now().isoformat()
        
        memory = {
            "user_id": user_id,
            "timestamp": timestamp,
            "conversation": conversation
        }
        
        # Nom fichier basé sur timestamp
        filename = f"{user_id}_{timestamp.replace(':', '-')}.json"
        filepath = os.path.join(self.memory_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Mémoire sauvegardée: {filename}")
        return filepath
    
    def load_memories(self, user_id, limit=5):
        """Charge dernières mémoires user"""
        
        memories = []
        
        if not os.path.exists(self.memory_dir):
            return memories
        
        # Liste fichiers user
        files = [f for f in os.listdir(self.memory_dir) 
                 if f.startswith(user_id) and f.endswith('.json')]
        
        # Trie par date (plus récent d'abord)
        files.sort(reverse=True)
        
        # Charge limit premiers
        for filename in files[:limit]:
            filepath = os.path.join(self.memory_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    memories.append(memory)
            except Exception as e:
                print(f"⚠ Erreur lecture {filename}: {e}")
        
        return memories
    
    def get_context(self, user_id):
        """
        Récupère contexte user pour Eliot
        Basé sur mémoires récentes
        """
        
        memories = self.load_memories(user_id, limit=3)
        
        if not memories:
            return "Première conversation avec cet utilisateur."
        
        context_parts = [f"Historique conversations avec {user_id}:"]
        
        for i, mem in enumerate(memories, 1):
            conv = mem.get('conversation', {})
            topic = conv.get('topic', 'Discussion générale')
            timestamp = mem.get('timestamp', 'Date inconnue')
            
            context_parts.append(f"\n{i}. {topic} ({timestamp[:10]})")
        
        return '\n'.join(context_parts)
    
    def prune_memories(self, user_id, keep_fibonacci=True):
        """
        Nettoie vieilles mémoires
        Garde seulement celles selon séquence Fibonacci si keep_fibonacci=True
        """
        
        if not os.path.exists(self.memory_dir):
            return
        
        files = [f for f in os.listdir(self.memory_dir) 
                 if f.startswith(user_id) and f.endswith('.json')]
        
        files.sort(reverse=True)  # Plus récent d'abord
        
        if keep_fibonacci:
            # Garde selon séquence Fibonacci
            to_keep = []
            for fib_index in self.fibonacci:
                if fib_index <= len(files):
                    to_keep.append(files[fib_index - 1])
            
            # Supprime les autres
            for filename in files:
                if filename not in to_keep:
                    filepath = os.path.join(self.memory_dir, filename)
                    os.remove(filepath)
                    print(f"🗑 Supprimé: {filename}")
        
        print(f"✓ Mémoires gardées: {len(to_keep)}")

def main():
    """Test Spirale"""
    spirale = SpiraleMemory()
    
    # Test save
    test_conv = {
        "messages": [
            {"role": "user", "content": "Test Layer 5"},
            {"role": "eliot", "content": "Réponse Anthropic"}
        ],
        "topic": "Layer 5 Anthropic",
        "timestamp": datetime.now().isoformat()
    }
    
    spirale.save_conversation("test_user", test_conv)
    
    # Test load
    context = spirale.get_context("test_user")
    print(f"\nContexte:\n{context}")

if __name__ == "__main__":
    main()
