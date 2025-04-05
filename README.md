# Sentiment Analysis and Semantic Search with Qdrant

## 📌 Project Description
a Python library that processes text data, generates **embeddings**, and stores them in the **Qdrant** vector database for similarity search.

## Features

- 📊 Batch processing of large datasets from Parquet files
- 🔍 Semantic search capabilities with configurable thresholds
- 🧠 Sentence Transformer integration for text embeddings
- 🚀 Efficient vector storage and retrieval with Qdrant
- 📈 Progress tracking with time estimation
- 📝 Configurable logging with loguru
- ⚙️ Pydantic-based configuration management

## 📦 Installation
The project is compatible with **Python 3.8+**. To install the required dependencies, run:

1. Clone the repository:
```bash
git clone https://github.com/ozanguneyli/Sentiment-Analyzer.git
cd Sentiment-Analyzer
```

```bash
# Install dependencies using Poetry
poetry install
```

If **Poetry** is not installed, you can install it using:
```bash
pip install poetry
```

## 🛠 Usage
1. **Convert your data into Parquet format** (e.g., `data.parquet`)
2. **Update the `path_to_parquet_data` variable in `main.py`**
3. **Change the model name (`all-MiniLM-L6-V2`) if needed**
4. **Run the script using:**

```bash
python main.py
```

## 🔍 Example Usage
Once the project is running, embeddings will be uploaded, and you can perform a similarity search as follows:

```python
query = 'I really liked this product.'
results = analyzer.search(query=query, collection_name='sentiment_collection')
print(results)
```

## 📂 Project Structure
```
project/
│── sentiment_analyzer.py  # Core class for sentiment analysis
│── client.py              # Handles communication with Qdrant server
│── utils.py               # Utility functions (preprocessing, file reading, etc.)
│── constants.py           # Default settings
│── log_config.py          # Logging configuration
│── main.py                # Main execution script
│── README.md              # Project documentation
```

## License

[MIT License](LICENSE)
