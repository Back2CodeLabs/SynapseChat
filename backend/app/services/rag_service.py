from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)


class RAGService:
    """Service pour le Retrieval Augmented Generation"""
    
    def __init__(self):
        # Créer le dossier de persistance
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
        
        # Initialiser ChromaDB
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Créer ou récupérer la collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Modèle d'embeddings
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        logger.info("RAG service initialized")
    
    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: Optional[Dict] = None,
        chunk_size: int = 500
    ) -> int:
        """Ajoute un document en le découpant en chunks"""
        chunks = self._split_text(text, chunk_size)
        
        if not chunks:
            return 0
        
        # Générer les embeddings
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        # Préparer les métadonnées
        chunk_metadata = []
        for i, chunk in enumerate(chunks):
            meta = {
                "document_id": document_id,
                "chunk_index": i,
                "chunk_text": chunk[:200]  # Preview
            }
            if metadata:
                meta.update(metadata)
            chunk_metadata.append(meta)
        
        # IDs uniques pour chaque chunk
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Ajouter à ChromaDB
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=chunk_metadata
        )
        
        logger.info(f"Added {len(chunks)} chunks for document {document_id}")
        return len(chunks)
    
    def search(
        self,
        query: str,
        n_results: int = None,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """Recherche les chunks les plus pertinents"""
        if n_results is None:
            n_results = settings.MAX_CHUNKS_TO_RETRIEVE
        
        # Générer l'embedding de la requête
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Préparer le filtre utilisateur si nécessaire
        where_filter = {"user_id": user_id} if user_id else None
        
        # Rechercher dans ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        # Formater les résultats
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        
        return formatted_results
    
    def delete_document(self, document_id: str):
        """Supprime tous les chunks d'un document"""
        # Récupérer tous les IDs des chunks
        results = self.collection.get(
            where={"document_id": document_id}
        )
        
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            logger.info(f"Deleted document {document_id}")
    
    def get_context_for_query(self, query: str, user_id: Optional[str] = None) -> str:
        """Récupère le contexte pertinent pour une requête"""
        results = self.search(query, user_id=user_id)
        
        if not results:
            return ""
        
        # Construire le contexte
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Source {i}]: {result['text']}")
        
        return "\n\n".join(context_parts)
    
    def _split_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Découpe un texte en chunks avec overlap"""
        if not text:
            return []
        
        overlap = chunk_size // 4  # 25% overlap
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Essayer de couper à une phrase complète
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                last_break = max(last_period, last_newline)
                
                if last_break > chunk_size // 2:
                    chunk = chunk[:last_break + 1]
                    end = start + last_break + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Supprimer les chunks vides


# Instance globale
rag_service = RAGService() if settings.ENABLE_RAG else None
