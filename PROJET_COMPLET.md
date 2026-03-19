# 🤖 SynapseChat > Chatbot Avancé - Stack Full-Stack Complète

## 📦 Contenu du Projet

Votre chatbot avancé est prêt ! Voici ce qui a été créé :

### 🎯 Structure du Projet

```
synapsechat/
├── backend/                    # API Python FastAPI
│   ├── app/
│   │   ├── api/               # Routes API
│   │   ├── core/              # Configuration
│   │   ├── models/            # Modèles DB
│   │   ├── schemas/           # Schémas Pydantic
│   │   └── services/          # Logique métier
│   │       ├── ai_provider.py      # Interface abstraite
│   │       ├── claude_provider.py  # Provider Claude
│   │       ├── openai_provider.py  # Provider OpenAI
│   │       ├── ollama_provider.py  # Provider Ollama
│   │       ├── ai_factory.py       # Factory pattern
│   │       ├── rag_service.py      # Service RAG
│   │       └── chat_service.py     # Service principal
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                   # Interface React
│   ├── src/
│   │   ├── components/        # Composants React
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── SettingsPanel.tsx
│   │   ├── services/          # API client
│   │   ├── store/             # Zustand store
│   │   └── types/             # Types TypeScript
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
│
├── docker-compose.yml          # Orchestration Docker
├── setup.sh                    # Script de setup automatique
├── setup-ollama.sh            # Configuration Ollama
├── README.md                   # Documentation principale
├── GUIDE_DEMARRAGE.md         # Guide de démarrage rapide
├── ARCHITECTURE.md            # Documentation architecture
└── .gitignore

```

## ✨ Fonctionnalités Implémentées

### Backend
✅ Support multi-providers IA (Claude, OpenAI, Ollama)
✅ Switch dynamique entre providers
✅ RAG avec ChromaDB pour la recherche sémantique
✅ Upload de documents (PDF, DOCX, TXT, MD)
✅ Streaming des réponses en temps réel
✅ Historique des conversations (PostgreSQL)
✅ Cache Redis pour les sessions
✅ API REST complète avec documentation auto-générée
✅ Validation des données avec Pydantic
✅ Architecture async pour les performances
✅ Health check endpoints

### Frontend
✅ Interface moderne et responsive (Tailwind CSS)
✅ Chat en temps réel avec streaming
✅ Gestion de l'historique des conversations
✅ Upload de documents drag & drop
✅ Panneau de configuration des providers
✅ Support Markdown dans les messages
✅ Coloration syntaxique du code
✅ Gestion d'état avec Zustand
✅ TypeScript pour la sécurité des types

### Infrastructure
✅ Docker Compose pour tout orchestrer
✅ PostgreSQL pour la persistance
✅ Redis pour le cache
✅ Support optionnel d'Ollama (LLM local)
✅ Scripts de setup automatisés
✅ Configuration par variables d'environnement

## 🚀 Démarrage Rapide

### Prérequis
- Docker & Docker Compose
- Clé API pour Claude OU OpenAI (ou aucune pour Ollama)

### Installation en 3 étapes

1. **Configuration automatique:**
   ```bash
   cd synapsechat
   ./setup.sh
   ```

2. **Accéder à l'application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentation API: http://localhost:8000/docs

3. **Commencer à chatter!**
   - Ouvrez http://localhost:3000
   - Posez votre première question
   - Uploadez des documents pour tester le RAG

## 🎮 Utilisation

### Changer de Provider IA

1. Via l'interface:
   - Cliquez sur l'icône ⚙️ (Paramètres)
   - Sélectionnez le provider désiré
   - Cliquez sur "Appliquer"

2. Via le fichier .env:
   ```bash
   # backend/.env
   AI_PROVIDER=claude  # ou openai, ou ollama
   ```

### Activer le RAG

1. Uploadez des documents:
   - Cliquez sur l'icône 📄
   - Sélectionnez vos fichiers (PDF, DOCX, TXT, MD)
   - Attendez le traitement

2. Activez le RAG:
   - Allez dans Paramètres
   - Cochez "Activer le RAG"

3. Posez des questions sur vos documents!

### Utiliser Ollama (LLM Local)

1. Démarrer avec Ollama:
   ```bash
   docker-compose --profile ollama up -d
   ```

2. Télécharger un modèle:
   ```bash
   ./setup-ollama.sh
   # ou manuellement:
   docker exec -it synapsechat-ollama ollama pull llama2
   ```

3. Configurer le provider:
   ```bash
   # backend/.env
   AI_PROVIDER=ollama
   OLLAMA_MODEL=llama2
   ```

4. Redémarrer:
   ```bash
   docker-compose restart backend
   ```

## 📊 Providers IA Disponibles

### 1. Claude (Anthropic) - Recommandé ⭐
- **Avantages:** Excellent en français, conversations naturelles, raisonnement
- **Modèle:** claude-sonnet-4-20250514
- **Setup:** Clé API requise (https://console.anthropic.com)
- **Coût:** Pay-as-you-go

### 2. OpenAI (GPT-4)
- **Avantages:** Très performant, large contexte
- **Modèle:** gpt-4-turbo-preview
- **Setup:** Clé API requise (https://platform.openai.com)
- **Coût:** Pay-as-you-go

### 3. Ollama (Local) - Gratuit 🆓
- **Avantages:** Gratuit, privé, aucune clé API
- **Modèles:** llama2, mistral, codellama, etc.
- **Setup:** GPU NVIDIA recommandé
- **Coût:** Gratuit (seulement l'électricité)

## 🔧 Configuration Avancée

### Variables d'Environnement (backend/.env)

```bash
# Provider IA
AI_PROVIDER=claude                    # claude | openai | ollama
ANTHROPIC_API_KEY=sk-ant-xxx         # Pour Claude
OPENAI_API_KEY=sk-xxx                # Pour OpenAI
OLLAMA_BASE_URL=http://ollama:11434  # Pour Ollama
OLLAMA_MODEL=llama2                   # Modèle Ollama

# RAG
ENABLE_RAG=True
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_CHUNKS_TO_RETRIEVE=5

# Base de données
DATABASE_URL=postgresql+asyncpg://synapsechat:synapsechat123@postgres:5432/synapsechat_db
REDIS_URL=redis://redis:6379/0

# Conversation
MAX_CONVERSATION_HISTORY=20
MAX_MESSAGE_LENGTH=4000
```

## 📚 Documentation

- **README.md** - Vue d'ensemble et fonctionnalités
- **GUIDE_DEMARRAGE.md** - Instructions détaillées de démarrage
- **ARCHITECTURE.md** - Documentation technique complète

## 🐛 Dépannage

### Le backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs backend

# Vérifier la connexion DB
docker-compose logs postgres

# Redémarrer
docker-compose restart backend
```

### Ollama ne fonctionne pas
```bash
# Vérifier qu'un modèle est installé
docker exec -it synapsechat-ollama ollama list

# Télécharger un modèle
docker exec -it synapsechat-ollama ollama pull llama2
```

### Le RAG ne trouve pas mes documents
- Vérifiez que `ENABLE_RAG=True` dans backend/.env
- Assurez-vous d'avoir uploadé des documents
- Activez le RAG dans les paramètres de l'interface

## 🛠️ Commandes Utiles

```bash
# Démarrer tout
docker-compose up -d

# Démarrer avec Ollama
docker-compose --profile ollama up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Redémarrer un service
docker-compose restart backend

# Reconstruire
docker-compose build --no-cache

# Nettoyer tout (⚠️ supprime les données)
docker-compose down -v
```

## 🎯 Prochaines Étapes

1. **Testez les 3 providers** pour voir lequel vous préférez
2. **Uploadez des documents** pour tester le RAG
3. **Personnalisez l'interface** (couleurs, logo, etc.)
4. **Ajoutez des fonctionnalités** selon vos besoins
5. **Déployez en production** si satisfait

## 📝 Notes Importantes

- 🔑 **Clés API:** Ne jamais commiter vos clés API dans Git
- 💾 **Données:** Les conversations sont sauvegardées en base de données
- 🔒 **Sécurité:** Changez les mots de passe par défaut en production
- 📊 **Monitoring:** Consultez régulièrement `/api/health`

## 🤝 Support

Pour toute question:
1. Consultez la documentation dans les fichiers .md
2. Vérifiez les logs: `docker-compose logs -f`
3. Testez l'API: http://localhost:8000/docs

## 🎉 Félicitations !

Votre chatbot avancé est prêt à l'emploi avec:
- ✅ 3 providers IA au choix
- ✅ RAG pour les documents
- ✅ Interface moderne
- ✅ Architecture scalable
- ✅ Prêt pour la production

Bon développement ! 🚀
