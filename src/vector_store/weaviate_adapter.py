# src/vector_store/weaviate_adapter.py

import weaviate
from sentence_transformers import SentenceTransformer
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class WeaviateAdapter:
    def __init__(self, weaviate_url="http://localhost:8080", model_name="llama3-70b-8192"):
        print(f"🔌 Connecting to Weaviate at {weaviate_url}")
        self.client = weaviate.Client(weaviate_url)
        self.model = SentenceTransformer(model_name)
        self.class_name = "CodeChunk"
        self._ensure_schema()

    def _ensure_schema(self):
        if not self.client.schema.contains({"class": self.class_name}):
            schema = {
                "classes": [
                    {
                        "class": self.class_name,
                        "description": "Code snippets and doc chunks",
                        "properties": [
                            {"name": "content", "dataType": ["text"]},
                            {"name": "source", "dataType": ["string"]}
                        ],
                        "vectorizer": "none"
                    }
                ]
            }
            self.client.schema.create(schema)
            print("✅ Schema created in Weaviate.")

    def add_documents(self, chunks: list[dict]):
        for chunk in chunks:
            vector = self.model.encode(chunk["content"]).tolist()
            self.client.data_object.create(
                data_object={
                    "content": chunk["content"],
                    "source": chunk["source"]
                },
                class_name=self.class_name,
                vector=vector
            )
        print(f"✅ Added {len(chunks)} documents to Weaviate.")

    def search(self, query: str, top_k=3) -> list[str]:
        query_vector = self.model.encode(query).tolist()
        result = self.client.query.get(self.class_name, ["content", "source"]) \
            .with_near_vector({"vector": query_vector}) \
            .with_limit(top_k) \
            .do()
        hits = result["data"]["Get"][self.class_name]
        return [f"{hit['source']}:\n{hit['content']}" for hit in hits]


# ✅ Wrapper used by orchestrator
def store_context_vector(context_data: dict):
    adapter = WeaviateAdapter()
    flattened = []

    for key, val in context_data.items():
        if isinstance(val, (str, int, float)):
            flattened.append({"content": f"{key}: {val}", "source": "context"})
        elif isinstance(val, list):
            for i, item in enumerate(val):
                flattened.append({"content": f"{key}[{i}]: {item}", "source": "context"})
        elif isinstance(val, dict):
            for subkey, subval in val.items():
                flattened.append({"content": f"{key}.{subkey}: {subval}", "source": "context"})

    adapter.add_documents(flattened)


