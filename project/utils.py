import pandas as pd
from typing import Generator



def preprocess_text(text: str) -> str:
    """
    preprocess the text for sentiment analysis

    args:
        text (str): text to preprocess

    returns:
        str: preprocessed text

    """

    # implement text preprocessing logic
    preprocessed_text = text.lower()
    return preprocessed_text

def read_parquet_in_batches(file_path: str, batch_size: int) -> Generator[pd.DataFrame,None,None]:
    """
    reads a parquet file in batches

    args:
        file_path (str): path to parquet file
        batch_size (int): number of rows per patch

    yields:
        generator[pd.DataFrame,None,None]: generator of dataframes

    """

    import pyarrow.parquet as pq

    parquet_file = pq.ParquetFile(file_path)
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        yield batch.to_pandas()