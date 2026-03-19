#!/bin/bash

echo "🚀 Démarrage de Synapse Chat..."
echo ""

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer depuis https://docker.com"
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Le fichier .env n'existe pas."
    echo "📝 Création du fichier .env..."
    cat > .env << EOF
# Clé API Anthropic (obligatoire)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Clé secrète pour les sessions (changez en production)
SECRET_KEY=your-super-secret-key-change-this-in-production
EOF
    echo "✅ Fichier .env créé. Veuillez éditer ce fichier avec votre clé API Anthropic."
    echo ""
    echo "Pour obtenir une clé API Anthropic :"
    echo "1. Visitez https://console.anthropic.com/"
    echo "2. Créez un compte ou connectez-vous"
    echo "3. Générez une clé API"
    echo "4. Copiez la clé dans le fichier .env"
    echo ""
    read -p "Appuyez sur Entrée une fois que vous avez configuré le fichier .env..."
fi

# Vérifier que la clé API est configurée
if grep -q "your_anthropic_api_key_here" .env; then
    echo "⚠️  ATTENTION : Vous devez configurer votre clé API Anthropic dans le fichier .env"
    echo "Éditez le fichier .env et remplacez 'your_anthropic_api_key_here' par votre vraie clé."
    exit 1
fi

echo "🐳 Lancement des conteneurs Docker..."
docker-compose up --build -d

echo ""
echo "⏳ Attente du démarrage des services..."
sleep 10

echo ""
echo "✅ Synapse Chat est maintenant en cours d'exécution !"
echo ""
echo "📍 Accès à l'application :"
echo "   Frontend : http://localhost:5173"
echo "   Backend API : http://localhost:8000"
echo "   Documentation API : http://localhost:8000/docs"
echo ""
echo "📋 Commandes utiles :"
echo "   Voir les logs : docker-compose logs -f"
echo "   Arrêter : docker-compose down"
echo "   Redémarrer : docker-compose restart"
echo ""
echo "🎉 Bon chat !"
