# 🤖 Synapse Chat - Assistant Conversationnel Avancé

Un chatbot web moderne et avancé propulsé par Claude AI (Anthropic), avec gestion du contexte, historique des conversations et interface élégante.

## 🚀 Fonctionnalités

### Backend (Python + FastAPI)
- ✅ API REST complète avec FastAPI
- ✅ Intégration avec l'API Claude (Anthropic)
- ✅ Gestion du contexte conversationnel
- ✅ Base de données PostgreSQL pour l'historique
- ✅ Cache Redis pour les performances
- ✅ Gestion des sessions utilisateurs
- ✅ Génération automatique de titres de conversations

### Frontend (Vue.js 3 + TypeScript)
- ✅ Interface moderne et responsive avec Tailwind CSS
- ✅ Gestion d'état avec Pinia
- ✅ Sidebar avec liste des conversations
- ✅ Messages formatés en Markdown
- ✅ Animations et transitions fluides
- ✅ Support des raccourcis clavier
- ✅ Auto-scroll et indicateurs de chargement

## 📋 Prérequis

- Docker et Docker Compose
- Une clé API Anthropic (https://console.anthropic.com/)

## 🛠️ Installation

### 1. Cloner le projet

```bash
cd synapsechat
```

### 2. Configurer les variables d'environnement

Éditez le fichier `.env` à la racine du projet :

```bash
ANTHROPIC_API_KEY=votre_clé_api_anthropic
SECRET_KEY=votre_clé_secrète_aléatoire
```

### 3. Lancer avec Docker Compose

```bash
docker-compose up --build
```

L'application sera accessible :
- Frontend : http://localhost:5173
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## 📁 Structure du Projet

```
synapsechat/
├── backend/                  # Backend Python/FastAPI
│   ├── main.py              # Point d'entrée de l'application
│   ├── config.py            # Configuration
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── database.py          # Connexion DB et Redis
│   ├── claude_service.py    # Service Claude AI
│   ├── routes.py            # Routes API
│   ├── requirements.txt     # Dépendances Python
│   └── Dockerfile           # Image Docker backend
│
├── frontend/                 # Frontend Vue.js
│   ├── src/
│   │   ├── components/      # Composants Vue
│   │   │   ├── ChatMessage.vue
│   │   │   ├── ChatInput.vue
│   │   │   └── Sidebar.vue
│   │   ├── stores/          # Stores Pinia
│   │   │   └── chat.ts
│   │   ├── services/        # Services API
│   │   │   └── api.ts
│   │   ├── types/           # Types TypeScript
│   │   │   └── index.ts
│   │   ├── App.vue          # Composant principal
│   │   ├── main.ts          # Point d'entrée
│   │   └── style.css        # Styles globaux
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml        # Configuration Docker Compose
├── .env                      # Variables d'environnement
├── .gitignore
└── README.md
```

## 🔧 Développement

### Backend seul

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos configurations
uvicorn main:app --reload
```

### Frontend seul

```bash
cd frontend
npm install
npm run dev
```

## 🌟 API Endpoints

### Chat
- `POST /api/chat` - Envoyer un message
- `GET /api/conversations/{session_id}` - Liste des conversations
- `GET /api/conversations/{session_id}/{conversation_id}` - Détails d'une conversation
- `DELETE /api/conversations/{session_id}/{conversation_id}` - Supprimer une conversation
- `POST /api/conversations/new` - Créer une nouvelle conversation

### Santé
- `GET /` - Info de l'application
- `GET /health` - Health check

## 🎨 Technologies Utilisées

### Backend
- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM pour PostgreSQL
- **Redis** - Cache et gestion des sessions
- **Anthropic SDK** - Intégration Claude AI
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI

### Frontend
- **Vue.js 3** - Framework JavaScript progressif
- **TypeScript** - Typage statique
- **Pinia** - Gestion d'état
- **Vite** - Build tool ultra-rapide
- **Tailwind CSS** - Framework CSS utility-first
- **Axios** - Client HTTP
- **Marked** - Parser Markdown

### Infrastructure
- **PostgreSQL** - Base de données relationnelle
- **Redis** - Cache en mémoire
- **Docker** - Containerisation
- **Docker Compose** - Orchestration

## 🔒 Sécurité

- Sessions utilisateur avec ID unique
- Variables d'environnement pour les secrets
- CORS configuré
- Validation des données avec Pydantic
- Soft delete des conversations

## 📈 Optimisations

- Cache Redis pour les conversations actives
- Pagination des messages
- Lazy loading des conversations
- Debouncing des inputs
- Compression des réponses API

## 🐛 Debugging

Logs Docker :
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

Accès aux conteneurs :
```bash
docker exec -it synapsechat-backend bash
docker exec -it synapsechat-frontend sh
```

## 🚀 Déploiement en Production

### Modifications recommandées

1. **Backend** :
   - Changer `SECRET_KEY` avec une valeur forte
   - Désactiver `DEBUG=False`
   - Configurer un vrai serveur SMTP
   - Utiliser PostgreSQL managé (AWS RDS, etc.)
   - Configurer Redis managé

2. **Frontend** :
   - Build de production : `npm run build`
   - Servir avec Nginx
   - Configurer CDN pour les assets

3. **Infrastructure** :
   - Utiliser un reverse proxy (Nginx, Traefik)
   - Configurer HTTPS avec Let's Encrypt
   - Mettre en place un système de monitoring
   - Configurer des backups automatiques

## 📝 License

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

## 📧 Support

Pour toute question : support@votre-domaine.com

---

Développé avec ❤️ en utilisant Claude AI
