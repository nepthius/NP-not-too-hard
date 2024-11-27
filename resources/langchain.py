from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from transformers import pipeline
from pymongo import MongoClient

#hugging face
llm_pipeline = pipeline(
    "text-generation",
    model="meta-llama/Llama-3b",
    tokenizer="meta-llama/Llama-3b",
    device=0
)

#add the db connect
llm = HuggingFacePipeline(pipeline=llm_pipeline)
client = MongoClient("mongodb://localhost:27017/")
db = client["langchain_llama"]
collection = db["results"]

#sample regulatory questions
template = "Answer the following regulatory question in detail: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(llm=llm, prompt=prompt)

#storage
def process_question_and_store(question):

    answer = llm_chain.run(question)
    collection.insert_one({"question": question, "answer": answer})
    return answer

#makes sure results are predicted
def analyze_results():
    results = list(collection.find())
    for result in results:
        print("Question:", result["question"])
        print("Answer:", result["answer"])
        print("---")

#defining the model        
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(
    collection_name="regulatory_docs",
    embedding_function=embedding_model
)

#adding the data
def add_document_to_store(doc_path):
    loader = TextLoader(doc_path)
    documents = loader.load()
    vector_store.add_documents(documents)

#grabbing it
def retrieve_similar_documents(query):
    retriever = vector_store.as_retriever()
    results = retriever.get_relevant_documents(query)
    return results