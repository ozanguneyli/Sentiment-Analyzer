from typing import List
from project.client import QdrantClientManager
from sentence_transformers import SentenceTransformer
from loguru import logger
from pydantic import BaseModel


class SentimentAnalyzerConfig(BaseModel):
    threshold : float
    qdrant_host : str
    qdrant_port : int
    model_name : str


class SentimentAnalyzer():
    
    """
    a class used to analyze the sentiment of text

    """

    def __init__(self, config : SentimentAnalyzerConfig):
        """
        initialize the sentiment with a sentiment threshold

        args:
            threshold (float) : the threshold for sentiment analysis
            qdrant_host (str) : the host adress for qdrant
            qdrant_port (int) : the port for qdrant
            model_name (str) : the name of the model used for encoding

        """
        self.threshold = config.threshold
        self.client = QdrantClientManager(
            host = config.qdrant_host, 
            port = config.qdrant_port
            )
        self.model = SentenceTransformer(config.model_name)
        logger.info('sentimentAnalyzer initialized with config: {}',config)


    def analyze(self, text : str) -> str:
        """
        analyze the sentiment of a given text

        args:
            text (str): text to analyze

        returns:
            str: sentiment analysis result

        """

        # implement sentiment analysis logic
        sentiment = "positive" if self.threshold > 0.5 else "negative"
        return sentiment

    def create_collection(self, collection_name: str):
        """
        Create a qdrant collection if it does not exist.

        args:
            collection_name (str): name of the collection
        """

        if not self.client.client.collection_exists(collection_name):
            self.client.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    'size': 384,  # vector size
                    'distance': 'Cosine'  # distance metric
                }
            )
            logger.info('created collection: {}',collection_name)




    def upload_embeddings(self, data: List[str], batch_size: int, collection_name: str,start_id : int = 0):
        """
        upload embeddings to the Qdrant collection.

        args:
            data (List[str]): list of texts to generate embeddings for
            batch_size (int): batch size for embedding generation
            collection_name (str): name of the Qdrant collection
            start_id (int): Starting id for the batch.
        """

        self.create_collection(collection_name)

        vectors = self.model.encode(sentences=data, batch_size=batch_size, normalize_embeddings=True)
        vectors = [vector.tolist() for vector in vectors]

        try:
            batch_number = 0
            for i in range(0, len(vectors), batch_size):
                batch_vectors = vectors[i:i + batch_size]
                points=[
                    {
                        'id': idx,
                        'vector': vector
                    } for idx, vector in enumerate(batch_vectors)
                ]
                self.client.upload_batch(batch=points,collection_name=collection_name)
                logger.info(f'uploaded batch {batch_number + 1} starting with ID {start_id + batch_number * batch_size} to collection: {collection_name}')
                print(f"uploaded batch {batch_number + 1} starting with ID {start_id + batch_number * batch_size} to collection {collection_name}")
                batch_number += 1
        except Exception as e:
            logger.error('an error occured while uploading embeddings: {}',e)



    
    