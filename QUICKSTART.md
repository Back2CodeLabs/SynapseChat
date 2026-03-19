# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Obtenir une clé API Anthropic

1. Visitez [https://console.anthropic.com/](https://console.anthropic.com/)
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Cliquez sur "Create Key"
5. Copiez votre clé API

### 2️⃣ Configurer le projet

Éditez le fichier `.env` :

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxx  # Collez votre clé ici
SECRET_KEY=votre-cle-secrete-aleatoire
```

### 3️⃣ Lancer l'application

**Option A : Avec le script (Linux/Mac)**
```bash
./start.sh
```

**Option B : Manuellement**
```bash
docker-compose up --build
```

## 🎯 Première utilisation

1. Ouvrez votre navigateur sur [http://localhost:5173](http://localhost:5173)
2. Cliquez sur "Nouvelle conversation"
3. Tapez votre message et appuyez sur Entrée
4. L'assistant Claude vous répondra !

## ⌨️ Raccourcis clavier

- `Entrée` : Envoyer le message
- `Shift + Entrée` : Nouvelle ligne dans le message

## 🔧 Commandes utiles

### Voir les logs
```bash
docker-compose logs -f
docker-compose logs -f backend    # Logs du backend uniquement
docker-compose logs -f frontend   # Logs du frontend uniquement
```

### Arrêter l'application
```bash
docker-compose down
```

### Redémarrer un service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Reconstruire les images
```bash
docker-compose up --build
```

### Supprimer les données (reset complet)
```bash
docker-compose down -v
```

## 🐛 Problèmes courants

### "ANTHROPIC_API_KEY not found"
➡️ Vérifiez que votre clé API est correctement configurée dans `.env`

### "Port 5173 already in use"
➡️ Un autre processus utilise le port. Arrêtez-le ou changez le port dans `docker-compose.yml`

### "Connection refused"
➡️ Attendez quelques secondes que tous les services démarrent
➡️ Vérifiez les logs : `docker-compose logs`

### Les messages ne s'envoient pas
➡️ Vérifiez que le backend est démarré : `curl http://localhost:8000/health`
➡️ Vérifiez votre clé API Anthropic

## 📊 Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Vue.js    │─────▶│   FastAPI   │─────▶│  Claude AI  │
│  Frontend   │◀─────│   Backend   │◀─────│   (API)     │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                ┌────▼────┐   ┌───▼────┐
                │PostgreSQL│   │ Redis  │
                └─────────┘   └────────┘
```

## 🎨 Personnalisation

### Changer le modèle Claude
Éditez `backend/claude_service.py` ligne 9 :
```python
self.model = "claude-sonnet-4-20250514"  # Changez ici
```

Modèles disponibles :
- `claude-opus-4-20250514` - Le plus puissant
- `claude-sonnet-4-20250514` - Équilibré (recommandé)
- `claude-haiku-4-20250514` - Le plus rapide

### Changer les couleurs
Éditez `frontend/tailwind.config.js` pour personnaliser les couleurs

### Modifier le prompt système
Éditez `backend/claude_service.py` lignes 23-26

## 📖 Ressources

- [Documentation Claude](https://docs.anthropic.com/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Vue.js](https://vuejs.org/)
- [Documentation Tailwind CSS](https://tailwindcss.com/)

## 💡 Astuces

1. **Sauvegardez vos conversations** : Elles sont stockées dans PostgreSQL
2. **Utilisez le contexte** : L'assistant se souvient de toute la conversation
3. **Formatez avec Markdown** : Les réponses supportent le Markdown
4. **Conversations multiples** : Créez autant de conversations que vous voulez

Bon développement ! 🚀
