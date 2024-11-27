from qdrant_client import QdrantClient


class HybridSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
    def __init__(self, collection_name: str, url: str, api_key: str):
        self.collection_name = collection_name
        self.url = url
        self.api_key = api_key
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(url=self.url, api_key=self.api_key)
        self.qdrant_client.set_model(self.DENSE_MODEL)
        # comment this line to use dense vectors only
        self.qdrant_client.set_sparse_model(self.SPARSE_MODEL)

    def search(self, text: str, query_filter: str) -> list:
        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=query_filter,
            limit=5,
        )

        metadata = [hit.metadata for hit in search_result]
        return metadata