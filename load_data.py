from qdrant_client import QdrantClient, models
import json
from typing import List
import numpy as np
import os

client = QdrantClient(url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))

client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("prithivida/Splade_PP_en_v1")

if not client.collection_exists("startups"):
    client.create_collection(
        collection_name="startups",
        vectors_config=client.get_fastembed_vector_params(),
        sparse_vectors_config=client.get_fastembed_sparse_vector_params(),  
    )

def named_vectors(vectors: List[float], sparse_vectors: List[models.SparseVector]) -> dict:
    # make sure to use the same client object as previously
    # or `set_model_name` and `set_sparse_model_name` manually
    dense_vector_name = client.get_vector_field_name()
    sparse_vector_name = client.get_sparse_vector_field_name()  
    for vector, sparse_vector in zip(vectors, sparse_vectors):
        yield {
            dense_vector_name: vector,
            sparse_vector_name: models.SparseVector(**sparse_vector),
        } 

with open("startups_hybrid_search_processed_40k/dense_vectors.npy", "rb") as f:
    vectors = np.load(f)
    
with open("startups_hybrid_search_processed_40k/sparse_vectors.json", "r") as f:
    sparse_vectors = json.load(f)
    
with open("startups_hybrid_search_processed_40k/payload.json", "r",) as f:
    payload = json.load(f)

client.upload_collection(
    "startups", vectors=named_vectors(vectors, sparse_vectors), payload=payload
)