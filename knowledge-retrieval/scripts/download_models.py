from pathlib import Path

from fastembed import SparseTextEmbedding, TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

LOCAL_CACHE = Path("./models_cache")

models = {
    "dense": {
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "class": TextEmbedding,
    },
    "sparse": {
        "name": "Qdrant/bm25",
        "class": SparseTextEmbedding,
    },
    "reranker": {
        "name": "Xenova/ms-marco-MiniLM-L-6-v2",
        "class": TextCrossEncoder,
    },
}

for model_type, config in models.items():
    model_name = config["name"]
    model_dir = LOCAL_CACHE / model_name.replace("/", "--")

    model_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {model_type}: {model_name}")
    print(f"Saving to: {model_dir}")

    config["class"](
        model_name=model_name,
        cache_dir=str(model_dir),
    )

    print(f"Successfully downloaded {model_type}\n")

print(f"All models saved to {LOCAL_CACHE.resolve()}")


