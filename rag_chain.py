# rag_chain.py

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

PERSIST_DIR = "chroma_db"


def get_rag_chain():
    # 1) Vector store + retriever
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    # 2) LLM
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.1,
    )

    # 3) Prompt + document chain
    system_prompt = (
        "You are a helpful customer support assistant. "
        "Use ONLY the provided documentation context to answer the question. "
        "If the answer is not in the docs, say you don't know.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Turn docs + prompt into an LLM chain
    doc_chain = create_stuff_documents_chain(llm, prompt)

    # 4) Retrieval chain (RAG pipeline)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    return rag_chain
