

from dataclasses import dataclass
import tiktoken

@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    text: str
    token_count: int
    chunker_version: str


class TokenChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64, version: str = "v1.0"):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.version = version
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def chunk(self, text: str, document_id: str) -> list[TextChunk]:
        ''' Create chunks of text based on the specified chunk size and overlap, returning a list of TextChunk objects. '''
        tokens = self.tokenizer.encode(text)
        chunks = []

        step = self.chunk_size - self.overlap
        for i in range(0, len(tokens), step):
            chunk_tokens = tokens[i: i + self.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunk_id = f"{document_id}#chunk_{len(chunks)}"

            chunks.append(
                TextChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    token_count=len(chunk_tokens),
                    chunker_version=self.version,
                )
            )
        return chunks


