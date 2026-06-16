#!/usr/bin/env bash
set -e

echo "===================================="
echo "  Interactive Generative Studio"
echo "  Setup"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[ERROR] Python n'est pas installé."
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)
echo "[OK] Python trouvé: $($PYTHON --version)"

# Create virtual environment
if [ ! -f "venv/bin/activate" ]; then
    echo ""
    echo "[1/4] Création de l'environnement virtuel..."
    $PYTHON -m venv venv
    echo "[OK] Environnement virtuel créé"
else
    echo "[OK] Environnement virtuel existe déjà"
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo ""
echo "[2/4] Installation des dépendances..."
pip install -r backend/requirements.txt
echo "[OK] Dépendances installées"

# Create media folders
echo ""
echo "[3/4] Création des dossiers media..."
mkdir -p media/audio media/generated media/uploads
echo "[OK] Dossiers media créés"

# Create static plots folder
echo ""
echo "[4/4] Création du dossier plots..."
mkdir -p frontend/static/plots
echo "[OK] Dossier plots créé"

echo ""
echo "===================================="
echo "  Setup terminé avec succès !"
echo "===================================="
echo ""
echo "Pour lancer l'application :"
echo "    ./run.sh"
echo ""
echo "Ou manuellement :"
echo "    source venv/bin/activate && python backend/app.py"
echo ""
echo "Optionnel - Installer FFmpeg pour l'audio :"
echo "    ./install_ffmpeg.sh"
echo ""
