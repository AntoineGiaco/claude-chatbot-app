#!/bin/bash
# Script de démarrage pour l'Agent IA Local
# Utilisation: bash start.sh (ou ./start.sh sur macOS/Linux)

echo "🚀 Démarrage de l'Agent IA Local..."
echo ""

# Vérifier Python
echo "✓ Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi
python3 --version

# Vérifier Ollama
echo ""
echo "✓ Vérification d'Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama n'est pas installé - voir https://ollama.ai"
fi

# Créer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo ""
    echo "✓ Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement
echo "✓ Activation de l'environnement virtuel..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Installer les dépendances
echo "✓ Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier credentials.json
echo ""
if [ ! -f "credentials.json" ]; then
    echo "⚠️  credentials.json n'existe pas"
    echo "   Téléchargez-le depuis: https://console.cloud.google.com/"
    echo ""
fi

# Lancer le serveur
echo "✓ Démarrage du serveur Flask..."
echo ""
echo "🎉 Serveur lancé sur http://localhost:5000"
echo "📖 Ouvrez index.html dans votre navigateur"
echo ""
echo "Appuyez sur CTRL+C pour arrêter"
echo ""

python3 app.py
