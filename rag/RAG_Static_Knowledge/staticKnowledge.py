from common import VectorDataStore
#Image to text libraries
import pytesseract
from PIL import Image
#PDF to text library
from PyPDF2 import PdfReader
import os
import json
#from vectorDataStore import VectorDataStore
    
class StaticKnowledge:
    def __init__(self):
        # Reference to persistent data store
        self.vectorData = VectorDataStore()

    def _load_image(self, file_path):
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text

    def _load_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _load_txt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
        
    def _processFile(self, path):
        if path.lower().endswith(".pdf"):
            return self._load_pdf(path)
        elif path.lower().endswith((".png", ".jpg", ".jpeg")):
            return self._load_image(path)
        elif path.lower().endswith(".txt"):
            return self._load_txt(path)
    
    def load(self, data_dir):
        docs_to_add = []

        for file in os.listdir(data_dir):
            path = os.path.join(data_dir, file)
            if not os.path.isfile(path):
                continue
            
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".pdf", ".txt")):
                print(f"📄 Processing file: {file}")
                fileContent = self._processFile(path)
                # 1 Entire story in single chunk
                #docs_to_add += fileContent
                # 2 Split the document to small chunks
                documents = fileContent.splitlines()
                docs_to_add += documents
                print(f"documents count:: {len(docs_to_add)}")

        if docs_to_add:
            self.vectorData.add_documents(docs_to_add)
        else:
            print("✅ No new changes detected.")
    
    def retrieve(self, query, k=0):
        return self.vectorData.retrieve(query, k)