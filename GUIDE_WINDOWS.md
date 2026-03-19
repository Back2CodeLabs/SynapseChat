# 🪟 Guide de Démarrage - Windows avec Ollama distant

## 📋 Votre Configuration

- **OS**: Windows
- **Ollama**: VM distante à `http://localhost:11434`
- **Modèle**: Mistral
- **Docker**: Docker Desktop pour Windows

## 🚀 Installation Rapide

### Étape 1 : Vérifications préalables

1. **Docker Desktop est installé et démarré**
   - Téléchargez depuis : https://www.docker.com/products/docker-desktop/
   - Assurez-vous qu'il est en cours d'exécution (icône dans la barre des tâches)

2. **Votre VM Ollama est accessible**
   - Testez dans un navigateur : http://localhost:11434
   - Ou dans PowerShell :
   ```powershell
   curl http://localhost:11434/api/tags
   ```

3. **Vérifiez que Mistral est installé sur Ollama**
   - Connectez-vous à votre VM et vérifiez :
   ```bash
   ollama list
   ```
   - Si Mistral n'est pas installé :
   ```bash
   ollama pull mistral
   ```

### Étape 2 : Configuration automatique

Double-cliquez sur :
```
setup-windows.bat
```

Ce script va :
- ✅ Créer le fichier `backend\.env` avec l'URL de votre Ollama distant
- ✅ Créer le fichier `frontend\.env`
- ✅ Configurer automatiquement Mistral comme provider

### Étape 3 : Démarrer l'application

Double-cliquez sur :
```
start-windows.bat
```

Ce script va :
- ✅ Vérifier que Docker est démarré
- ✅ Démarrer PostgreSQL, Redis, Backend et Frontend
- ✅ Ouvrir automatiquement le navigateur

**Premier démarrage :** Cela peut prendre 5-10 minutes pour télécharger les images Docker.

### Étape 4 : Accéder à l'application

Une fois démarré, l'application sera accessible sur :

- 🌐 **Frontend** : http://localhost:3000
- 🔧 **Backend API** : http://localhost:8000
- 📚 **Documentation API** : http://localhost:8000/docs
- ❤️ **Health Check** : http://localhost:8000/api/health

## 🔍 Vérification de la Configuration

### Test 1 : Vérifier que tous les services sont démarrés

Ouvrez PowerShell et tapez :
```powershell
docker-compose ps
```

Vous devriez voir 4 services en "running" :
- synapsechat-postgres
- synapsechat-redis
- synapsechat-backend
- synapsechat-frontend

### Test 2 : Tester la connexion à Ollama

Ouvrez : http://localhost:8000/api/health

Vous devriez voir :
```json
{
  "status": "healthy",
  "ai_provider": "ollama",
  "ai_available": true,
  ...
}
```

Si `ai_available` est `false`, vérifiez que votre VM Ollama est accessible.

### Test 3 : Premier message

1. Allez sur http://localhost:3000
2. Tapez : "Bonjour, peux-tu te présenter ?"
3. Vous devriez recevoir une réponse de Mistral via Ollama

## 🛠️ Commandes Utiles Windows

### Voir les logs en temps réel

```powershell
docker-compose logs -f
```

Pour voir les logs d'un service spécifique :
```powershell
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Redémarrer un service

```powershell
docker-compose restart backend
```

### Arrêter l'application

Double-cliquez sur `stop-windows.bat` ou :
```powershell
docker-compose down
```

### Reconstruire après une modification

```powershell
docker-compose build --no-cache
docker-compose up -d
```

### Nettoyer complètement (⚠️ supprime les données)

```powershell
docker-compose down -v
```

## 📊 Structure des Fichiers

```
synapsechat/
├── setup-windows.bat       ⭐ Configuration automatique
├── start-windows.bat       ⭐ Démarrer l'application
├── stop-windows.bat        ⭐ Arrêter l'application
├── docker-compose.yml      📝 Configuration Docker (modifié pour Ollama distant)
├── backend/
│   ├── .env               ⚙️ Configuration backend (créé par setup-windows.bat)
│   └── ...
└── frontend/
    ├── .env               ⚙️ Configuration frontend
    └── ...
```

## 🔧 Configuration Manuelle (Alternative)

Si vous préférez configurer manuellement :

### 1. Créer `backend\.env`

Créez le fichier `backend\.env` avec ce contenu :

```env
# Configuration pour Ollama distant
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# RAG
ENABLE_RAG=True
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma
MAX_CHUNKS_TO_RETRIEVE=5

# Database (ne pas modifier)
DATABASE_URL=postgresql+asyncpg://synapsechat:synapsechat123@postgres:5432/synapsechat_db

# Redis (ne pas modifier)
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=change-this-in-production
ALGORITHM=HS256

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Conversation
MAX_CONVERSATION_HISTORY=20
MAX_MESSAGE_LENGTH=4000
```

### 2. Créer `frontend\.env`

```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Démarrer

```powershell
docker-compose up -d
```

## 🐛 Dépannage

### Problème : "Docker n'est pas démarré"

**Solution :**
1. Ouvrez Docker Desktop
2. Attendez que l'icône de Docker dans la barre des tâches devienne verte
3. Relancez `start-windows.bat`

### Problème : "ai_available: false"

**Solution :**
1. Vérifiez que votre VM Ollama est accessible :
   ```powershell
   curl http://localhost:11434/api/tags
   ```

2. Si la VM n'est pas accessible :
   - Vérifiez que la VM est démarrée
   - Vérifiez le pare-feu Windows
   - Testez le ping : `ping localhost`

3. Vérifiez que Mistral est installé sur Ollama :
   ```bash
   # Sur votre VM
   ollama list
   ```

### Problème : "Port 3000 déjà utilisé"

**Solution :**
1. Trouvez le processus qui utilise le port :
   ```powershell
   netstat -ano | findstr :3000
   ```

2. Arrêtez-le ou modifiez le port dans `docker-compose.yml`

### Problème : Le frontend ne se connecte pas au backend

**Solution :**
1. Vérifiez que le backend est démarré :
   ```powershell
   curl http://localhost:8000/api/health
   ```

2. Vérifiez le fichier `frontend\.env` :
   ```
   VITE_API_URL=http://localhost:8000/api
   ```

3. Redémarrez le frontend :
   ```powershell
   docker-compose restart frontend
   ```

### Problème : "Error initializing database"

**Solution :**
1. Vérifiez les logs PostgreSQL :
   ```powershell
   docker-compose logs postgres
   ```

2. Redémarrez PostgreSQL :
   ```powershell
   docker-compose restart postgres
   ```

3. Si le problème persiste, réinitialisez la base :
   ```powershell
   docker-compose down -v
   docker-compose up -d
   ```

## 🎯 Tester les Fonctionnalités

### Test 1 : Chat simple

1. Ouvrez http://localhost:3000
2. Tapez : "Explique-moi ce qu'est un chatbot"
3. Mistral devrait répondre via Ollama

### Test 2 : RAG avec upload de document

1. Cliquez sur l'icône 📄 (Upload)
2. Uploadez un fichier PDF ou TXT
3. Attendez le traitement
4. Activez le RAG dans les paramètres (⚙️)
5. Posez une question sur votre document

### Test 3 : Streaming

1. Dans les paramètres, vérifiez que "Streaming activé" est coché
2. Posez une question longue
3. Vous devriez voir la réponse s'afficher mot par mot

## 📝 Changer de Modèle Ollama

Si vous voulez utiliser un autre modèle que Mistral :

1. Installez le modèle sur votre VM :
   ```bash
   ollama pull llama2
   # ou
   ollama pull codellama
   ```

2. Modifiez `backend\.env` :
   ```env
   OLLAMA_MODEL=llama2
   ```

3. Redémarrez le backend :
   ```powershell
   docker-compose restart backend
   ```

## 🔄 Ajouter Claude ou OpenAI (Optionnel)

Si vous voulez aussi utiliser Claude ou OpenAI :

1. Éditez `backend\.env`
2. Ajoutez votre clé API :
   ```env
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   # ou
   OPENAI_API_KEY=sk-xxxxx
   ```

3. Dans l'interface web, allez dans Paramètres (⚙️)
4. Sélectionnez le provider désiré

## 📞 Support

Si vous rencontrez des problèmes :

1. **Consultez les logs** :
   ```powershell
   docker-compose logs -f
   ```

2. **Vérifiez la santé du système** :
   http://localhost:8000/api/health

3. **Testez Ollama directement** :
   http://localhost:11434/api/tags

4. **Redémarrez tout** :
   ```powershell
   docker-compose down
   docker-compose up -d
   ```

## 🎉 Vous êtes prêt !

Votre chatbot est maintenant configuré pour utiliser Ollama (Mistral) sur votre VM distante !

Profitez de votre chatbot avancé avec RAG ! 🚀
