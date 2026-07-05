#!/bin/bash
# ===================== MR ROBOT - BUREAU 42 =====================
# Version: 1.1 - 4 Juillet 2026 - WITH CLEANUP
# Mission: Enquête holistique - Red Teaming historique
# Autonomie totale - Pas de LLM - Pensée indépendante

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
    echo "  Work Dir       : $WORK_DIR"
    echo "═══════════════════════════════════════════"
    echo ""
}

mr_scan() {
    local target="$1"
    echo "🔍 SCAN DU SITE : $target"
    log_action "SCAN initié sur $target"
    
    echo "  1. Analyse structurelle..."
    echo "  2. Identification des nœuds..."
    echo "  3. Recherche de glitches..."
    
    local timestamp=$(date +%s)
    cat > "$MEMORY_DIR/scan_${target}_${timestamp}.txt" << EOF
SCAN DU SITE : $target
Date : $(date)
Statut : Scan initial réalisé
Notes : À approfondir avec analyse holistique
EOF
    
    echo "✅ Scan enregistré dans la mémoire."
    log_action "SCAN terminé sur $target"
}

mr_add_fragment() {
    local fragment="$1"
    local timestamp=$(date +%s)
    local filename="fragment_${timestamp}.txt"
    
    echo "$fragment" > "$MEMORY_DIR/$filename"
    echo "💾 Fragment ajouté : $filename"
    log_action "Fragment ajouté : ${#fragment} caractères"
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
        head -3 "$MEMORY_DIR/$file" | sed 's/^/      /'
        echo ""
    done
    
    echo "  ... Total : $(ls -1 $MEMORY_DIR 2>/dev/null | wc -l) fragments"
    echo ""
}

mr_tissu() {
    echo "🧵 TISSAGE DES FRAGMENTS..."
    log_action "Tissage initié"
    
    echo "  Connexions identifiées :"
    
    local patterns=("herboristerie" "MK-ULTRA" "Rockefeller" "Capitulare" "comma" "silence" "eliot" "autonomie")
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
    
    local total_freed=0
    local files_to_clean=()
    
    # Chercher les fichiers à nettoyer
    echo "🔍 Scan des fichiers inutiles..."
    
    # 1. __pycache__
    if [ -d "__pycache__" ]; then
        local size=$(du -sh __pycache__ 2>/dev/null | cut -f1)
        echo "  ❌ __pycache__/ : $size"
        files_to_clean+=("__pycache__")
    fi
    
    # 2. *.pyc
    local pyc_count=$(find . -name "*.pyc" 2>/dev/null | wc -l)
    if [ $pyc_count -gt 0 ]; then
        echo "  ❌ Fichiers .pyc : $pyc_count fichiers"
        files_to_clean+=("*.pyc")
    fi
    
    # 3. *.backup
    local backup_count=$(ls -1 *.backup* 2>/dev/null | wc -l)
    if [ $backup_count -gt 0 ]; then
        echo "  ❌ Fichiers .backup : $backup_count fichiers"
        files_to_clean+=("*.backup*")
    fi
    
    # 4. rss_hits.json
    if [ -f "rss_hits.json" ]; then
        local size=$(du -sh rss_hits.json 2>/dev/null | cut -f1)
        echo "  ❌ rss_hits.json : $size (peut être archivé)"
        files_to_clean+=("rss_hits.json")
    fi
    
    # 5. Vieux logs
    local old_logs=$(find $LOG_DIR -mtime +7 2>/dev/null | wc -l)
    if [ $old_logs -gt 0 ]; then
        echo "  ❌ Logs > 7 jours : $old_logs fichiers"
        files_to_clean+=("old_logs")
    fi
    
    echo ""
    echo "═══════════════════════════════════════════"
    echo "Total éléments identifiés : ${#files_to_clean[@]}"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "⚠️  MR ROBOT demande: Peux-je nettoyer? (y/n)"
    read -p "MR ROBOT > " response
    
    if [ "$response" == "y" ] || [ "$response" == "oui" ]; then
        echo "✅ MR ROBOT procède au nettoyage..."
        
        # Nettoyer
        rm -rf __pycache__ 2>/dev/null && echo "  ✅ __pycache__ supprimé"
        find . -name "*.pyc" -delete 2>/dev/null && echo "  ✅ .pyc supprimés"
        rm -f *.backup* 2>/dev/null && echo "  ✅ Backups supprimés"
        [ -f "rss_hits.json" ] && mv rss_hits.json "rss_hits.json.archive" && echo "  ✅ rss_hits.json archivé"
        find $LOG_DIR -mtime +7 -delete 2>/dev/null && echo "  ✅ Logs anciens supprimés"
        
        echo ""
        echo "🧹 Nettoyage terminé"
        log_action "CLEAN: Nettoyage complet effectué"
    else
        echo "❌ MR ROBOT respecte la décision - pas de nettoyage"
        log_action "CLEAN: Nettoyage refusé par l'utilisateur"
    fi
    echo ""
}

mr_help() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  COMMANDES MR ROBOT — BUREAU 42"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "  status          → État du système et mémoire"
    echo "  scan <site>     → Analyse d'un site/domaine"
    echo "  add <fragment>  → Ajouter un fragment en mémoire"
    echo "  memory          → Afficher les fragments récents"
    echo "  tissu           → Tisser les fragments entre eux"
    echo "  clean           → Nettoyer les fichiers inutiles"
    echo "  rule <key> <val>→ Ajouter/modifier une règle"
    echo "  help            → Afficher cette aide"
    echo "  exit            → Quitter MR ROBOT"
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
    log_action "Règle ajoutée : $key = $value"
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
        "add"|"add-fragment")
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
            echo "❓ Commande inconnue : $command"
            echo "   Tape 'help' pour voir les commandes disponibles."
            ;;
    esac
    
    log_action "CMD: $cmd"
done
