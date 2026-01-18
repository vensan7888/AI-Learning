import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os
class VectorDataStore:
    def __init__(self):
        # -----------------------------
        # Embedding model (for RAG)
        # -----------------------------
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # -----------------------------
        # Vector DB (FAISS)
        # -----------------------------
        dimension = 384  # embedding size for all-MiniLM-L6-v2
        # Indexing is needed to perform the similarity-search
        self.index = faiss.IndexFlatL2(dimension)
        # Store original texts in same order
        self.docStore = []
        
        # Persitent vector store configuration
        self.indexPath = "faiss_index.bin"
        self.mappingPath = "doc_mapping.pkl"
        
        # Load "Documents from Persistent Storage"
        # UnComment below to test Persistence
        self._loadDocuments()

    # -----------------------------
    # Add documents to FAISS
    # -----------------------------
    def add_documents(self, docs):
        embeddings = self.embedder.encode(docs, convert_to_numpy=True)
        self.index.add(embeddings)
        self.docStore.append(docs)
        
        # Add "Documents to Persistent Storage
        # UnComment below to test Persistence
        self._saveDocuments(docs, embeddings)
        
    # -----------------------------
    # Retrieve top-k docs
    # -----------------------------
    def retrieve(self, query, k=0):
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        
        if k == 0:
            # total exact vectors/docs related
            k = self.index.ntotal

        distances, indices = self.index.search(q_emb, k)
        if len(self.docStore) == 0:
            return ""
        return [self.docStore[i] for i in indices[0] if i < len(self.docStore)]

    
    # ---- FAISS Persitent Helpers ----
    # Note: We can only control the duplicate document insertions by 
    # a specific paramter coming from host systems, like document name, date.
    # Store them in a traditional database & check with those parameters before handing them over to VectorDataStore
    
    def _loadDocuments(self):
        savedIndex, docs = self._loadFaiss()
        if savedIndex is None:
            return

        self.index = savedIndex
        self.docStore = docs
    
    def _saveDocuments(self, newDocs, embeddings):
        self._writeFaiss(newDocs, embeddings)

    def _writeFaiss(self, docs, embeddings):
        faiss.write_index(self.index, self.indexPath)
        with open(self.mappingPath, "wb") as f:
            pickle.dump(docs, f)
        print(f"✅ FAISS index built with {len(docs)} docs")

    def _loadFaiss(self):
        if not os.path.exists(self.mappingPath):
            print("\n ***** Mapping File doesn't exist *****\n")
            return None, []
        if not os.path.exists(self.indexPath):
            print("\n ***** Index File doesn't exist *****\n")
            return None, []
        index = faiss.read_index(self.indexPath)
        with open(self.mappingPath, "rb") as f:
            docs = pickle.load(f)
        return index, docs