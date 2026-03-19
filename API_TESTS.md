# Tests API - SynapseChat

## Tester le health check

```bash
curl http://localhost:8000/health
```

Réponse attendue :
```json
{"status": "healthy"}
```

## Tester l'envoi d'un message

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour, qui es-tu ?",
    "session_id": "test-session-123"
  }'
```

## Récupérer les conversations

```bash
curl http://localhost:8000/api/conversations/test-session-123
```

## Récupérer une conversation spécifique

```bash
curl http://localhost:8000/api/conversations/test-session-123/1
```

## Créer une nouvelle conversation

```bash
curl -X POST "http://localhost:8000/api/conversations/new?session_id=test-session-123"
```

## Supprimer une conversation

```bash
curl -X DELETE http://localhost:8000/api/conversations/test-session-123/1
```

## Tester avec Python

```python
import requests

# Envoyer un message
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Explique-moi ce qu'est FastAPI",
        "session_id": "python-test"
    }
)

print(response.json())
```

## Tester avec JavaScript

```javascript
// Envoyer un message
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Qu\'est-ce que Vue.js ?',
    session_id: 'js-test'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Documentation interactive

Visitez http://localhost:8000/docs pour accéder à la documentation Swagger interactive de l'API.
