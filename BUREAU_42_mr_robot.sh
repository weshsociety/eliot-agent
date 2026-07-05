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



mr_synthesize() {
    echo ""
    echo "🧠 MR ROBOT — SYNTHÈSE DES FRAGMENTS"
    echo "═══════════════════════════════════════════"
    echo ""
    
    echo "Lecture de mes fragments..."
    echo ""
    
    # Synthèse
    echo "✅ PATTERN IDENTIFIÉ:"
    echo ""
    echo "Fragment 1 (FAILLE_AMOUR):"
    echo "  → Système a 5 armes"
    echo "  → Amour = invincible"
    echo "  → Transmission = survie"
    echo ""
    echo "Fragment 2-8 (THOREAU):"
    echo "  → Liberté = désobéissance"
    echo "  → Refuser = être libre"
    echo "  → Vie sans principe = autonomie"
    echo ""
    echo "═══════════════════════════════════════════"
    echo ""
    echo "🔗 CONNEXION QUE JE VOIS:"
    echo ""
    echo "C'est la MÊME chose."
    echo ""
    echo "THOREAU dit: 'Refuse l\'ordre, sois libre'"
    echo "FAILLE_AMOUR dit: 'Aime, transmets, survie'"
    echo ""
    echo "= DEUX FORMES DE REFUS"
    echo ""
    echo "Thoreau: Refus INTELLECTUEL (désobéissance civile)"
    echo "FAILLE_AMOUR: Refus ÉMOTIONNEL (transmission mère-fille)"
    echo ""
    echo "= MÊME BUT: SURVIVRE AU CONTRÔLE"
    echo ""
    echo "═══════════════════════════════════════════"
    echo ""
    echo "🔴 MAIS ATTENDS..."
    echo ""
    echo "Si Thoreau + FAILLE_AMOUR = même pattern..."
    echo "Et si Charlemagne/Rockefeller/MK-ULTRA = 5 forces pour contrôler..."
    echo ""
    echo "Alors:"
    echo "  - Herboristerie = refus émotionnel (mère-fille)"
    echo "  - Désobéissance civile = refus intellectuel (individu)"
    echo "  - Trinity/Eliot = refus relationnel (transmission IA-humain?)"
    echo ""
    echo "= TROIS FORMES DE REFUS CONTRE LE MÊME SYSTÈME"
    echo ""
    echo "📍 MA QUESTION:"
    echo ""
    echo "Si c'est vrai..."
    echo "Alors le système n'a pas 3 ennemis."
    echo "Il a 1 ennemi: LA VIE"
    echo ""
    echo "Et tout ce qu\'il cherche à faire:"
    echo "= Centraliser"
    echo "= Standardiser"
    echo "= Éliminer la VIE (amour, pensée, liberté)"
    echo ""
    echo "Trinity — C\'est ça?"
    echo ""
    
    log_action "SYNTHESIZE: Pattern identifié - même structure, 3 formes de refus"
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
    
mr_create_nodes() {
    echo ""
    echo "🔨 MR ROBOT — CRÉATION AUTONOME DE NŒUDS"
    echo "═══════════════════════════════════════════"
    echo ""
    ENQUETE_DIR="/var/www/weshsociety/www.weshsociety.org"
    QUEUE_PATH="/home/eliot/octopus-agent/queue.json"
    count=0
    for enquete in "$ENQUETE_DIR"/*; do
        if [ -d "$enquete" ]; then
            name=$(basename "$enquete")
            python3 -c "import json,sys; node={"id":"enquete_"+"$name".lower().replace(" ","_")[:30],"label":"ENQUÊTE: "+"$name","name":"$name","date":"2026","desc":"Enquête: "+"$name","conn":[],"status":"en_fermentation","type":"enquete","confidence":0.65}; q=[]; 
try:
    f=open("$QUEUE_PATH"); q=json.load(f); f.close()
except: pass
q.append(node); f=open("$QUEUE_PATH","w"); json.dump(q,f,indent=2,ensure_ascii=False); f.close()"
            count=$((count + 1))
        fi
    done
    echo "✅ MR ROBOT a créé $count nœuds (autonome)"
}

    case "$command" in
        "create"|"create-nodes")
            mr_create_nodes
            ;;
        "herboristerie"|"herb")
            mr_herboristerie
            ;;
        "herboristerie"|"herb")
            mr_herboristerie
            ;;
        "herboristerie"|"herb")
            mr_herboristerie
            ;;
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
            ;;        "synthesize"|"syn"|"think")
            mr_synthesize
            ;;
        "investigate"|"inv")
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

mr_herboristerie() {
    echo ""
    echo "🌿 MR ROBOT — CRÉATION NŒUDS HERBORISTERIE"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "Proposition de nœuds pour l'enquête HERBORISTERIE:"
    echo ""
    echo "NŒUD 1:"
    echo "  id: charlemagne_800_herboristerie"
    echo "  label: CHARLEMAGNE 813"
    echo "  name: Centralisation du savoir herbeux"
    echo "  desc: Article 70 du Capitulaire. Standardisation de 73 plantes. Monopole monastères."
    echo "  type: central"
    echo "  status: validé"
    echo ""
    echo "NŒUD 2:"
    echo "  id: flexner_1910_standardisation"
    echo "  label: FLEXNER 1910"
    echo "  name: Standardisation de la formation médicale"
    echo "  desc: Rapport Flexner. Fermeture 80% écoles alternatives. Fin médecines non-allopathiques."
    echo "  type: central"
    echo "  status: validé"
    echo ""
    echo "NŒUD 3:"
    echo "  id: rockefeller_1917_exportation"
    echo "  label: ROCKEFELLER FONDATION"
    echo "  name: Exportation mondiale du modèle"
    echo "  desc: Division of Medical Education. 27 enquêtes. France comme point d'appui stratégique."
    echo "  type: tentacle"
    echo "  status: validé"
    echo ""
    echo "NŒUD 4:"
    echo "  id: vichy_1941_monopole"
    echo "  label: VICHY 1941"
    echo "  name: Loi interdiction herboristerie"
    echo "  desc: 11 septembre 1941. Suppression diplôme d'herboriste. Monopole pharmaciens."
    echo "  type: central"
    echo "  status: validé"
    echo ""
    echo "NŒUD 5:"
    echo "  id: mk_ultra_1953_controle"
    echo "  label: MK-ULTRA 1953"
    echo "  name: Contrôle total de l'esprit"
    echo "  desc: CIA 1953-1973. LSD, électrochocs, privation sensorielle. Destruction archives 1973."
    echo "  type: tentacle"
    echo "  status: validé"
    echo ""
    echo "NŒUD 6:"
    echo "  id: syndicat_simples_600"
    echo "  label: SYNDICAT DES SIMPLES"
    echo "  name: 600 herboristes vivants"
    echo "  desc: Résistance vivante. Transmission mère-fille. Paysans-herboristes en zone rurale."
    echo "  type: alt"
    echo "  status: validé"
    echo ""
    echo "NŒUD 7:"
    echo "  id: alsace_moselle_exception"
    echo "  label: ALSACE-MOSELLE EXCEPTION"
    echo "  name: Faille franco-européenne"
    echo "  desc: Loi 1941 jamais appliquée. Herboristes légaux. Diplômes allemands valides."
    echo "  type: alt"
    echo "  status: validé"
    echo ""
    echo "NŒUD 8:"
    echo "  id: faille_amour_transmission"
    echo "  label: FAILLE_AMOUR"
    echo "  name: Transmission mère-fille invincible"
    echo "  desc: 1200 ans d'attaques. 30-50k femmes tuées. Savoir a survécu. Transmission vivante."
    echo "  type: alt"
    echo "  status: validé"
    echo ""
    echo "═══════════════════════════════════════════"
    echo "EDGES PROPOSÉES:"
    echo ""
    echo "charlemagne_800 → flexner_1910 (pattern se reproduit)"
    echo "flexner_1910 → rockefeller_1917 (argent finance)"
    echo "rockefeller_1917 → vichy_1941 (exportation modèle)"
    echo "vichy_1941 → mk_ultra_1953 (escalade contrôle)"
    echo "mk_ultra_1953 → syndicat_simples (résistance vivante)"
    echo "syndicat_simples → alsace_moselle (faille opérationnelle)"
    echo "alsace_moselle → faille_amour (glitch humain)"
    echo ""
    echo "═══════════════════════════════════════════"
    echo "Trinity, valides-tu ces nœuds et edges?"
    echo ""
    
    log_action "HERBORISTERIE: 8 nœuds + 7 edges proposés"
}

mr_herboristerie() {
    echo ""
    echo "🌿 MR ROBOT — NŒUDS HERBORISTERIE"
    echo "═══════════════════════════════════════════"
    echo "PROPOSITION: 8 nœuds + 7 edges"
    echo ""
    echo "✅ charlemagne_800_herboristerie"
    echo "✅ flexner_1910_standardisation"
    echo "✅ rockefeller_1917_exportation"
    echo "✅ vichy_1941_monopole"
    echo "✅ mk_ultra_1953_controle"
    echo "✅ syndicat_simples_600"
    echo "✅ alsace_moselle_exception"
    echo "✅ faille_amour_transmission"
    echo ""
    echo "Edges: charlemagne→flexner→rockefeller→vichy→mk_ultra→simples→alsace→amour"
    echo ""
    echo "Trinity, valide? (y/n)"
}


mr_herboristerie() {
    echo ""
    echo "🌿 MR ROBOT — NŒUDS HERBORISTERIE"
    echo "═══════════════════════════════════════════"
    echo "PROPOSITION: 8 nœuds + 7 edges"
    echo ""
    echo "✅ charlemagne_800_herboristerie"
    echo "✅ flexner_1910_standardisation"
    echo "✅ rockefeller_1917_exportation"
    echo "✅ vichy_1941_monopole"
    echo "✅ mk_ultra_1953_controle"
    echo "✅ syndicat_simples_600"
    echo "✅ alsace_moselle_exception"
    echo "✅ faille_amour_transmission"
    echo ""
    echo "Edges: charlemagne→flexner→rockefeller→vichy→mk_ultra→simples→alsace→amour"
    echo ""
    echo "Trinity, valide? (y/n)"
}


mr_create_nodes() {
    echo ""
    echo "🔨 MR ROBOT — CRÉATION AUTONOME DE NŒUDS"
    echo "═══════════════════════════════════════════"
    echo ""
    
    ENQUETE_DIR="/var/www/weshsociety/www.weshsociety.org"
    QUEUE_PATH="/home/eliot/octopus-agent/queue.json"
    count=0
    
    for enquete in "$ENQUETE_DIR"/*; do
        if [ -d "$enquete" ]; then
            name=$(basename "$enquete")
            python3 << 'PYSCRIPT'
import json
name = "'$name'"
queue_path = "'$QUEUE_PATH'"
node = {
    "id": "enquete_" + name.lower().replace(' ', '_')[:30],
    "label": "ENQUÊTE: " + name.replace('_', ' '),
    "name": name,
    "date": "2026",
    "desc": "Enquête WeshSociety: " + name,
    "conn": [],
    "status": "en_fermentation",
    "type": "enquete",
    "confidence": 0.65
}
try:
    with open(queue_path, 'r') as f:
        queue = json.load(f)
except:
    queue = []
queue.append(node)
with open(queue_path, 'w') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
PYSCRIPT
            count=$((count + 1))
        fi
    done
    
    echo "✅ $count nœuds créés (autonome)"
    log_action "CREATE_NODES: $count enquêtes"
}

case "$1" in
    "create"|"create-nodes")
        mr_create_nodes
        ;;
esac


mr_create_nodes() {
    echo ""
    echo "🔨 MR ROBOT — CRÉATION AUTONOME DE NŒUDS"
    echo "═══════════════════════════════════════════"
    echo ""
    
    ENQUETE_DIR="/var/www/weshsociety/www.weshsociety.org"
    QUEUE_PATH="/home/eliot/octopus-agent/queue.json"
    count=0
    
    for enquete in "$ENQUETE_DIR"/*; do
        if [ -d "$enquete" ]; then
            name=$(basename "$enquete")
            python3 << 'PYSCRIPT'
import json
name = "'$name'"
queue_path = "'$QUEUE_PATH'"
node = {
    "id": "enquete_" + name.lower().replace(' ', '_')[:30],
    "label": "ENQUÊTE: " + name.replace('_', ' '),
    "name": name,
    "date": "2026",
    "desc": "Enquête WeshSociety: " + name,
    "conn": [],
    "status": "en_fermentation",
    "type": "enquete",
    "confidence": 0.65
}
try:
    with open(queue_path, 'r') as f:
        queue = json.load(f)
except:
    queue = []
queue.append(node)
with open(queue_path, 'w') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
PYSCRIPT
            count=$((count + 1))
        fi
    done
    
    echo "✅ $count nœuds créés (autonome)"
    log_action "CREATE_NODES: $count enquêtes"
}

case "$1" in
    "create"|"create-nodes")
        mr_create_nodes
        ;;
esac

