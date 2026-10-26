

import tiktoken
from pydantic import BaseModel

from data_onboarding.domain import make_chunk_id


class TextChunk(BaseModel):
    document_id: str
    chunk_index: int
    chunk_id: str
    text_chunk: str
    chunker_version: str


class TokenChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64, version: str = "v1.0"):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.version = version
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def create_chunk(self, text: str, document_id: str) -> list[TextChunk]:
        ''' Create chunks of text based on the specified chunk size and overlap, returning a list of TextChunk objects. '''
        tokens = self.tokenizer.encode(text)
        chunks = []


        step = self.chunk_size - self.overlap
        for i in range(0, len(tokens), step):
            chunk_tokens = tokens[i: i + self.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunk_id = make_chunk_id(doc_id=document_id, chunk_index=i)

            chunks.append(
                TextChunk(
                    document_id = document_id,
                    chunk_index = i,
                    text_chunk = chunk_text,
                    chunk_id = chunk_id,
                    chunker_version=self.version
                )
            )
        return chunks


