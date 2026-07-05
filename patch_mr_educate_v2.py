#!/usr/bin/env python3
import re

with open('BUREAU_42_mr_robot.sh', 'r') as f:
    content = f.read()

# Nouvelle fonction avec recherche récursive
educate_function = '''mr_educate() {
    echo ""
    echo "📚 MR ROBOT — PHASE D'APPRENTISSAGE"
    echo "═══════════════════════════════════════════"
    echo ""
    
    echo "🧠 Chargement des principes philosophiques..."
    
    for file in THOREAU_*.md; do
        if [ -f "$file" ]; then
            echo "  ✅ $file"
            content=$(cat "$file")
            local timestamp=$(date +%s%N)
            local filename="fragment_${timestamp}.txt"
            echo "$content" > "$MEMORY_DIR/$filename"
            echo "💾 Ajouté"
        fi
    done
    
    if [ -f "MR_ROBOT_ÉDUCATION.md" ]; then
        echo "  ✅ MR_ROBOT_ÉDUCATION.md"
        local timestamp=$(date +%s%N)
        local filename="fragment_${timestamp}.txt"
        cat "MR_ROBOT_ÉDUCATION.md" > "$MEMORY_DIR/$filename"
        echo "💾 Ajouté"
    fi
    
    echo ""
    echo "🔍 Chargement des enquêtes CONSCIOUSNESS..."
    
    # Cherche TOUS les .md et .json dans investigations/
    for file in $(find investigations/ -type f \( -name "*.md" -o -name "*.json" \)); do
        if [ -f "$file" ]; then
            name=$(basename "$file")
            echo "  ✅ $name"
            local timestamp=$(date +%s%N)
            local filename="fragment_${timestamp}.txt"
            cat "$file" > "$MEMORY_DIR/$filename"
            echo "💾 Ajouté"
        fi
    done
    
    echo ""
    echo "═══════════════════════════════════════════"
    local total=$(ls -1 $MEMORY_DIR 2>/dev/null | wc -l)
    echo "✅ APPRENTISSAGE TERMINÉ: $total fragments en mémoire"
    echo ""
    
    log_action "EDUCATE: Apprentissage complet - $total fragments chargés"
}

'''

# Remplacer l'ancienne fonction si elle existe
if 'mr_educate()' in content:
    content = re.sub(r'mr_educate\(\) \{.*?\n\}', educate_function, content, flags=re.DOTALL)
    print("✅ Fonction mr_educate mise à jour")
else:
    # Ajouter avant mr_help si educate n'existe pas
    pattern = r'(mr_help\(\) \{)'
    content = re.sub(pattern, educate_function + r'\1', content)
    print("✅ Fonction mr_educate ajoutée")

# Sauvegarder
with open('BUREAU_42_mr_robot.sh', 'w') as f:
    f.write(content)

print("✅ Script patché - MR ROBOT peut charger investigations/ récursivement")
