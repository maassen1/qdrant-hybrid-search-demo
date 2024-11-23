import os
import nest_asyncio
import qdrant_client
from dotenv import load_dotenv
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_parse import LlamaParse
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import PromptTemplate
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
from llama_index.core import Settings


'''
Purpose: load data from `data` directory into Qdrant collection titled `demo`
Precondition: Jina Embeddings, mixtral LLM, Qdrant client, and env variables all initialized
Postcondition: Data from `data` directory is loaded into Qdrant `demo` collection and ready to be queried
'''
def load_data(jina_embedding_model: JinaEmbedding, mixtral_llm: HuggingFaceInferenceAPI, client: qdrant_client.QdrantClient) -> VectorStoreIndex:
	nest_asyncio.apply()

	llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

	llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data([
	    "data/DJ68-00682F_0.0.pdf", 
	    "data/F500E_WF80F5E_03445F_EN.pdf", 
	    "data/O_ME4000R_ME19R7041FS_AA_EN.pdf"
	])

	Settings.embed_model = jina_embedding_model
	Settings.llm = mixtral_llm

	vector_store = QdrantVectorStore(
	    client=client, collection_name="demo", enable_hybrid=True, batch_size=20
	)
	Settings.chunk_size = 512

	storage_context = StorageContext.from_defaults(vector_store=vector_store)
	index = VectorStoreIndex.from_documents(
	    documents=llama_parse_documents, 
	    storage_context=storage_context
	)
	return index

def main():
	# load env file
	load_dotenv('./.env')

	# init Jina Embeddings
	jina_embedding_model = JinaEmbedding(
    model="jina-embeddings-v2-base-en",
    api_key=os.getenv("JINAAI_API_KEY"),
	)

	# init mixtral LLM on HuggingFace
	mixtral_llm = HuggingFaceInferenceAPI(
	    model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
	    token=os.getenv("HF_INFERENCE_API_KEY"),
	)

	# init Qdrant client
	client = qdrant_client.QdrantClient(url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))

	# load data from `data` directory to Qdrant collection titled `demo`
	print("Loading data directory to `demo` collection in Qdrant")
	index = load_data(jina_embedding_model, mixtral_llm, client)
	print("Completed loading data into `demo` Qdrant collection")

	# init promt 
	qa_prompt_tmpl = (
	    "Context information is below.\n"
	    "-------------------------------"
	    "{context_str}\n"
	    "-------------------------------"
	    "Given the context information and not prior knowledge,"
	    "answer the query. Please be concise, and complete.\n"
	    "If the context does not contain an answer to the query,"
	    "respond with \"I don't know!\"."
	    "Query: {query_str}\n"
	    "Answer: "
	)
	qa_prompt = PromptTemplate(qa_prompt_tmpl)


	Settings.embed_model = jina_embedding_model
	Settings.llm = mixtral_llm

	# retriever
	retriever = VectorIndexRetriever(
	    index=index,
	    similarity_top_k=2,
	    sparse_top_k=12,
	    vector_store_query_mode="hybrid"
	)

	# response synthesizer
	response_synthesizer = get_response_synthesizer(
	    llm=mixtral_llm,
	    text_qa_template=qa_prompt,
	    response_mode="compact",
	)

	# query engine
	query_engine = RetrieverQueryEngine(
	    retriever=retriever,
	    response_synthesizer=response_synthesizer,
	)


	# continuously promt user for questions until `exit` is typed
	while True:
		try:
			user_input = str(input("Please ask a question! To exit simply type `exit`: "))
			if user_input == "exit":
				break
		except:
			print("You did not enter a valid question, please try again.")
		result = query_engine.query(user_input)
		print(result.response)


if __name__ == "__main__":
	main()