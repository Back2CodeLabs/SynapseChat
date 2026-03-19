# ⚡ Démarrage Ultra-Rapide - Windows

## 🎯 En 3 étapes simples

### ✅ Prérequis
- Docker Desktop installé et démarré
- VM Ollama accessible sur `http://localhost:11434`
- Modèle Mistral installé sur Ollama

---

## 📍 ÉTAPE 1 : Configuration (1 fois seulement)

Double-cliquez sur :
```
📄 setup-windows.bat
```

✅ Cela crée automatiquement les fichiers de configuration

---

## 🚀 ÉTAPE 2 : Démarrage

Double-cliquez sur :
```
📄 start-windows.bat
```

⏱️ Attendez 30 secondes - 2 minutes

✅ Le navigateur s'ouvrira automatiquement sur http://localhost:3000

---

## 💬 ÉTAPE 3 : Utilisation

1. Tapez votre question dans la zone de texte
2. Appuyez sur Entrée ou cliquez sur le bouton d'envoi
3. Profitez de Mistral via Ollama !

---

## 🛑 Pour arrêter

Double-cliquez sur :
```
📄 stop-windows.bat
```

---

## 🔍 Vérifications Rapides

### Le chatbot ne répond pas ?

1. **Testez Ollama** :
   - Double-cliquez sur `test-ollama.bat`
   - Ou ouvrez : http://localhost:11434/api/tags

2. **Vérifiez Docker** :
   - Ouvrez PowerShell
   - Tapez : `docker-compose ps`
   - Les 4 services doivent être "Up"

3. **Vérifiez la santé** :
   - Ouvrez : http://localhost:8000/api/health
   - Vérifiez que `ai_available: true`

### Logs

Pour voir ce qui se passe :
```powershell
docker-compose logs -f
```

---

## 🎨 Interface

```
┌─────────────────────────────────────────────┐
│  Synapse Chat               [📄] [⚙️]      │
│  Provider: ollama | RAG: Désactivé          │
├─────────────────────────────────────────────┤
│                                             │
│  👤  Bonjour, comment ça va ?              │
│                                             │
│  🤖  Bonjour ! Je vais bien, merci.        │
│      Comment puis-je vous aider             │
│      aujourd'hui ?                          │
│                                             │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│  Posez votre question...            [📤]   │
└─────────────────────────────────────────────┘
```

### Boutons :
- **📄** : Upload de documents (PDF, TXT, DOCX)
- **⚙️** : Paramètres (changer de provider, activer RAG, etc.)
- **📤** : Envoyer le message

---

## 🎯 Fonctionnalités Principales

### 💬 Chat Intelligent
- Conversations naturelles avec Mistral
- Streaming en temps réel
- Historique automatique

### 📚 RAG (Upload de Documents)
1. Cliquez sur 📄
2. Uploadez un PDF, TXT ou DOCX
3. Activez le RAG dans ⚙️
4. Posez des questions sur vos documents !

### ⚙️ Paramètres
- Changer de provider IA
- Activer/désactiver le RAG
- Activer/désactiver le streaming

---

## 📞 Besoin d'aide ?

Consultez :
- `GUIDE_WINDOWS.md` - Guide détaillé
- `GUIDE_DEMARRAGE.md` - Documentation complète
- Logs : `docker-compose logs -f`

---

## 🎉 C'est tout !

Votre chatbot avec Ollama (Mistral) est prêt à l'emploi !

**Astuce** : Pour de meilleures performances, gardez votre VM Ollama active pendant l'utilisation du chatbot.
