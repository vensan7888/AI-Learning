from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
import json

class FaissHelper:

    def __init__(self, manifestPath, faissVectorDbPath, documentsDir):
        self.manifestPath = manifestPath
        self.faissVectorDbPath = faissVectorDbPath
        self.documentsDir = documentsDir
        

    def loadFaiss(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        # Load New docs & updated manifest
        newDocs, manifest = self._processDocuments(self.documentsDir)
        if os.path.exists(self.faissVectorDbPath):
            print("\n Exisiting FAISS DB\n")
            # Load FAISS index from disk
            faiss_loaded = FAISS.load_local(
                self.faissVectorDbPath,
                embeddings,
                allow_dangerous_deserialization=True
            )
            if (not newDocs == None) and len(newDocs) > 0:
                faiss_loaded.add_documents(newDocs)
                faiss_loaded.save_local(self.faissVectorDbPath)
                self.saveManifest(manifest, self.manifestPath)
        else:
            print("\n No FAISS DB\n")
            if (not newDocs == None) and len(newDocs) > 0:
                faiss_loaded = FAISS.from_documents(newDocs, embeddings)
                faiss_loaded.save_local(self.faissVectorDbPath)
                self.saveManifest(manifest, self.manifestPath)

        if faiss_loaded == None:
            texts = ["this is sample text", "you need to provide documents"]
            # Default Empty vector data store
            faiss_loaded = FAISS.from_texts(texts, embeddings)

        return faiss_loaded

    def save(self, message: str, faissDb: FAISS):
        faissDb.add_texts([message])
        faissDb.save_local(self.faissVectorDbPath)
    
    def _processDocuments(self, data_dir):
        docs_to_add = []
        manifest = self.loadManifest(self.manifestPath)
        updated_manifest = manifest.copy()

        for file in os.listdir(data_dir):
            path = os.path.join(data_dir, file)
            if not os.path.isfile(path):
                continue
            
            # last modified time
            mtime = os.path.getmtime(path)  

            # Chunk the data
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=200,
                chunk_overlap=30
            )
            
            # Check if file is new or changed
            if file not in manifest or manifest[file] < mtime:
                print(f"Processing new/updated file: {file}")
                if file.lower().endswith(".pdf"):
                    loader = PyPDFLoader(path)
                    docs = loader.load()
                elif file.lower().endswith(".txt"):
                    loader = TextLoader(path)
                    docs = loader.load()
                
                if (not docs == None) or (len(docs) > 0):
                    chunks = splitter.split_documents(docs)
                    docs_to_add += chunks
                    # Update manifest with latest mtime
                    updated_manifest[file] = mtime

        if docs_to_add:
            return docs_to_add, updated_manifest
        else:
            print("✅ No new changes detected.")
            return None, None
        

    def loadManifest(self, manifest_path):
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                return json.load(f)
        return {}

    def saveManifest(self, manifest, manifest_path):
        with open(manifest_path, "w") as f:
            json.dump(manifest, f)