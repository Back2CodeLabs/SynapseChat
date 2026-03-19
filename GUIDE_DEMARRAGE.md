# 🚀 Guide de Démarrage Rapide

## Prérequis

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optionnel mais recommandé)
- PostgreSQL 16+ (si installation manuelle)
- Redis 7+ (si installation manuelle)

## Option 1: Avec Docker (Recommandé)

### 1. Configuration initiale

```bash
# Copier les fichiers d'environnement
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Éditer backend/.env et ajouter vos clés API
nano backend/.env
```

### 2. Configuration des clés API

Dans `backend/.env`, configurez au moins un provider:

```bash
# Pour Claude (recommandé)
AI_PROVIDER=claude
ANTHROPIC_API_KEY=votre_cle_api_anthropic

# OU pour OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=votre_cle_api_openai

# OU pour Ollama (local, sans clé nécessaire)
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2
```

### 3. Lancer l'application

```bash
# Sans Ollama (recommandé pour démarrer)
docker-compose up -d

# Avec Ollama (nécessite GPU NVIDIA)
docker-compose --profile ollama up -d

# Voir les logs
docker-compose logs -f
```

### 4. Accéder à l'application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

### 5. Installer un modèle Ollama (si utilisation d'Ollama)

```bash
# Entrer dans le conteneur Ollama
docker exec -it synapsechat-ollama bash

# Télécharger un modèle (choisir parmi: llama2, mistral, codellama, etc.)
ollama pull llama2

# Vérifier les modèles installés
ollama list

# Quitter
exit
```

## Option 2: Installation Manuelle

### 1. Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
nano .env  # Éditer avec vos clés API

# Lancer PostgreSQL et Redis
# (Assurez-vous qu'ils sont installés et démarrés)

# Lancer le serveur
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.example .env

# Lancer le serveur de développement
npm run dev
```

## Configuration des Providers IA

### Claude (Anthropic)

1. Créez un compte sur https://console.anthropic.com
2. Générez une clé API
3. Ajoutez-la dans `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   AI_PROVIDER=claude
   ```

### OpenAI

1. Créez un compte sur https://platform.openai.com
2. Générez une clé API
3. Ajoutez-la dans `backend/.env`:
   ```
   OPENAI_API_KEY=sk-...
   AI_PROVIDER=openai
   ```

### Ollama (Local)

1. Installez Ollama: https://ollama.ai
2. Téléchargez un modèle:
   ```bash
   ollama pull llama2
   # ou
   ollama pull mistral
   ```
3. Configurez dans `backend/.env`:
   ```
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

## Configuration du RAG

### Activer le RAG

Dans `backend/.env`:
```bash
ENABLE_RAG=True
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_CHUNKS_TO_RETRIEVE=5
```

### Uploader des documents

1. Accédez au frontend (http://localhost:3000)
2. Cliquez sur l'icône de documents
3. Uploadez vos fichiers (PDF, TXT, DOCX, MD)
4. Activez le RAG dans les paramètres
5. Posez des questions sur vos documents!

## Fonctionnalités

✅ **Multi-Provider IA**: Basculez facilement entre Claude, OpenAI, et Ollama
✅ **RAG**: Upload de documents pour enrichir les réponses
✅ **Streaming**: Réponses en temps réel
✅ **Historique**: Sauvegarde automatique des conversations
✅ **Multi-utilisateurs**: Support de plusieurs utilisateurs
✅ **Interface moderne**: UI responsive avec Tailwind CSS
✅ **API REST**: Documentation OpenAPI automatique

## Commandes Utiles

```bash
# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Redémarrer un service
docker-compose restart backend

# Arrêter tout
docker-compose down

# Supprimer les volumes (⚠️ supprime les données)
docker-compose down -v

# Reconstruire les images
docker-compose build --no-cache

# Accéder à la base de données
docker exec -it synapsechat-postgres psql -U synapsechat -d synapsechat_db
```

## Dépannage

### Le backend ne démarre pas
- Vérifiez que PostgreSQL et Redis sont accessibles
- Vérifiez vos clés API dans `.env`
- Consultez les logs: `docker-compose logs backend`

### Ollama ne fonctionne pas
- Assurez-vous d'avoir un GPU NVIDIA avec les drivers installés
- Téléchargez un modèle: `docker exec -it synapsechat-ollama ollama pull llama2`
- Vérifiez: `docker exec -it synapsechat-ollama ollama list`

### Le RAG ne trouve pas mes documents
- Vérifiez que RAG est activé: `ENABLE_RAG=True`
- Assurez-vous d'avoir uploadé des documents
- Activez le RAG dans les paramètres de l'interface

### Erreur de connexion API
- Vérifiez que le backend est démarré: http://localhost:8000/api/health
- Vérifiez l'URL dans `frontend/.env`: `VITE_API_URL=http://localhost:8000/api`

## Support

Pour toute question ou problème:
1. Consultez les logs: `docker-compose logs -f`
2. Vérifiez la santé du système: http://localhost:8000/api/health
3. Consultez la documentation de l'API: http://localhost:8000/docs

## Contribution

N'hésitez pas à contribuer en créant des issues ou des pull requests!
