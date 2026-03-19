# Architecture de SynapseChat (Chatbot Avancé)

## Vue d'ensemble

Cette application est un chatbot conversationnel avancé avec support multi-provider IA et RAG (Retrieval Augmented Generation).

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ ChatInterface│  │ SettingsPanel│  │  MessageList       │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│         │                  │                     │              │
│         └──────────────────┴─────────────────────┘              │
│                            │                                     │
│                    ┌───────▼───────┐                           │
│                    │  API Service   │                           │
│                    │  (Axios/Fetch) │                           │
│                    └───────┬───────┘                           │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTP/WebSocket
┌────────────────────────────┼─────────────────────────────────┐
│                     BACKEND (FastAPI)                          │
│                    ┌───────▼───────┐                          │
│                    │   API Routes   │                          │
│                    │  /api/chat     │                          │
│                    │  /api/docs     │                          │
│                    └───────┬───────┘                          │
│                            │                                    │
│        ┌──────────────────┼──────────────────┐                │
│        │                  │                   │                │
│   ┌────▼────┐      ┌─────▼──────┐     ┌─────▼──────┐        │
│   │  Chat   │      │    RAG      │     │  Provider  │        │
│   │ Service │      │  Service    │     │  Factory   │        │
│   └────┬────┘      └─────┬──────┘     └─────┬──────┘        │
│        │                  │                   │                │
│        │           ┌──────▼──────┐           │                │
│        │           │  ChromaDB   │           │                │
│        │           │  (Vectors)  │           │                │
│        │           └─────────────┘           │                │
│        │                                      │                │
│        │           ┌──────────────────────────┼────────┐      │
│        │           │                          │        │      │
│        │      ┌────▼─────┐  ┌────▼────┐  ┌──▼──────┐ │      │
│        │      │  Claude  │  │ OpenAI  │  │ Ollama  │ │      │
│        │      │ Provider │  │Provider │  │Provider │ │      │
│        │      └──────────┘  └─────────┘  └─────────┘ │      │
│        │                                              │      │
│   ┌────▼────┐                                         │      │
│   │Database │                                         │      │
│   │ (Async) │                                         │      │
│   └────┬────┘                                         │      │
└─────────┼──────────────────────────────────────────────────┘
          │
    ┌─────▼─────┐      ┌──────────┐      ┌──────────┐
    │PostgreSQL │      │  Redis   │      │  Ollama  │
    │(Conversations)│   │ (Cache)  │      │  (GPU)   │
    └───────────┘      └──────────┘      └──────────┘
```

## Composants Principaux

### Frontend (React + TypeScript)

**Technologies:**
- React 18 avec TypeScript
- Zustand pour la gestion d'état
- Tailwind CSS pour le styling
- Axios pour les requêtes HTTP
- React Markdown pour le rendu des messages

**Composants clés:**
- `ChatInterface`: Interface principale du chat
- `MessageList`: Affichage des messages avec support Markdown
- `SettingsPanel`: Configuration des providers et paramètres

**Fonctionnalités:**
- Support du streaming des réponses
- Upload de documents
- Gestion de l'historique
- Switch entre providers
- Interface responsive

### Backend (Python + FastAPI)

**Technologies:**
- FastAPI pour l'API REST
- SQLAlchemy pour l'ORM (async)
- ChromaDB pour les embeddings
- SentenceTransformers pour les embeddings

**Architecture en couches:**

1. **API Layer** (`app/api/`)
   - Routes REST
   - Validation des requêtes
   - Gestion des erreurs

2. **Service Layer** (`app/services/`)
   - `ChatService`: Logique métier du chat
   - `RAGService`: Recherche sémantique
   - `AIProviderFactory`: Création des providers
   - Providers spécifiques (Claude, OpenAI, Ollama)

3. **Model Layer** (`app/models/`)
   - Modèles de base de données
   - Relations entre entités

4. **Schema Layer** (`app/schemas/`)
   - Validation Pydantic
   - Sérialisation/Désérialisation

### Providers IA

#### 1. Claude Provider (Anthropic)
- API Cloud
- Modèle: claude-sonnet-4-20250514
- Streaming natif
- Pas d'embeddings natifs (utilise SentenceTransformers)

#### 2. OpenAI Provider
- API Cloud
- Modèle: gpt-4-turbo-preview
- Streaming natif
- Embeddings: text-embedding-ada-002

#### 3. Ollama Provider
- LLM local
- Support GPU NVIDIA
- Modèles disponibles: llama2, mistral, codellama, etc.
- Embeddings locaux ou fallback

### RAG (Retrieval Augmented Generation)

**Pipeline:**
1. Upload de document
2. Extraction du texte (PDF, DOCX, TXT, MD)
3. Découpage en chunks (500 caractères avec overlap)
4. Génération d'embeddings
5. Stockage dans ChromaDB
6. Recherche sémantique lors des requêtes
7. Injection du contexte dans le prompt

**Technologies:**
- ChromaDB pour le stockage vectoriel
- SentenceTransformers pour les embeddings
- pypdf, python-docx pour l'extraction

### Base de données

**PostgreSQL:**
- Tables:
  - `conversations`: Historique des conversations
  - `messages`: Messages individuels
  - `documents`: Documents uploadés

**Redis:**
- Cache des sessions
- Rate limiting
- Données temporaires

## Flux de données

### Conversation normale

```
User → Frontend → Backend API → ChatService
                                     ↓
                              Provider Factory
                                     ↓
                         [Claude|OpenAI|Ollama]
                                     ↓
                              Response → User
                                     ↓
                              PostgreSQL (save)
```

### Conversation avec RAG

```
User → Frontend → Backend API → ChatService
                                     ↓
                              RAGService
                                     ↓
                              Query Embedding
                                     ↓
                         ChromaDB (similarity search)
                                     ↓
                         Relevant Chunks → Context
                                     ↓
                         Enhanced Prompt → Provider
                                     ↓
                              Response → User
```

### Upload de document

```
User → Frontend → Backend API → Document Table
                                     ↓
                         Text Extraction (PDF/DOCX/etc)
                                     ↓
                         Text Chunking (500 chars)
                                     ↓
                         Generate Embeddings
                                     ↓
                         Store in ChromaDB
```

## Sécurité

- Validation des entrées avec Pydantic
- CORS configuré
- Rate limiting avec Redis
- Pas de stockage des clés API côté frontend
- Sanitization des uploads

## Performance

- Connexions async avec PostgreSQL
- Pool de connexions optimisé
- Cache Redis pour les données fréquentes
- Streaming pour les réponses longues
- Embeddings en batch

## Scalabilité

- Architecture stateless
- Services containerisés
- Base de données relationnelle robuste
- Support horizontal scaling (avec load balancer)
- ChromaDB peut être remplacé par Pinecone/Weaviate

## Déploiement

**Développement:**
```bash
docker-compose up -d
```

**Production:**
- Utiliser des secrets pour les clés API
- Reverse proxy (Nginx/Traefik)
- SSL/TLS
- Monitoring (Prometheus/Grafana)
- Logging centralisé

## Extensibilité

**Ajouter un nouveau provider:**
1. Créer une classe héritant de `AIProvider`
2. Implémenter les méthodes requises
3. L'ajouter dans `AIProviderFactory`
4. Configurer dans `.env`

**Ajouter un nouveau type de document:**
1. Ajouter l'extension dans `ALLOWED_EXTENSIONS`
2. Ajouter la logique d'extraction dans `/documents/upload`
3. Tester l'extraction et le chunking

**Ajouter une fonctionnalité:**
1. Créer le service backend approprié
2. Créer la route API
3. Créer le composant frontend
4. Mettre à jour le store si nécessaire

## Monitoring

**Endpoints de santé:**
- `/`: Basic health check
- `/api/health`: Détails système (DB, IA, RAG)

**Métriques à surveiller:**
- Temps de réponse API
- Taux d'erreur
- Utilisation mémoire (ChromaDB)
- Latence provider IA
- Taille de la base de données
