#!/bin/bash

# Script pour configurer Ollama avec des modèles recommandés

echo "🦙 Configuration d'Ollama..."
echo ""

# Vérifier si Ollama est en cours d'exécution
if ! docker ps | grep -q synapsechat-ollama; then
    echo "❌ Le conteneur Ollama n'est pas démarré"
    echo "Démarrez-le avec: docker-compose --profile ollama up -d"
    exit 1
fi

echo "✅ Ollama est en cours d'exécution"
echo ""

# Proposer des modèles
echo "📦 Modèles recommandés:"
echo ""
echo "1) llama2 (7B) - Polyvalent, bon équilibre"
echo "2) mistral (7B) - Excellent pour le français"
echo "3) codellama (7B) - Spécialisé pour le code"
echo "4) neural-chat (7B) - Optimisé pour la conversation"
echo "5) llama2:13b - Plus performant mais plus lourd"
echo "6) tous les modèles ci-dessus"
echo ""

read -p "Quel(s) modèle(s) voulez-vous télécharger? (1-6): " choice

download_model() {
    model=$1
    echo ""
    echo "📥 Téléchargement de $model..."
    docker exec synapsechat-ollama ollama pull $model
    
    if [ $? -eq 0 ]; then
        echo "✅ $model téléchargé avec succès"
    else
        echo "❌ Erreur lors du téléchargement de $model"
    fi
}

case $choice in
    1)
        download_model "llama2"
        ;;
    2)
        download_model "mistral"
        ;;
    3)
        download_model "codellama"
        ;;
    4)
        download_model "neural-chat"
        ;;
    5)
        download_model "llama2:13b"
        ;;
    6)
        download_model "llama2"
        download_model "mistral"
        download_model "codellama"
        download_model "neural-chat"
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "📋 Modèles installés:"
docker exec synapsechat-ollama ollama list

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "💡 Pour utiliser un modèle spécifique, modifiez OLLAMA_MODEL dans backend/.env"
echo "   Par exemple: OLLAMA_MODEL=mistral"
echo ""
echo "🔄 N'oubliez pas de redémarrer le backend après modification:"
echo "   docker-compose restart backend"
