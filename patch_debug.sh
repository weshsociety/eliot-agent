#!/bin/bash

# Sauvegarde le fichier original
cp octopus_agent.py octopus_agent.py.bak

# Ajoute du debug APRÈS la ligne qui reçoit la réponse Claude
sed -i '/content = response.json()\["content"\]\[0\]\["text"\]/a\    print(f"[DEBUG_RESPONSE] Length: {len(content)}")\n    print(f"[DEBUG_RESPONSE] Content:\\n{content}\\n---END---\\n")' octopus_agent.py

echo "✅ Patch appliqué"
echo "Backup: octopus_agent.py.bak"

