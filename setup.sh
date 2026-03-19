#!/bin/bash

# Script de setup automatique pour le chatbot

echo "🚀 Configuration de Synapse Chat..."
echo ""

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Vérifier les prérequis
echo "📋 Vérification des prérequis..."

if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé"
    echo "   Installez Docker depuis: https://docs.docker.com/get-docker/"
    exit 1
fi
print_success "Docker trouvé"

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé"
    echo "   Installez Docker Compose depuis: https://docs.docker.com/compose/install/"
    exit 1
fi
print_success "Docker Compose trouvé"

echo ""

# Créer les fichiers .env s'ils n'existent pas
echo "📝 Configuration des fichiers d'environnement..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    print_success "Fichier backend/.env créé"
    print_info "⚠️  N'oubliez pas d'ajouter vos clés API dans backend/.env"
else
    print_info "backend/.env existe déjà"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    print_success "Fichier frontend/.env créé"
else
    print_info "frontend/.env existe déjà"
fi

echo ""

# Demander le provider IA
echo "🤖 Configuration du provider IA..."
echo "Quel provider souhaitez-vous utiliser?"
echo "1) Claude (Anthropic) - Recommandé"
echo "2) OpenAI (GPT-4)"
echo "3) Ollama (Local - nécessite GPU)"
read -p "Votre choix (1-3): " provider_choice

case $provider_choice in
    1)
        sed -i 's/AI_PROVIDER=.*/AI_PROVIDER=claude/' backend/.env
        print_success "Provider configuré: Claude"
        echo ""
        read -p "Entrez votre clé API Anthropic (ou appuyez sur Entrée pour la configurer plus tard): " api_key
        if [ ! -z "$api_key" ]; then
            sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$api_key/" backend/.env
            print_success "Clé API configurée"
        else
            print_info "N'oubliez pas de configurer ANTHROPIC_API_KEY dans backend/.env"
        fi
        ;;
    2)
        sed -i 's/AI_PROVIDER=.*/AI_PROVIDER=openai/' backend/.env
        print_success "Provider configuré: OpenAI"
        echo ""
        read -p "Entrez votre clé API OpenAI (ou appuyez sur Entrée pour la configurer plus tard): " api_key
        if [ ! -z "$api_key" ]; then
            sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" backend/.env
            print_success "Clé API configurée"
        else
            print_info "N'oubliez pas de configurer OPENAI_API_KEY dans backend/.env"
        fi
        ;;
    3)
        sed -i 's/AI_PROVIDER=.*/AI_PROVIDER=ollama/' backend/.env
        print_success "Provider configuré: Ollama"
        print_info "Ollama sera démarré avec Docker Compose"
        OLLAMA_PROFILE="--profile ollama"
        ;;
    *)
        print_error "Choix invalide"
        exit 1
        ;;
esac

echo ""

# Demander si on active le RAG
read -p "Activer le RAG (Retrieval Augmented Generation)? (o/n): " enable_rag
if [ "$enable_rag" = "o" ] || [ "$enable_rag" = "O" ]; then
    sed -i 's/ENABLE_RAG=.*/ENABLE_RAG=True/' backend/.env
    print_success "RAG activé"
else
    sed -i 's/ENABLE_RAG=.*/ENABLE_RAG=False/' backend/.env
    print_info "RAG désactivé"
fi

echo ""

# Démarrer les services
echo "🐳 Démarrage des services Docker..."
echo ""

docker-compose $OLLAMA_PROFILE up -d

if [ $? -eq 0 ]; then
    print_success "Services démarrés avec succès!"
    echo ""
    echo "📊 État des services:"
    docker-compose ps
    echo ""
    echo "✨ Configuration terminée!"
    echo ""
    echo "🌐 Accès à l'application:"
    echo "   - Frontend:  http://localhost:3000"
    echo "   - Backend:   http://localhost:8000"
    echo "   - API Docs:  http://localhost:8000/docs"
    echo ""
    
    if [ ! -z "$OLLAMA_PROFILE" ]; then
        echo "📥 Pour télécharger un modèle Ollama:"
        echo "   docker exec -it synapsechat-ollama ollama pull llama2"
        echo ""
    fi
    
    echo "📝 Commandes utiles:"
    echo "   - Voir les logs:        docker-compose logs -f"
    echo "   - Arrêter:              docker-compose down"
    echo "   - Redémarrer:           docker-compose restart"
    echo "   - Consulter la santé:   curl http://localhost:8000/api/health"
    echo ""
    print_info "Consultez GUIDE_DEMARRAGE.md pour plus d'informations"
else
    print_error "Erreur lors du démarrage des services"
    echo "Consultez les logs avec: docker-compose logs"
    exit 1
fi
