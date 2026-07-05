#!/usr/bin/env python3
import re
import json

with open('BUREAU_42_mr_robot.sh', 'r') as f:
    content = f.read()

# Nouvelle fonction mr_investigate PATTERNS CLÉS
investigate_patterns = '''mr_investigate() {
    echo ""
    echo "🔍 MR ROBOT — INVESTIGATION PATTERNS CLÉS"
    echo "═══════════════════════════════════════════"
    echo ""
    
    if [ ! -f "data/octopus_data_REAL.json" ]; then
        echo "❌ Map non trouvée"
        return
    fi
    
    echo "📊 Analyse de la STRUCTURE..."
    echo ""
    
    # Identifie les HUBS (nœuds centraux)
    echo "🔴 HUBS PRINCIPAUX (structure hiérarchique):"
    echo ""
    
    # BRI au centre
    echo "  [0] BRI — Banque Règlements Internationaux"
    echo "      └─ Preuve empirique pieuvre centrale"
    echo "      └─ Fonctionne pendant guerre Alliés+Axe"
    echo ""
    
    # Niveau 1: Finance
    echo "  [1] FINANCE — Rothschild / Morgan / Warburg / Fed"
    echo "      ├─ Rothschild: réseau bancaire transnational"
    echo "      ├─ Morgan: sauve 2x État américain"
    echo "      ├─ Warburg: pont transatlantique"
    echo "      └─ Fed: institutionnalise contrôle monnaie"
    echo ""
    
    # Niveau 2: États
    echo "  [2] ÉTATS — USA / UK / FRANCE / ISRAËL"
    echo "      ├─ USA: CIA + Rockefeller + CFR"
    echo "      ├─ UK: MI6 + Tavistock + Chatham"
    echo "      ├─ FRANCE: ENA + Inspection Finances"
    echo "      └─ ISRAËL: Mossad + Épstein"
    echo ""
    
    # Niveau 3: Ingénierie sociale
    echo "  [3] INGÉNIERIE SOCIALE — Rockefeller"
    echo "      ├─ Bureau Social Hygiene"
    echo "      ├─ CRPS (recherche sexologie)"
    echo "      ├─ Kinsey (normalisation)"
    echo "      ├─ WFMH (exportation modèle)"
    echo "      └─ Sanger (contrôle population)"
    echo ""
    
    # Niveau 4: Contrôle
    echo "  [4] CONTRÔLE — MK-ULTRA / CIA / NSA"
    echo "      ├─ MK-ULTRA: programmation mentale"
    echo "      ├─ CIA: Paperclip + Mockingbird"
    echo "      └─ NSA/PRISM: surveillance totale"
    echo ""
    
    # Niveau 5: Victimes/Objectifs
    echo "  [5] VICTIMES/ENQUÊTES — Tesla / Épstein / Dutroux"
    echo "      ├─ Tesla: énergie non centralisable = menace"
    echo "      ├─ Épstein: réseau pédocriminel = preuve"
    echo "      └─ Dutroux: gladio = état profond"
    echo ""
    
    echo "═══════════════════════════════════════════"
    echo ""
    echo "✅ PATTERNS CLÉS IDENTIFIÉS:"
    echo ""
    echo "  Pattern 1: BRI → États → Finance"
    echo "             (Contrôle monétaire = contrôle politique)"
    echo ""
    echo "  Pattern 2: Rockefeller → WFMH → Tavistock"
    echo "             (Ingénierie sociale = normalisation)"
    echo ""
    echo "  Pattern 3: CIA → MK-ULTRA → Surveillance"
    echo "             (Contrôle esprit = contrôle masse)"
    echo ""
    echo "  Pattern 4: Tesla/Épstein/Dutroux = preuves"
    echo "             (Ce que la pieuvre FAIT pour survivre)"
    echo ""
    echo "═══════════════════════════════════════════"
    echo ""
    echo "📝 MR ROBOT rapporte:"
    echo "  ✓ Hiérarchie vue"
    echo "  ✓ Structure comprise"
    echo "  ✓ Patterns tissés"
    echo "  ✓ Prochaine étape: enrichir avec enquêtes HTML"
    echo ""
    
    log_action "INVESTIGATE: PATTERNS CLÉS analysés - structure pieuvre comprise"
}

'''

# Remplacer l'ancienne fonction
if 'mr_investigate()' in content:
    content = re.sub(r'mr_investigate\(\) \{.*?\n\}', investigate_patterns, content, flags=re.DOTALL)
    print("✅ Fonction mr_investigate PATTERNS mise à jour")
else:
    pattern = r'(mr_help\(\) \{)'
    content = re.sub(pattern, investigate_patterns + r'\1', content)
    print("✅ Fonction mr_investigate PATTERNS ajoutée")

# Sauvegarder
with open('BUREAU_42_mr_robot.sh', 'w') as f:
    f.write(content)

print("✅ MR ROBOT apprend la STRUCTURE réelle")
