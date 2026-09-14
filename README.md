# 🤖 Agent IA Local avec Ollama

Une application chatbot IA qui fonctionne **100% localement**, gratuitement, sans clé API !

## ✨ Fonctionnalités

- ✅ Fonctionne hors ligne (offline)
- ✅ Gratuit, aucune clé API requise
- ✅ Interface web belle et simple
- ✅ Historique de conversation
- ✅ Modèles IA locaux (Llama, Mistral, etc.)

## 🚀 Installation

### Étape 1 : Installer Ollama

1. Téléchargez Ollama : https://ollama.ai
2. Installez et lancez l'application
3. Ouvrez un terminal/command prompt et vérifiez :
   ```bash
   ollama --version
   ```

### Étape 2 : Télécharger un modèle IA

Choisissez un modèle selon votre ordinateur :

**Petit & rapide (2-4 GB)** :
```bash
ollama pull mistral
```

**Moyen & bon (4-7 GB)** :
```bash
ollama pull neural-chat
```

**Plus puissant (7+ GB)** :
```bash
ollama pull llama2
```

### Étape 3 : Lancer Ollama

```bash
ollama serve
```

Vous devriez voir :
```
listening on 127.0.0.1:11434
```

### Étape 4 : Ouvrir l'application

1. Ouvrez `index.html` dans votre navigateur
2. Configurez le modèle (ex: `mistral`)
3. Commencez à discuter ! 💬

## 📝 Configuration

- **Adresse Ollama** : `http://localhost:11434` (par défaut)
- **Modèle** : Changez le modèle dans l'interface (onglet ⚙️)
- **Historique** : Sauvegardé localement dans votre navigateur

## 🎯 Modèles recommandés

| Modèle | Taille | Vitesse | Qualité |
|--------|--------|---------|---------|
| mistral | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| neural-chat | 5GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| llama2 | 7GB | ⚡ | ⭐⭐⭐⭐⭐ |
| orca-mini | 2GB | ⚡⚡⚡ | ⭐⭐⭐ |

## 🛠️ Dépannage

**❌ "Impossible de se connecter"**
- Vérifiez que Ollama est lancé avec `ollama serve`
- Vérifiez que le port 11434 est accessible

**❌ "Modèle introuvable"**
- Assurez-vous d'avoir téléchargé le modèle : `ollama pull [nom-modèle]`
- Vérifiez le nom exact du modèle

**❌ "C'est lent"**
- Utilisez un modèle plus petit (mistral, orca-mini)
- Augmentez la RAM disponible
- Utilisez un GPU si possible

## 📚 En savoir plus

- Documentation Ollama : https://ollama.ai
- Modèles disponibles : https://ollama.ai/library
- GitHub Ollama : https://github.com/ollama/ollama

---

**Créé avec ❤️ par AntoineGiaco**
