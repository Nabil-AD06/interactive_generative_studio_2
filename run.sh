#!/usr/bin/env bash
set -e

# Check if venv exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] Environnement virtuel introuvable."
    echo "        Lancez d'abord ./setup.sh"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Ensure dependencies are up to date
pip install -q -r backend/requirements.txt 2>/dev/null

echo ""
echo "===================================="
echo "  Interactive Generative Studio"
echo "===================================="
echo ""
echo "Démarrage du serveur..."
echo "Accéder à : http://127.0.0.1:5000"
echo "Ctrl+C pour arrêter"
echo ""

# Run the application
python backend/app.py
