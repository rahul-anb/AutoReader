from PyPDF2 import PdfReader
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain
    


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multi pdf", page_icon=":books:")
    
    st.header("Chat with multi pdf")
    st.text_input("Ask a question")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs= st.file_uploader("Upload a pdf and click process", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                
                #get text cgunk
                text_chunks = get_text_chunks(raw_text)

                
                vectorstore = get_vectorstore(text_chunks)
                
                
                # st.write(text_chunks)
                
                #create converstation chain
                conversation = get_conversation_chain(vectorstore)
        
        
    # pdf_file_obj = open('chatwithpdf.pdf', 'rb')
    # pdfReader = PdfReader(pdf_file_obj)
    # # print(len(pdfReader.pages))
    # pageObj = pdfReader.pages[0]
 
    # # e text from p    age
    # # print(pageObj.extract_text())
    # text = ""
    
    # for page in pdfReader.pages:
    #     text += page.extract_text()
    # print(text)
    # # closing the pdf file object
    # pdf_file_obj.close()
        
if __name__ =="__main__":
    main()