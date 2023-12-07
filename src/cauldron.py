import chromadb
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings


class Cauldron():
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.persist_directory = '/.sapphire'
        self.__setup_client()

    def reingest(self) -> None:
        self.db = self.__get_new_client()

    def __setup_client(self) -> None:
        """
        if last updated != today or user asked to reingest, call __setup_new_client()
        else: use existing client
        """
        if self.__should_reingest():
            self.db = self.__get_new_client()
        else:
            self.db = self.__get_existing_client()

    def __should_reingest(self) -> bool:
        """
        return True if cache doesn't exist or last updated != today
        """
        pass

    def __get_existing_client(self):
        client = chromadb.PersistentClient(self.persist_directory)
        return client

    def __get_new_client(self):
        embeddings = OpenAIEmbeddings()
        docs = self.__get_docs()
        client = Chroma.from_documents(
            docs, embeddings, persist_directory=self.persist_directory)
        return client

    def __get_docs(self, chunk_size=1000, chunk_overlap=20) -> list:
        loader = DirectoryLoader(self.directory)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        return docs
