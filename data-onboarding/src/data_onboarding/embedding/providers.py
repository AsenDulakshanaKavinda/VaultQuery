
from pathlib import Path
from typing import Protocol
from data_onboarding.observability import log

from sentence_transformers import SentenceTransformer


class Embedder(Protocol):
    model_name: str

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class LocalSentenceTransformerEmbedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        model_dir: str | Path = "models/all-MiniLM-L6-v2",
    ) -> None:
        self.model_name = model_name
        self.model_dir = Path(model_dir).resolve()

        if self._is_model_downloaded():
            log.info(f"Loading local embedding model: {self.model_dir}")

            self.model = SentenceTransformer(
                str(self.model_dir),
                local_files_only=True,
            )
        else:
            log.info(f"Downloading embedding model: {self.model_name}")

            self.model_dir.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # Download the model from Hugging Face.
            model = SentenceTransformer(self.model_name)

            # Save all required model files locally.
            model.save(str(self.model_dir))

            self.model = model

            log.info(f"Model saved to: {self.model_dir}")

    def _is_model_downloaded(self) -> bool:
        return (
            self.model_dir.is_dir()
            and (self.model_dir / "modules.json").is_file()
            and (self.model_dir / "config.json").is_file()
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()
