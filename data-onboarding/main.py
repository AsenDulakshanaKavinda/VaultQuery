

from dataclasses import dataclass
from pydantic import BaseModel
import tiktoken
import uuid

class TextChunk(BaseModel):
    text: str
    document_id: str
    chunked_text: str




class TokenChunker:
    def __init__(self, chunk_size: int = 100, overlap: int = 64, version: str = "v1.0"):
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

            chunks.append(
                TextChunk(
                    text=text,
                    chunked_text=chunk_text,
                    document_id=document_id,
                )
            )
            # print("---")
            # print(f"text: {text} ")
            print("---")
            print(f"chunk_text: {chunk_text} ")
            print("---")
            print(f"document_id: {document_id} ")
            print("---")
            # print(tokens)
            # print("---")



        return chunks



if __name__ == "__main__":
    t = "The main function is explicitly instructing how the coroutines should work together. This involves manually scheduling, so technically it does not meet the criteria for truly symmetrical coroutines. We are mimicking some of the functionality of sym‐ metrical coroutines as an educational exercise. A true symmetrical coroutine would pass control from the reader to the writer without having to return to the main function; this is restricted by Rust’s borrowing rules, as both coroutines will need to reference each other. Despite this, it is still a useful example to demonstrate how writing your own coroutines can provide more functionality. We are now going to move on to looking at async behavior and how we can mimic some of this functionality with simple coroutines.Throughout this book, we have controlled the flow of the async task internally. For instance, when we implement the Future trait, we get to choose when to return Pending or Ready, depending on the internal logic of the poll function. The same goes for our async functions; we choose when the async task might yield control back to the executor with the await syntax and choose when the async task returns Ready with return statements. We can control these async tasks with external Sync primitives such as atomic values and mutexes by getting the async task to react to changes and values in these atomic values and mutexes. However, the logic reacting to external signals has to be coded into the async task before sending the async task to the runtime. For simple cases, this can be fine, but it does expose the async tasks to being brittle if the system around the async task is evolving. This also makes the async task harder to use in other contexts. The async task might also need to know the state of other async tasks before reacting, and this can lead to potential problems such as deadlocks."
    tc = TokenChunker()
    chunk = tc.create_chunk(text=t, document_id=str(uuid.uuid4()))
    
