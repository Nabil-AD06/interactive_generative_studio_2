#!/usr/bin/env bash
set -e

echo "===================================="
echo "  Installation de FFmpeg"
echo "===================================="
echo ""

# Check if ffmpeg is already installed
if command -v ffmpeg &> /dev/null; then
    echo "[OK] FFmpeg est deja installe: $(ffmpeg -version 2>&1 | head -1)"
    exit 0
fi

echo "[1/2] Recherche du gestionnaire de paquets..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        echo "[OK] Detected: apt-get (Debian/Ubuntu)"
        echo ""
        echo "[2/2] Installation de FFmpeg..."
        sudo apt-get update -qq
        sudo apt-get install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        echo "[OK] Detected: dnf (Fedora)"
        echo ""
        echo "[2/2] Installation de FFmpeg..."
        sudo dnf install -y ffmpeg
    elif command -v pacman &> /dev/null; then
        echo "[OK] Detected: pacman (Arch)"
        echo ""
        echo "[2/2] Installation de FFmpeg..."
        sudo pacman -S --noconfirm ffmpeg
    else
        echo "[ERREUR] Gestionnaire de paquets non reconnu."
        echo "        Installez FFmpeg manuellement :"
        echo "        https://ffmpeg.org/download.html"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        echo "[OK] Detected: Homebrew (macOS)"
        echo ""
        echo "[2/2] Installation de FFmpeg..."
        brew install ffmpeg
    else
        echo "[ERREUR] Homebrew n'est pas installe."
        echo "        Installez Homebrew : https://brew.sh"
        echo "        Puis : brew install ffmpeg"
        exit 1
    fi
else
    echo "[ERREUR] OS non supporte par ce script."
    echo "        Installez FFmpeg manuellement :"
    echo "        https://ffmpeg.org/download.html"
    exit 1
fi

# Verify
echo ""
echo "[OK] Verification..."
if command -v ffmpeg &> /dev/null; then
    echo "[OK] FFmpeg installe avec succes: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "[ERREUR] FFmpeg n'a pas pu etre installe."
    exit 1
fi

echo ""
echo "===================================="
echo "  Installation terminee !"
echo "===================================="
echo "Redemarrez l'application."
