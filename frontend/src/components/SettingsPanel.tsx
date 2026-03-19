import React, { useState, useEffect } from 'react';
import { X, Check, AlertCircle } from 'lucide-react';
import { useChatStore } from '../store/chatStore';
import { chatApi } from '../services/api';
import type { HealthStatus } from '../types';

interface SettingsPanelProps {
  onClose: () => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ onClose }) => {
  const { config, updateConfig } = useChatStore();
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [ollamaModels, setOllamaModels] = useState<string[]>([]);
  const [loadingModels, setLoadingModels] = useState(false);

  useEffect(() => {
    loadHealth();
    if (config.aiProvider === 'ollama') {
      loadOllamaModels();
    }
  }, [config.aiProvider]);

  const loadHealth = async () => {
    try {
      const status = await chatApi.getHealth();
      setHealth(status);
    } catch (error) {
      console.error('Error loading health:', error);
    }
  };

  const loadOllamaModels = async () => {
    setLoadingModels(true);
    try {
      const models = await chatApi.getOllamaModels();
      if (models && models.length > 0) {
        setOllamaModels(models);
      } else {
        // Modèles par défaut si aucun n'est retourné
        setOllamaModels(['mistral', 'deepseek-coder:6.7b', 'qwen2.5-coder:7b', 'codestral']);
      }
    } catch (error) {
      console.error('Error loading Ollama models:', error);
      // Modèles par défaut en cas d'erreur
      setOllamaModels(['mistral', 'deepseek-coder:6.7b', 'qwen2.5-coder:7b', 'codestral']);
    } finally {
      setLoadingModels(false);
    }
  };

  const handleProviderChange = async (provider: 'claude' | 'openai' | 'ollama') => {
    setLoading(true);
    try {
      await chatApi.changeProvider(provider);
      updateConfig({ aiProvider: provider });
      await loadHealth();
      
      // Charger les modèles Ollama si on bascule vers Ollama
      if (provider === 'ollama') {
        await loadOllamaModels();
      }
    } catch (error) {
      console.error('Error changing provider:', error);
      alert('Erreur lors du changement de provider');
    } finally {
      setLoading(false);
    }
  };

  const handleOllamaModelChange = async (model: string) => {
    setLoading(true);
    try {
      await chatApi.changeOllamaModel(model);
      updateConfig({ ollamaModel: model });
      await loadHealth();
    } catch (error) {
      console.error('Error changing Ollama model:', error);
      alert('Erreur lors du changement de modèle Ollama');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Paramètres</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Health Status */}
          {health && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-semibold mb-3">État du système</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="flex items-center gap-2">
                  {health.ai_available ? (
                    <Check size={16} className="text-green-600" />
                  ) : (
                    <AlertCircle size={16} className="text-red-600" />
                  )}
                  <span>IA: {health.ai_available ? 'Disponible' : 'Indisponible'}</span>
                </div>
                <div className="flex items-center gap-2">
                  {health.database_connected ? (
                    <Check size={16} className="text-green-600" />
                  ) : (
                    <AlertCircle size={16} className="text-red-600" />
                  )}
                  <span>Base de données: {health.database_connected ? 'Connectée' : 'Déconnectée'}</span>
                </div>
                <div className="col-span-2">
                  <span className="text-gray-600">Provider actuel: </span>
                  <span className="font-semibold">{health.ai_provider}</span>
                </div>
                <div className="col-span-2">
                  <span className="text-gray-600">RAG: </span>
                  <span className="font-semibold">{health.rag_enabled ? 'Activé' : 'Désactivé'}</span>
                </div>
              </div>
            </div>
          )}

          {/* Provider Selection */}
          <div>
            <h3 className="font-semibold mb-3">Provider IA</h3>
            <div className="space-y-2">
              {[
                { value: 'claude', label: 'Claude (Anthropic)', desc: 'API Cloud - Recommandé' },
                { value: 'openai', label: 'OpenAI (GPT-4)', desc: 'API Cloud' },
                { value: 'ollama', label: 'Ollama (Local)', desc: 'LLM local avec RAG' },
              ].map((provider) => (
                <label
                  key={provider.value}
                  className={`flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                    config.aiProvider === provider.value
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="provider"
                    value={provider.value}
                    checked={config.aiProvider === provider.value}
                    onChange={() => handleProviderChange(provider.value as any)}
                    className="mt-1"
                    disabled={loading}
                  />
                  <div>
                    <div className="font-medium">{provider.label}</div>
                    <div className="text-sm text-gray-600">{provider.desc}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Ollama Model Selection - Only visible when Ollama is selected */}
          {config.aiProvider === 'ollama' && (
            <div>
              <h3 className="font-semibold mb-3">Modèle Ollama</h3>
              <div className="space-y-2">
                {loadingModels ? (
                  <div className="flex items-center justify-center p-4 text-gray-500">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    <span className="ml-2">Chargement des modèles...</span>
                  </div>
                ) : ollamaModels.length > 0 ? (
                  ollamaModels.map((model) => (
                    <label
                      key={model}
                      className={`flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                        config.ollamaModel === model
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <input
                        type="radio"
                        name="ollama-model"
                        value={model}
                        checked={config.ollamaModel === model}
                        onChange={() => handleOllamaModelChange(model)}
                        className="mt-1"
                        disabled={loading}
                      />
                      <div className="flex-1">
                        <div className="font-medium">{model}</div>
                        <div className="text-sm text-gray-600">
                          {model === 'mistral' && '🌟 Modèle polyvalent - Excellent équilibre performance/qualité'}
                          {model.includes('deepseek-coder') && '💻 Spécialisé code - Excellent pour le développement'}
                          {model.includes('qwen2.5-coder') && '⚡ Codage rapide - Performances optimales'}
                          {model.includes('codestral') && '🚀 Code avancé - Mistral spécialisé développement'}
                          {!['mistral', 'deepseek-coder:6.7b', 'qwen2.5-coder:7b', 'codestral'].some(m => model.includes(m.split(':')[0])) && '🤖 Modèle Ollama'}
                        </div>
                      </div>
                    </label>
                  ))
                ) : (
                  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <p className="text-sm text-yellow-800">
                      Aucun modèle Ollama détecté. Assurez-vous qu'Ollama est démarré et que des modèles sont installés.
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* RAG Toggle */}
          <div>
            <h3 className="font-semibold mb-3">RAG (Retrieval Augmented Generation)</h3>
            <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-gray-300">
              <input
                type="checkbox"
                checked={config.enableRAG}
                onChange={(e) => updateConfig({ enableRAG: e.target.checked })}
              />
              <div>
                <div className="font-medium">Activer le RAG</div>
                <div className="text-sm text-gray-600">
                  Utilise les documents uploadés pour enrichir les réponses
                </div>
              </div>
            </label>
          </div>

          {/* Streaming Toggle */}
          <div>
            <h3 className="font-semibold mb-3">Mode de réponse</h3>
            <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-gray-300">
              <input
                type="checkbox"
                checked={config.enableStreaming}
                onChange={(e) => updateConfig({ enableStreaming: e.target.checked })}
              />
              <div>
                <div className="font-medium">Streaming activé</div>
                <div className="text-sm text-gray-600">
                  Affiche les réponses en temps réel (plus fluide)
                </div>
              </div>
            </label>
          </div>

          {/* User ID */}
          <div>
            <h3 className="font-semibold mb-3">Identifiant utilisateur</h3>
            <input
              type="text"
              value={config.userId}
              readOnly
              className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-600"
            />
            <p className="text-xs text-gray-500 mt-1">
              Cet identifiant est généré automatiquement et stocké localement
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;