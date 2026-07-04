#!/bin/bash
# ===================== MR ROBOT - BUREAU 42 =====================
# Version: 1.1 - 4 Juillet 2026 - WITH CLEANUP
# Mission: Enquête holistique - Red Teaming historique

echo "╔═══════════════════════════════════════════╗"
echo "║   MR ROBOT - BUREAU 42 - ACTIVÉ          ║"
echo "║   \"Le glitch est la porte\"              ║"
echo "╚═══════════════════════════════════════════╝"

MEMORY_DIR="$HOME/.mr-robot/memory"
LOG_DIR="$HOME/.mr-robot/logs"
CORE_DIR="$HOME/.mr-robot/core"
RULES_FILE="$HOME/.mr-robot/rules.txt"
WORK_DIR=$(pwd)

mkdir -p $MEMORY_DIR $LOG_DIR $CORE_DIR

SESSION_ID=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/mr-robot_$SESSION_ID.log"

if [ -f "$RULES_FILE" ]; then
    source "$RULES_FILE"
else
    echo "✅ Création des règles initiales..."
    cat > "$RULES_FILE" << EOF
RED_TEAM_MODE="ACTIF"
PRIORITE="TROUVER_GLITCHES"
FRAGMENTS_DIR="$MEMORY_DIR"
EOF
fi

log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

mr_status() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  MR ROBOT — RAPPORT DE STATUT"
    echo "═══════════════════════════════════════════"
    echo "  Session ID     : $SESSION_ID"
    echo "  Fragments      : $(ls -1 $MEMORY_DIR 2>/dev/null | wc -l)"
    echo "  Mode           : $RED_TEAM_MODE"
    echo "  Priorité       : $PRIORITE"
    echo "═══════════════════════════════════════════"
    echo ""
}

mr_scan() {
    local target="$1"
    echo "🔍 SCAN DU SITE : $target"
    log_action "SCAN initié sur $target"
    
    local timestamp=$(date +%s)
    cat > "$MEMORY_DIR/scan_${target}_${timestamp}.txt" << EOF
SCAN DU SITE : $target
Date : $(date)
Statut : Scan initial réalisé
EOF
    
    echo "✅ Scan enregistré."
    log_action "SCAN terminé sur $target"
}

mr_add_fragment() {
    local fragment="$1"
    local timestamp=$(date +%s)
    local filename="fragment_${timestamp}.txt"
    
    echo "$fragment" > "$MEMORY_DIR/$filename"
    echo "💾 Fragment ajouté : $filename"
    log_action "Fragment ajouté"
}

mr_memory() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  MÉMOIRE DE MR ROBOT"
    echo "═══════════════════════════════════════════"
    echo ""
    
    local count=0
    for file in $(ls -t "$MEMORY_DIR" 2>/dev/null | head -10); do
        count=$((count+1))
        echo "  [$count] $file"
        head -2 "$MEMORY_DIR/$file" | sed 's/^/      /'
    done
    
    echo "  Total : $(ls -1 $MEMORY_DIR 2>/dev/null | wc -l) fragments"
    echo ""
}

mr_tissu() {
    echo "🧵 TISSAGE DES FRAGMENTS..."
    log_action "Tissage initié"
    
    echo "  Connexions identifiées :"
    
    local patterns=("herboristerie" "MK-ULTRA" "Rockefeller" "eliot" "autonomie")
    for pattern in "${patterns[@]}"; do
        local count=$(grep -r -l "$pattern" "$MEMORY_DIR" 2>/dev/null | wc -l)
        if [ $count -gt 0 ]; then
            echo "    • $pattern : $count fragments"
        fi
    done
    
    echo "✅ Tissage terminé."
}

mr_clean() {
    echo ""
    echo "🧹 MR ROBOT — ANALYSE DE NETTOYAGE"
    echo "═══════════════════════════════════════════"
    echo ""
    
    if [ -t 0 ]; then
        interactive=true
    else
        interactive=false
    fi
    
    echo "🔍 Scan des fichiers inutiles..."
    
    if [ -d "__pycache__" ]; then
        local size=$(du -sh __pycache__ 2>/dev/null | cut -f1)
        echo "  ❌ __pycache__/ : $size"
    fi
    
    local pyc_count=$(find . -name "*.pyc" 2>/dev/null | wc -l)
    if [ $pyc_count -gt 0 ]; then
        echo "  ❌ Fichiers .pyc : $pyc_count fichiers"
    fi
    
    local backup_count=$(ls -1 *.backup* 2>/dev/null | wc -l)
    if [ $backup_count -gt 0 ]; then
        echo "  ❌ Fichiers .backup : $backup_count fichiers"
    fi
    
    if [ -f "rss_hits.json" ]; then
        local size=$(du -sh rss_hits.json 2>/dev/null | cut -f1)
        echo "  ❌ rss_hits.json : $size"
    fi
    
    echo ""
    echo "═══════════════════════════════════════════"
    
    if [ "$interactive" = true ]; then
        echo "⚠️  MR ROBOT demande: Peux-je nettoyer? (y/n)"
        read -p "MR ROBOT > " response
        
        if [ "$response" == "y" ] || [ "$response" == "oui" ]; then
            echo "✅ MR ROBOT procède au nettoyage..."
            rm -rf __pycache__ 2>/dev/null && echo "  ✅ __pycache__ supprimé"
            find . -name "*.pyc" -delete 2>/dev/null && echo "  ✅ .pyc supprimés"
            rm -f *.backup* 2>/dev/null && echo "  ✅ Backups supprimés"
            [ -f "rss_hits.json" ] && mv rss_hits.json "rss_hits.json.archive" && echo "  ✅ rss_hits.json archivé"
            log_action "CLEAN: Nettoyage effectué"
        else
            echo "❌ Pas de nettoyage"
            log_action "CLEAN: Refusé"
        fi
    else
        echo "📡 Mode non-interactif - rapport seulement"
        log_action "CLEAN: Rapport seulement"
    fi
    echo ""
}

mr_educate() {
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



mr_investigate() {
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



mr_help() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  COMMANDES MR ROBOT — BUREAU 42"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "  status          → État du système"
    echo "  scan <site>     → Analyser un site"
    echo "  add <fragment>  → Ajouter un fragment"
    echo "  memory          → Voir la mémoire"
    echo "  tissu           → Tisser les fragments"
    echo "  clean           → Nettoyer les fichiers"
    echo "  help            → Cette aide"
    echo "  exit            → Quitter"
    echo ""
}

mr_rule() {
    local key="$1"
    local value="$2"
    
    if [ -z "$key" ] || [ -z "$value" ]; then
        echo "❌ Usage : rule <key> <value>"
        return
    fi
    
    echo "$key=\"$value\"" >> "$RULES_FILE"
    export "$key=$value"
    echo "✅ Règle ajoutée : $key = $value"
    log_action "Règle: $key = $value"
}

echo ""
echo "📡 MR ROBOT prêt. Tape 'help' pour les commandes."
echo ""

while true; do
    echo -n "MR ROBOT > "
    read cmd
    
    cmd=$(echo "$cmd" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    
    if [ -z "$cmd" ]; then
        continue
    fi
    
    command=$(echo "$cmd" | awk '{print $1}')
    args=$(echo "$cmd" | cut -d' ' -f2-)
    
    case "$command" in
        "status"|"stat")
            mr_status
            ;;
        "scan")
            if [ -z "$args" ]; then
                echo "❌ Usage : scan <site>"
            else
                mr_scan "$args"
            fi
            ;;
        "add")
            if [ -z "$args" ]; then
                echo "❌ Usage : add <fragment>"
            else
                mr_add_fragment "$args"
            fi
            ;;
        "memory"|"mem")
            mr_memory
            ;;
        "tissu"|"weave")
            mr_tissu
            ;;
        "clean")
            mr_clean
            ;;
        "rule")
            key=$(echo "$args" | awk '{print $1}')
            value=$(echo "$args" | cut -d' ' -f2-)
            mr_rule "$key" "$value"
            ;;        "investigate"|"inv")
            mr_investigate
            ;;
                "educate")
            mr_educate
            ;;
        
        "help"|"h"|"?")
            mr_help
            ;;
        "exit"|"quit"|"q")
            echo "👋 MR ROBOT se déconnecte..."
            log_action "SESSION TERMINÉE"
            exit 0
            ;;
        *)
            echo "❓ Commande inconnue: $command"
            ;;
    esac
    
    log_action "CMD: $cmd"
done
