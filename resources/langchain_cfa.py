from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

#grab cfa textbooks
def load_textbooks(file_paths):
    documents = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())
    return documents

#grab all the different cfa books
file_paths = ["cfa_book1.pdf", "cfa_book2.pdf", "cfa_book3.pdf"]
documents = load_textbooks(file_paths)

#split up text using langchain
def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)
text_chunks = split_documents(documents)

#store into vector db
def create_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings() 
    vector_store = FAISS.from_documents(text_chunks, embeddings)
    return vector_store
vector_store = create_vector_store(text_chunks)
retriever = vector_store.as_retriever()

#prompt template
template = """
(This context is used for the question that follows: Sammy Sneadle, CFA, is the founder and portfolio manager of the Everglades Fund. In its first year, the fund generated a return of 30 percent. Building on the fund’s performance, Sneadle created new marketing materials that showed the fund’s gross 1-year return, as well as the 3 and 5-year returns, which he calculated by using back-testedperformance information. As the marketing material is used only for presentations to institutional clients, Sneadle does not mention the inclusion of back-tested data. According to the Standards of Practice Handbook, how did Sneadle violate CFA Institute Standards of Professional Conduct?). 
Please answer the following question with only the letter and associated description of the correct answer choice: 
A. He did not disclose the use of back-tested data, B. He failed to deduct all fees and expenses before calculating the fund’s track record, C. The marketing materials only include the Everglades Fund’s performance and are not a weighted composite of similar portfolios. Answer: A. He did not disclose the use of back-tested data.
"""
prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question_and_choices"]
)
llm = OpenAI(model="gpt-4", temperature=0)
qa_chain = RetrievalQA(
    llm=llm, 
    retriever=retriever, 
    return_source_documents=False, 
    prompt=prompt
)

#example query
def run_query(question_and_choices):
    """
    Function to retrieve context and run the query.
    """
    response = qa_chain.run({"question_and_choices": question_and_choices})
    return response

question_and_choices = """
What is the primary benefit of financial regulations? 
A) Market integrity 
B) Investor confidence 
C) Legal protection 
D) Tax compliance
"""

#running it
response = run_query(question_and_choices)
print("Answer:", response)
