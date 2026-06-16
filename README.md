# Interactive Generative Studio

A comprehensive web-based creative platform built with Python and Flask that combines generative art, data visualization, image processing, audio manipulation, and machine learning-powered style transfer.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)

---

## 🚀 Quick Start

### Windows

**Avec scripts :**
```bat
setup.bat
install_ffmpeg.bat
run.bat
```

**Manuellement :**
```bat
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
install_ffmpeg.bat
python backend\app.py
```

### Mac

**Avec scripts :**
```bash
chmod +x setup.sh install_ffmpeg.sh run.sh
./setup.sh
./install_ffmpeg.sh
./run.sh
```

**Manuellement :**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
chmod +x install_ffmpeg.sh && ./install_ffmpeg.sh
python3 backend/app.py
```

→ **Ouvrir http://127.0.0.1:5000**

---

## 📋 Prérequis

- **Python 3.8+** (3.14 sous Windows), pip, venv
- **~300 Mo** d'espace disque
- **Connexion internet** (première installation des dépendances et téléchargement de FFmpeg)

---

## Table des matieres

- [Fonctionnalites](#-fonctionnalites)
- [Technologies](#-technologies)
- [TensorFlow / Style Transfer ML](#-tensorflow--style-transfer-ml)
- [Notes techniques](#-notes-techniques)
- [Installation manuelle detaillee](#-installation-manuelle-detaille)
- [Utilisation](#-utilisation)
- [Modules](#-module-details)
- [Depannage](#-depannage)
- [Structure du projet](#-structure-du-projet)

---

## Fonctionnalites

###  Generative Art Studio
- **Compositions geometriques** : classes Shape, Circle, Square, Triangle (POO)
- **Arbres fractals** : generation recursive avec profondeur reglable
- **Spirales** : motifs mathematiques avec controle de densite
- **Palettes** : 6 palettes de couleurs, apercu en direct

###  Data Visualization
- **Wave landscapes** : donnees de temperature en compositions fluides
- **Heatmaps abstraites** : matrice 20x20 avec colormap plasma
- **Bar compositions** : diagrammes artistiques avec gradients viridis
- **Interactif** : bubble chart et sunburst (Plotly)

###  Image Processing (25+ effets)
- **Filtres couleur** : noir & blanc, sepia, neon, vintage, chaud/froid
- **Artistique** : aquarelle, peinture a l'huile, cartoon, croquis
- **Distorsions** : glitch, pixelisation
- **Transformations** : rotation, mirroir, flip
- **Avance** : detection de contours, emboss, sharpen

###  Audio Processing
- **Vitesse** : accelere (1.5x) ou ralentit (0.75x)
- **Pitch** : decalage de +/- 4 demi-tons (Librosa)
- **Spatial** : echo (300ms) et reverb
- **Filtres** : passe-bas, passe-haut, bass boost
- **Generation** : synthetiseur de paysage sonore ambient
- **Visualisation** : spectrogramme en temps reel

###  Style Transfer (ML)
- **5 styles** : Van Gogh, Monet, Picasso, Munch, Kandinsky
- **Moteur** : TensorFlow Hub (reel) ou OpenCV (fallback)
- Voir la [section dediee](#-tensorflow--style-transfer-ml)

###  Gallery
- Parcourir toutes les creations generees, images traitees et style transfer
- Organise par type avec apercu vignette
- Telechargement direct

---

## Technologies

### Core
- **Python 3.8+** (3.14 sous Windows)
- **Flask 2.0+** + Jinja2
- **Three.js** (3D homepage)

### Image
- **Pillow** : manipulation de base
- **OpenCV** : effets avances
- **NumPy** : operations matricielles

### Data
- **Pandas** : traitement de donnees
- **Matplotlib** / **Seaborn** : graphiques
- **Plotly** : visualisations interactives

### Audio
- **PyDub** : manipulation audio
- **Librosa** : pitch shifting et analyse
- **SoundFile** : I/O audio
- **FFmpeg** : codecs audio

### ML (optionnel)
- **TensorFlow 2.x** + **TensorFlow Hub** (modele Magenta)

---

## 🧠 TensorFlow / Style Transfer ML

### Comment ça marche

| Mode | Moteur | Qualité | Performance |
|------|--------|---------|-------------|
| **Reel** | TF Hub (Magenta) | Transfert neuronal, fidele au style | Lent, GPU recommande |
| **Fallback** (defaut) | OpenCV (`stylization`, `edgePreservingFilter`, `CLAHE`, `Canny`…) | Filtres artistiques | Rapide, CPU |

### Compatibilite Python

- **Python 3.14** (votre version) : TensorFlow 2.x n'a pas de wheels pour cette version → fallback OpenCV **automatique**
- **Python ≤ 3.12** : TF 2.x + TF Hub s'installent normalement → mode reel

### Installer TensorFlow (Python ≤ 3.12 uniquement)

```bash
pip install tensorflow tensorflow-hub
```

Le modele Magenta se charge automatiquement au demarrage.

### Verification du moteur actif

Au demarrage, le terminal affiche :
```
[TF] TensorFlow loaded - Real Neural Style Transfer enabled         # Mode reel
[TF] TensorFlow not available - Using OpenCV artistic filters as fallback  # Fallback
```

### Styles disponibles (5)

Van Gogh, Monet, Picasso, Munch, Kandinsky — fonctionnent avec les deux moteurs.

---

## 🔌 Notes techniques

- **FFmpeg** installe dans `backend/` — pas besoin d'installation systeme. PyDub le trouve automatiquement.
- **Scripts `.bat`** fonctionnent depuis **cmd.exe** et **PowerShell**.
- **TensorFlow** non compatible Python 3.14 → fallback OpenCV automatique.
- **Limite fichiers** : 50 MB (`MAX_CONTENT_LENGTH` dans `app.py`).
- **Media** : les fichiers utilisateurs sont dans `media/` (gitignore).

---

## ⚙️ Installation manuelle detaillee

### 1. Cloner ou copier le projet

```bash
cd interactive_generative_studio_2
```

### 2. Creer l'environnement virtuel

```bash
python -m venv venv
```

### 3. Activer le venv

**Windows :**
```bash
venv\Scripts\activate
```

**Mac :**
```bash
source venv/bin/activate
```

### 4. Installer les dependances

```bash
pip install -r backend\requirements.txt
```

### 5. Creer les dossiers necessaires

```bash
mkdir media\audio media\generated media\uploads
mkdir frontend\static\plots
```

### 6. Installer FFmpeg (obligatoire pour l'audio)

**Windows :**
```bat
install_ffmpeg.bat
```
Ou manuellement : telecharger [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) et extraire `ffmpeg.exe` + `ffprobe.exe` dans `backend/`.

**Mac :**
```bash
chmod +x install_ffmpeg.sh
./install_ffmpeg.sh
```
Ou manuellement : `brew install ffmpeg`

### 7. Lancer l'application

```bash
python backend\app.py
```

Ouvrir **http://127.0.0.1:5000**

---

## Utilisation

| Page | Route | Description |
|------|-------|-------------|
| Accueil | `/` | Presentation 3D, apercu des modules |
| Art generatif | `/generative` | Creer des oeuvres algorithmiques |
| Data viz | `/data-viz` | Visualisations de donnees |
| Traitement d'images | `/image-processor` | 25+ effets d'image |
| Traitement audio | `/audio-processor` | Effets audio et generation |
| Style transfer | `/style-transfer` | Transfert de style artistique |
| Galerie | `/gallery` | Parcourir toutes les creations |

### Raccourcis clavier

| Touche | Action |
|--------|--------|
| `?` | Afficher l'aide |
| `Ctrl + H` | Accueil |
| `Ctrl + G` | Galerie |
| `Echap` | Fermer les modales |
| `Ctrl + Entree` | Soumettre un formulaire |
| `Alt + Gauche` | Page precedente |

---

## Modules

### Art generatif (POO)

```python
class Shape:           # Classe de base
class Circle(Shape):   # Cercles
class Square(Shape):   # Carres
class Triangle(Shape): # Triangles
```

Algorithmes : positionnement aleatoire, recursion fractale, spirales mathematiques.

### Traitement d'images

1. Upload -> Secure filename -> Resize (800x600)
2. Application du filtre
3. Sauvegarde et affichage cote-a-cote

Fonctions cles : `apply_image_filter()`, `apply_glitch_effect()`, `apply_watercolor_effect()`, `apply_cartoon_effect()`

### Traitement audio

1. Upload -> PyDub -> Application effet
2. Generation du spectrogramme
3. Export MP3 (320kbps)

Fonctions cles : `change_speed()`, `change_pitch()`, `add_echo()`, `generate_ambient_soundscape()`

### Style transfer

- Primaire : TensorFlow Hub (modele Magenta) — si TF installe
- Fallback : Filtres OpenCV (`cv2.stylization`, `cv2.edgePreservingFilter`)
- Entree : Image contenu + choix du style
- Sortie : Image stylisee 800x600

---

## ❓ Depannage

| Erreur | Solution |
|--------|----------|
| `RuntimeWarning: Couldn't find ffmpeg` | Relancer `install_ffmpeg.bat` |
| `[WinError 2]` sur l'audio | ffmpeg/ffprobe manquants → idem |
| `[TF] TensorFlow not available` | Normal sur Python 3.14. Voir la [section dediee](#-tensorflow--style-transfer-ml) |
| `Port 5000 deja utilise` | Changer `port=5001` dans `backend/app.py` |
| `Module non trouve` | `pip install -r backend\requirements.txt` |
| `Fichier trop volumineux` | Limite 50 MB modifiable dans `app.py` |
| `Could not establish connection` | Erreur console Chrome — sans consequence |
| L'application ne demarre pas | Verifier : `cd` dans le bon dossier, venv active, `python backend/app.py` |

---

## Structure du projet

```
interactive_generative_studio/
├── backend/            # app.py, data.py, requirements.txt
├── frontend/
│   ├── static/         # CSS, JS, plots, favicon
│   └── templates/      # Jinja2 (base, home, generative, ...)
├── media/              # audio/, generated/, uploads (gitignore)
├── venv/               # Environnement virtuel (gitignore)
├── setup.bat / setup.sh
├── run.bat / run.sh
├── install_ffmpeg.bat / install_ffmpeg.sh
└── README.md
```

---

## Credits

**Projet :** Interactive Generative Studio  
**Cours :** Digital Creativity using Python  
**Etablissement :** National School of Applied Sciences - Tangier  
**Annee :** 2025

---

**Construit avec Python, Flask, et des principes de codage creatif.**
