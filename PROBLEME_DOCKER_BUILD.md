# 🔧 Résolution du problème Docker Build

## Problème rencontré
```
failed to receive status: rpc error: code = Unavailable desc = error reading from server: EOF
```

Ce problème arrive généralement quand :
- Docker manque de mémoire
- Docker manque d'espace disque
- Timeout lors du téléchargement des images
- Problème de connexion réseau

## 🚀 Solutions (dans l'ordre)

---

## Solution 1 : Augmenter les ressources Docker (RECOMMANDÉ)

### Windows - Docker Desktop

1. **Ouvrir Docker Desktop**
2. **Cliquer sur l'icône ⚙️ (Settings)**
3. **Aller dans "Resources"**
4. **Augmenter les valeurs** :
   - **Memory (RAM)** : Minimum 4 GB, recommandé 6-8 GB
   - **CPU** : Minimum 2, recommandé 4
   - **Disk image size** : Minimum 20 GB

5. **Cliquer sur "Apply & Restart"**
6. **Attendre que Docker redémarre**
7. **Relancer** : `docker-compose up -d`

---

## Solution 2 : Build séparé des images

Au lieu de tout builder en même temps, buildez séparément :

### Étape 1 : Backend uniquement
```powershell
cd backend
docker build -t synapsechat-backend .
```

Attendez que ça finisse (peut prendre 5-10 minutes).

### Étape 2 : Frontend uniquement
```powershell
cd ..\frontend
docker build -t synapsechat-frontend .
```

### Étape 3 : Modifier docker-compose.yml

Éditez `docker-compose.yml`, remplacez les sections `build:` par :

```yaml
  backend:
    image: synapsechat-backend
    # Supprimer les lignes build:
    container_name: synapsechat-backend
    ...

  frontend:
    image: synapsechat-frontend
    # Supprimer les lignes build:
    container_name: synapsechat-frontend
    ...
```

### Étape 4 : Lancer
```powershell
cd ..
docker-compose up -d
```

---

## Solution 3 : Nettoyer Docker et recommencer

Docker peut avoir des caches corrompus.

```powershell
# Arrêter tout
docker-compose down

# Nettoyer les images non utilisées
docker system prune -a --volumes

# Répondre "y" (yes) à la question

# Relancer
docker-compose up -d --build
```

⚠️ **Attention** : Cela supprime TOUTES les images Docker non utilisées sur votre système !

---

## Solution 4 : Build sans cache

Forcer la reconstruction complète :

```powershell
docker-compose build --no-cache
docker-compose up -d
```

---

## Solution 5 : Vérifier l'espace disque

Docker a besoin d'espace pour créer les images.

```powershell
# Vérifier l'espace disponible
docker system df

# Si Docker utilise trop d'espace, nettoyer :
docker system prune
```

Assurez-vous d'avoir **au moins 5-10 GB d'espace libre**.

---

## Solution 6 : Augmenter les timeouts

Si votre connexion Internet est lente :

### Méthode A : Variables d'environnement

```powershell
$env:COMPOSE_HTTP_TIMEOUT="300"
$env:DOCKER_CLIENT_TIMEOUT="300"
docker-compose up -d
```

### Méthode B : Modifier docker-compose.yml

Ajoutez au début du fichier :
```yaml
version: '3.8'

x-build-args: &build-args
  - DOCKER_BUILDKIT=1
  - BUILDKIT_PROGRESS=plain
```

---

## Solution 7 : Installation manuelle (SANS DOCKER)

Si Docker continue à poser problème, installez manuellement :

### Prérequis
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7

### Backend

```powershell
cd backend

# Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer .env
copy .env.example .env
notepad .env
# Modifier OLLAMA_BASE_URL=http://localhost:11434

# Lancer
uvicorn app.main:app --reload
```

### Frontend (nouveau terminal)

```powershell
cd frontend

# Installer les dépendances
npm install

# Copier et configurer .env
copy .env.example .env

# Lancer
npm run dev
```

### Services requis

Vous devrez installer et démarrer :
- **PostgreSQL** : https://www.postgresql.org/download/windows/
- **Redis** : https://github.com/microsoftarchive/redis/releases (ou utiliser WSL)

---

## 🔍 Diagnostics

### Vérifier les logs Docker

```powershell
# Logs généraux
docker-compose logs

# Logs backend uniquement
docker-compose logs backend

# Logs frontend uniquement
docker-compose logs frontend
```

### Vérifier l'état de Docker

```powershell
# État de Docker Desktop
docker version

# Ressources utilisées
docker stats

# Espace disque
docker system df
```

### Vérifier que Ollama est accessible

```powershell
# Test depuis Windows
curl http://localhost:11434/api/tags

# Ou dans le navigateur
# http://localhost:11434
```

---

## ⚡ Solution Rapide (À ESSAYER EN PREMIER)

1. **Augmenter la RAM de Docker à 6 GB**
2. **Redémarrer Docker Desktop**
3. **Nettoyer** :
   ```powershell
   docker-compose down
   docker system prune
   ```
4. **Relancer** :
   ```powershell
   docker-compose up -d
   ```

---

## 🆘 Si rien ne fonctionne

Deux options :

### Option A : Build pré-fait
Je peux vous fournir des images Docker pré-construites si vous le souhaitez.

### Option B : Installation manuelle
Suivez la **Solution 7** ci-dessus pour une installation sans Docker.

---

## 📞 Informations utiles pour le support

Si vous avez besoin d'aide, collectez ces informations :

```powershell
# Version Docker
docker version

# Info système Docker
docker info

# Espace disponible
docker system df

# Logs d'erreur complets
docker-compose logs > logs.txt
```

Envoyez-moi le contenu de `logs.txt` et les sorties des commandes ci-dessus.
