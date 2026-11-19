import io

import pymupdf
from docx import Document


class LayoutParser:
    @staticmethod
    def parse(file_bytes: bytes, filename: str) -> str:
        """Parse the given file bytes based on the file extension and return the extracted text in markdown format."""
        if filename.endswith(".pdf"):
            return LayoutParser._parse_pdf(file_bytes)
        elif filename.endswith(".docx"):
            return LayoutParser._parse_docx(file_bytes)
        raise ValueError(f"Unsupported file format: {filename}")

    @staticmethod
    def _parse_pdf(file_bytes: bytes) -> str:
        with pymupdf.open(stream=file_bytes, filetype="pdf") as document:
            pages: list[str] = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(f"## Page {page_number}\n\n{text}")

            return "\n\n".join(pages)

    @staticmethod
    def _parse_docx(file_bytes: bytes) -> str:
        """Parse DOCX bytes and return the extracted text in markdown format."""
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
