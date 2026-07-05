#!/usr/bin/env python3
import re

# Lire le fichier
with open('BUREAU_42_mr_robot.sh', 'r') as f:
    content = f.read()

# La fonction mr_educate à ajouter
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
            mr_add_fragment "PHILOSOPHIE: $file"
        fi
    done
    
    if [ -f "MR_ROBOT_ÉDUCATION.md" ]; then
        echo "  ✅ MR_ROBOT_ÉDUCATION.md"
        mr_add_fragment "ÉDUCATION: MR_ROBOT_ÉDUCATION.md"
    fi
    
    echo ""
    echo "🔍 Chargement des enquêtes..."
    
    if [ -d "investigations" ]; then
        for enquete in investigations/*.md; do
            if [ -f "$enquete" ]; then
                name=$(basename "$enquete")
                echo "  ✅ $name"
                mr_add_fragment "ENQUÊTE: $name"
            fi
        done
    fi
    
    echo ""
    echo "═══════════════════════════════════════════"
    local total=$(ls -1 $MEMORY_DIR 2>/dev/null | wc -l)
    echo "✅ APPRENTISSAGE TERMINÉ: $total fragments"
    echo ""
    
    log_action "EDUCATE: Apprentissage - $total fragments"
}

'''

# Chercher où insérer (avant mr_help)
pattern = r'(mr_help\(\) \{)'
if re.search(pattern, content):
    content = re.sub(pattern, educate_function + r'\1', content)
    print("✅ Fonction mr_educate ajoutée")
else:
    print("❌ Erreur: mr_help() non trouvé")
    exit(1)

# Ajouter le case statement
case_pattern = r'(case "\$command" in.*?"help"\|"h"\|"\?"\))'
case_statement = '''        "educate")
            mr_educate
            ;;
        '''

if re.search(case_pattern, content, re.DOTALL):
    content = re.sub(case_pattern, r'\1', content, flags=re.DOTALL)
    # Chercher la ligne '"help"' et ajouter avant
    content = re.sub(
        r'(\s+"help"\|"h"\|"\?")',
        case_statement + r'\1',
        content
    )
    print("✅ Case statement 'educate' ajouté")
else:
    print("⚠️  Ajout manuel du case statement recommandé")

# Sauvegarder
with open('BUREAU_42_mr_robot.sh', 'w') as f:
    f.write(content)

print("✅ Fichier patché avec succès")
