import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, model_name="llama3-70b-8192"):
        print(f"📥 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def embed_text(self, texts):
        return self.model.encode(texts, convert_to_tensor=False, normalize_embeddings=True)

    def build_index(self, documents: list[str]):
        print("🧠 Building FAISS index...")
        self.documents = documents
        embeddings = self.embed_text(documents)
        embeddings = np.array(embeddings).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query: str, top_k=3):
        if self.index is None:
            raise ValueError("❌ Index not built yet.")
        query_vec = np.array(self.embed_text([query])).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = [self.documents[i] for i in indices[0]]
        return results

    def save(self, path="vectorstore/"):
        os.makedirs(path, exist_ok=True)
        print("💾 Saving vectorstore to disk...")
        faiss.write_index(self.index, os.path.join(path, "faiss.index"))
        with open(os.path.join(path, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)

    def load(self, path="vectorstore/"):
        print("📂 Loading vectorstore from disk...")
        faiss_path = os.path.join(path, "faiss.index")
        docs_path = os.path.join(path, "documents.pkl")

        if not os.path.exists(faiss_path):
            raise FileNotFoundError(f"FAISS index not found at {faiss_path}")
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"Documents file not found at {docs_path}")

        self.index = faiss.read_index(faiss_path)
        with open(docs_path, "rb") as f:
            self.documents = pickle.load(f)


