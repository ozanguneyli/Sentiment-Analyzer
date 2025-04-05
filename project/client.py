from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)




class QdrantClientManager:

    """
    a class to interact with QdrantClient

    """

    def __init__(self, host: str, port: int, api_key: str = None):

        """
        args:
            host (str) : host adress of the qdrant server
            port (int) : port number of the qdrant server
            api_key (str, optional) : api key

        """
        self.client = QdrantClient(host=host, port=port, api_key=api_key)

    def upload_batch(self, batch, collection_name):

        """
        uploads batch to collection

        args:
            batch : list of data points to be uploaded
            collection_name : name of the collection

        """

        try:
            self.client.upsert(
                collection_name=collection_name,
                points=batch
               )
            logger.info(f"uploaded batch starting with ID {batch[0]['id']} to collection {collection_name}")
        except Exception as e:
            logger.error(f"an error occurred during batch upload: {e}")

    def search(self, query: str, collection_name: str, limit: int = 10, score_threshold : float = 0.5):

        """
        search for the closest points related to the given query in the qdrant vector store

        args:
            query (str): query text
            collection_name (str): name of the qdrant collection
            limit (int,optional): number of results to return. default = 10 
            score_threshold (float,optional): minimum score threshold. default = 0.5

        returns:
            List: List of search results
        """

        try:
            query_vector = self.model.encode(query, normalize_embeddings=True).tolist()
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            print(f"search results: {results}")
            return results
        except Exception as e:
            logger.error(f"an error occurred during search: {e}")
            return []
