from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.embeddings import DashScopeEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter


def qa_agent(openai_api_model, openai_api_key, memory, uploaded_file, question):
    if "qwen" in openai_api_model:
        model = ChatTongyi(model=openai_api_model, dashscope_api_key=openai_api_key)
    else:
        model = ChatOpenAI(model=openai_api_model, openai_api_key=openai_api_key)

    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", "。", "！", "？", "，", "、", ""]
    )
    texts = text_splitter.split_documents(docs)
    if "qwen" in openai_api_model:
        embeddings_model = DashScopeEmbeddings(model="text-embedding-v1", dashscope_api_key=openai_api_key)
    else:
        embeddings_model = OpenAIEmbeddings()

    db = FAISS.from_documents(texts, embeddings_model)
    retriever = db.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    response = qa.invoke({"chat_history": memory, "question": question})
    return response
