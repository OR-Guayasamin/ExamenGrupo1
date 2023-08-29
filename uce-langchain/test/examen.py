import os

from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import streamlit as st

os.environ['OPENAI_API_KEY'] = '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'
default_doc_name = 'Documento-de-examen-Grupo1.pdf'


def process_doc(
        path: str = '',
        is_local: bool = False,
        question: str = ''
):
    _, loader = os.system(f'curl -o {default_doc_name} {path}'), PyPDFLoader(f"./{default_doc_name}") if not is_local \
        else PyPDFLoader(path)

    documento = loader.load_and_split()

    print(documento[-1])

    db = Chroma.from_documents(documento, embedding=OpenAIEmbeddings())

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=db.as_retriever())

    st.write(qa.run(question))
    # print(qa.run(question))


def client():
    st.title('Manejo de documento Langchain')
    uploader = st.file_uploader('Cargar PDF', type='pdf')

    if uploader:
        with open(f'./{default_doc_name}', 'wb') as f:
            f.write(uploader.getbuffer())
        st.success('Correcto')

    question = st.text_input('',
                             placeholder='Give response about your PDF', disabled=not uploader)

    if st.button('Enviar pregunta'):
        if uploader:
            process_doc(
                path=default_doc_name,
                is_local=True,
                question=question
            )
        else:
            st.info('No has cargado un archivo')


if __name__ == '__main__':
    client()
    # process_doc()