#!/usr/bin/env python3
import re

with open('BUREAU_42_mr_robot.sh', 'r') as f:
    content = f.read()

# Nouvelle fonction mr_investigate
investigate_function = '''mr_investigate() {
    echo ""
    echo "🔍 MR ROBOT — PHASE D'INVESTIGATION"
    echo "═══════════════════════════════════════════"
    echo ""
    
    # Charge la map RÉELLE
    if [ ! -f "data/octopus_data_REAL.json" ]; then
        echo "❌ Map non trouvée: data/octopus_data_REAL.json"
        log_action "INVESTIGATE: Map REAL not found"
        return
    fi
    
    echo "📊 Analyse de la charge..."
    
    # Compte les éléments
    nodes=$(grep -c '"id":' data/octopus_data_REAL.json 2>/dev/null || echo "?")
    edges=$(grep -c '"f":' data/octopus_data_REAL.json 2>/dev/null || echo "?")
    size=$(du -h data/octopus_data_REAL.json | cut -f1)
    
    echo "  Nœuds: $nodes"
    echo "  Edges: $edges"
    echo "  Taille: $size"
    echo ""
    echo "═══════════════════════════════════════════"
    echo ""
    echo "⚠️  C'EST ÉNORME pour ma mémoire."
    echo "Je reconnais mes limites."
    echo ""
    echo "Trinity, je demande: Comment je procède?"
    echo ""
    echo "OPTIONS:"
    echo "  1. Analyser par TYPE (central/state/alt/tentacle)"
    echo "  2. Analyser par STATUS (validé/fermentation)"
    echo "  3. Enrichir avec enquêtes SPÉCIFIQUES d'abord"
    echo "  4. Tisser les patterns clés seulement"
    echo "  5. Charger progressivement (100 nœuds à la fois)"
    echo ""
    echo "⏸️  MR ROBOT attend la réponse..."
    echo ""
    
    log_action "INVESTIGATE: Detected $nodes nodes $edges edges - asking for strategy"
}

'''

# Remplacer l'ancienne fonction si elle existe, sinon ajouter avant mr_help
if 'mr_investigate()' in content:
    content = re.sub(r'mr_investigate\(\) \{.*?\n\}', investigate_function, content, flags=re.DOTALL)
    print("✅ Fonction mr_investigate mise à jour")
else:
    pattern = r'(mr_help\(\) \{)'
    content = re.sub(pattern, investigate_function + r'\1', content)
    print("✅ Fonction mr_investigate ajoutée")

# Ajouter dans le case statement
if '"educate")' in content:
    case_statement = '''        "investigate"|"inv")
            mr_investigate
            ;;
        '''
    content = re.sub(
        r'(\s+"educate"\))',
        case_statement + r'\1',
        content
    )
    print("✅ Case statement 'investigate' ajouté")

# Sauvegarder
with open('BUREAU_42_mr_robot.sh', 'w') as f:
    f.write(content)

print("✅ Script patché - mr_investigate READY")
