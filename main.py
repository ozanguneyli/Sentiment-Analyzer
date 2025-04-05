from project.sentiment_analyzer import SentimentAnalyzer, SentimentAnalyzerConfig
from project.utils import read_parquet_in_batches, preprocess_text
from project.constants import default_sentiment_threshold
from project.log_config import configure_logger
import time

configure_logger()

config = SentimentAnalyzerConfig(
    threshold=default_sentiment_threshold,
    qdrant_host='localhost',
    qdrant_port=6333,
    model_name='all-MiniLM-L6-V2'
)

analyzer = SentimentAnalyzer(config=config)

# calculate time for how much time left

total_batches = 489644 // 128

if 489644 % 128 != 0:
    total_batches +=1

start_time = time.time()


# read the parquet file and load the embeddings

batch_count = 0
for batch in read_parquet_in_batches(path_to_parquet_data, batch_size=128):
    print(f"processing batch {batch_count + 1}/{total_batches} ({(batch_count + 1) / total_batches * 100:.2f}%)")
    preprocessed_data = [preprocess_text(text) for text in batch['text']]
    analyzer.upload_embeddings(data=preprocessed_data, batch_size=128, collection_name='sentiment_collection',start_id = batch_count * 128)
    batch_count += 1

    elapsed_time = time.time() - start_time
    elapsed_minutes = elapsed_time / 60
    estimated_total_time = (elapsed_time / batch_count) * total_batches
    estimated_total_minutes = estimated_total_time / 60
    remaining_time = estimated_total_time - elapsed_time
    remaining_minutes = remaining_time / 60
    print(f"elapsed time: {elapsed_minutes:.2f} minutes, estimated total time: {estimated_total_minutes:2f} minutes, remaining time: {remaining_minutes:2f} minutes")
print(f"total batches processed: {batch_count} / {total_batches}")


query = 'bu ürünü çok beğendim.'
results = analyzer.search(query = query, collection_name = 'sentiment_collection')
print(results)
