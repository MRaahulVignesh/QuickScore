import os
import weaviate
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
import getpass
from langchain.embeddings import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.retrievers.document_compressors import CohereRerank
from backend.config.config import config

class VectorDB:
    def __init__(self):
        cohere_api_key = config.COHERE_API_KEY
        weaviate_api_key = config.WEAVIATE_API_KEY
        weaviate_url = config.WEAVIATE_URL

        self.client=weaviate.Client(
            url=weaviate_url,  # URL of your Weaviate instance
            auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),  # Replace w/ your Weaviate instance API key

            additional_headers={
                "X-Cohere-Api-Key": cohere_api_key, # Replace with your OpenAI key
            }
        )
                
        self.client.schema.delete_class("WikipediaLangChain")
        # Initialize the Cohere client in the constructor

        self.embeddings = CohereEmbeddings(model = "embed-multilingual-v3.0",cohere_api_key=cohere_api_key)

    def embed_and_store(self, document, class_name):
        print(document, class_name)
        # lets make sure its vectorizer is what the one we want
        class_definition = {
            "class": class_name, #should be obtainable from the doc_path
            "vectorizer": "text2vec-cohere",
            "vectorIndexConfig": {
                "distance": "cosine" # Set to "cosine" for English models; "dot" for multilingual models
            },
            "moduleConfig": { # specify the model you want to use
                    "generative-cohere": { 
                        "model": "command-xlarge-nightly",  #// Optional - Defaults to `command-xlarge-nightly`. 
                        # Can also use`command-xlarge-beta` and `command-xlarge`
                        "temperatureProperty": 1.1,  #// Optional
                        #"maxTokensProperty": <maxTokens>,  // Optional
                        #"kProperty": <k>, // Optional
                        #"stopSequencesProperty": <stopSequences>, // Optional
                        #"returnLikelihoodsProperty": <returnLikelihoods>, // Optional
                    },
                    "text2vec-cohere": {
                        "model": "embed-multilingual-v3.0", # Defaults to embed-multilingual-v3.0 if not set
                        # "truncate": "RIGHT", # Defaults to RIGHT if not set
                        #"baseURL": "https://proxy.yourcompanydomain.com"  // Optional. 
                        # Can be overridden by one set in the HTTP header.
                }
            }
        }

        self.client.schema.create_class(class_definition)

        metadata = [dict(year=2016, source=class_name)]

        documents = []
        idx = 0

        for document_fragment in document:
            document_fragment.metadata = metadata[idx]

        documents += document

        text_splitter = CharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 0,
        )
        docs = text_splitter.split_documents(documents)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 200,
        )
        docs1 = text_splitter.split_documents(documents)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 512,
            chunk_overlap = 100,
        )
        docs2 = text_splitter.split_documents(documents)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 256,
            chunk_overlap = 50,
        )
        docs3 = text_splitter.split_documents(documents)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 128,
            chunk_overlap = 25,
        )
        docs4 = text_splitter.split_documents(documents)

        try:    
            Weaviate.from_documents(docs, self.embeddings, index_name=class_name, client=self.client, by_text=False)
            Weaviate.from_documents(docs1, self.embeddings, index_name=class_name, client=self.client, by_text=False)
            Weaviate.from_documents(docs2, self.embeddings, index_name=class_name, client=self.client, by_text=False)
            Weaviate.from_documents(docs3, self.embeddings, index_name=class_name, client=self.client, by_text=False)
            Weaviate.from_documents(docs4, self.embeddings, index_name=class_name, client=self.client, by_text=False)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return True