# 🤖 Agent IA Local avec Base de Connaissance Google Drive

Application complète combinant **Ollama** (IA locale), **Google Drive** (base de connaissance), et **Python** (backend).

## ✨ Fonctionnalités

- ✅ **100% Local & Gratuit** - Aucune clé API requise
- ✅ **Base de Connaissance** - Indexe vos PDF, images, documents depuis Google Drive
- ✅ **Recherche Intelligente** - L'IA cherche automatiquement les documents pertinents
- ✅ **Modèles IA Locaux** - Mistral, Llama2, Neural-chat, etc.
- ✅ **Interface Moderne** - Sidebar intégrée, gestion des documents

## 🚀 Installation Complète

### Étape 1 : Installer les dépendances système

#### Windows
```bash
# Installer Python 3.10+ depuis https://python.org
# Vérifier l'installation
python --version
```

#### macOS
```bash
brew install python@3.11
python3 --version
```

#### Linux
```bash
sudo apt-get install python3-pip python3-dev
python3 --version
```

### Étape 2 : Installer Ollama

1. Téléchargez depuis : https://ollama.ai
2. Installez et lancez l'application
3. Vérifiez dans le terminal :
   ```bash
   ollama --version
   ```

### Étape 3 : Télécharger un modèle Ollama

Choisissez selon votre PC :

**Rapide (2-4 GB)** :
```bash
ollama pull mistral
```

**Équilibré (4-7 GB)** :
```bash
ollama pull neural-chat
```

**Puissant (7+ GB)** :
```bash
ollama pull llama2
```

Lancez Ollama :
```bash
ollama serve
```

Vous devriez voir :
```
listening on 127.0.0.1:11434
```

### Étape 4 : Configurer Google Drive

1. Allez sur : https://console.cloud.google.com/
2. Créez un nouveau projet
3. Activez l'API Google Drive
4. Créez des "Identifiants OAuth 2.0" (Application de bureau)
5. Téléchargez le JSON
6. **Renommez-le `credentials.json`** et placez-le dans le dossier du projet

### Étape 5 : Installer les dépendances Python

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 6 : Lancer le backend

```bash
python app.py
```

Vous devriez voir :
```
🚀 Serveur lancé sur http://localhost:5000
📚 Base de connaissance Google Drive + Ollama
```

### Étape 7 : Ouvrir l'interface

1. Ouvrez `index.html` dans votre navigateur
2. Cliquez sur **🔐 Connecter Google**
3. Connectez-vous à votre compte Google
4. Cliquez sur **📚 Charger la Base** (le dossier s'appelle `IA-Documents` par défaut)
5. Posez des questions ! 💬

---

## 📁 Structure des dossiers

```
claude-chatbot-app/
├── app.py                 # Backend Python (Flask)
├── index.html            # Interface web
├── requirements.txt      # Dépendances Python
├── credentials.json      # Google OAuth (à créer)
├── token.pickle          # Token Google (créé auto)
└── knowledge_base.json   # Base de connaissance (créée auto)
```

## 🗂️ Organisation Google Drive

Créez un dossier `IA-Documents` dans votre Google Drive avec :
- 📄 Fichiers PDF
- 📸 Images PNG/JPG
- 📝 Fichiers TXT
- 📋 Documents Markdown

L'app indexera tout automatiquement !

---

## 🎯 Modèles recommandés

| Modèle | Taille | Vitesse | Qualité | Mémoire RAM |
|--------|--------|---------|---------|-----------|
| mistral | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| neural-chat | 5GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | 12GB |
| llama2 | 7GB | ⚡ | ⭐⭐⭐⭐⭐ | 16GB |
| orca-mini | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | 4GB |

---

## 🛠️ Dépannage

### ❌ "Impossible de se connecter à Ollama"
```
✓ Vérifiez que vous avez lancé: ollama serve
✓ Vérifiez le port 11434: http://localhost:11434
✓ Redémarrez Ollama
```

### ❌ "Erreur d'authentification Google"
```
✓ Vérifiez que credentials.json est dans le bon dossier
✓ Supprimez token.pickle et recommencez
✓ Vérifiez que l'API Google Drive est activée
```

### ❌ "Modèle introuvable"
```bash
# Vérifiez les modèles disponibles
ollama list

# Retéléchargez si besoin
ollama pull mistral
```

### ❌ "C'est trop lent"
```
✓ Utilisez un modèle plus petit (mistral, orca-mini)
✓ Augmentez votre RAM
✓ Fermer les autres applications
✓ Utilisez un GPU si possible
```

### ❌ "Backend ne démarre pas"
```bash
# Vérifier Python
python --version

# Vérifier que Flask est installé
pip list | grep flask

# Réinstaller
pip install -r requirements.txt
```

---

## 📚 API Backend disponible

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/auth/login` | POST | Authentifier Google Drive |
| `/api/knowledge/build` | POST | Construire la base de connaissance |
| `/api/knowledge/status` | GET | État de la base |
| `/api/knowledge/search` | POST | Chercher dans la base |
| `/api/chat` | POST | Envoyer un message à l'IA |
| `/api/documents` | GET | Lister les documents |
| `/health` | GET | Vérifier que le serveur fonctionne |

---

## 🚀 Utilisation avancée

### Modifier le dossier Google Drive
Dans `index.html`, changez le nom du dossier :
```javascript
value="IA-Documents"  // Remplacer par votre dossier
```

### Améliorer la recherche
Modifiez la fonction `search_knowledge_base()` dans `app.py` pour utiliser des embeddings (plus puissant).

### Ajouter un historique persistant
Modifiez la base de données pour stocker les conversations dans Google Drive.

---

## 📝 Notes importantes

- 🔒 Votre clé Google n'est jamais partagée
- 💾 Les fichiers sont téléchargés mais pas stockés
- 🚀 L'IA tourne 100% en local
- 📊 Les documents sont indexés automatiquement

---

## 🆘 Support

- **Ollama** : https://ollama.ai
- **Google Drive API** : https://developers.google.com/drive
- **Flask** : https://flask.palletsprojects.com/

---

**Créé avec ❤️ - Agent IA Local Gratuit**
