import sys
import os

# ➕ Add the parent directory to sys.path so 'vector_store' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vector_store.faiss_index import VectorStore


class SemanticSearchEngine:
    def __init__(self, index_path="vectorstore/", model_name="llama3-70b-8192"):
        self.vectorstore = VectorStore(model_name=model_name)
        self.index_path = index_path
        self._load_vectorstore()

    def _load_vectorstore(self):
        try:
            self.vectorstore.load(self.index_path)
            print("✅ Vectorstore loaded successfully.")
        except Exception as e:
            print(f"❌ Failed to load vectorstore: {e}")

    def search(self, query: str, top_k: int = 3) -> list[str]:
        print(f"🔍 Semantic search for: {query}")
        return self.vectorstore.search(query, top_k=top_k)


if __name__ == "__main__":
    engine = SemanticSearchEngine()

    while True:
        q = input("\n🧠 Enter your search query (or type 'exit'): ")
        if q.strip().lower() == "exit":
            break

        try:
            results = engine.search(q)
            print("\n📌 Top Matches:")
            for r in results:
                print("—" * 40)
                print(r)
        except Exception as e:
            print(f"❌ Search failed: {e}")


