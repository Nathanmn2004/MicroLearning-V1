import json
from pathlib import Path

from openai import OpenAI
import pdfplumber
from sqlalchemy.orm import Session

from .config import get_settings
from .models import Book, Lesson

settings = get_settings()


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    pages: list[dict] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"page": index, "text": text.strip()})
    return pages


def chunk_pages(pages: list[dict], max_words: int = 650) -> list[dict]:
    chunks: list[dict] = []
    current_text: list[str] = []
    current_pages: list[int] = []
    current_words = 0

    for page in pages:
        paragraphs = [part.strip() for part in page["text"].split("\n\n") if part.strip()]
        for paragraph in paragraphs:
            words = paragraph.split()
            if current_text and current_words + len(words) > max_words:
                chunks.append(
                    {
                        "text": "\n\n".join(current_text),
                        "pages": _format_pages(current_pages),
                    }
                )
                current_text = []
                current_pages = []
                current_words = 0

            current_text.append(paragraph)
            current_pages.append(page["page"])
            current_words += len(words)

    if current_text:
        chunks.append({"text": "\n\n".join(current_text), "pages": _format_pages(current_pages)})

    return chunks


def generate_lesson(chunk_text: str) -> dict:
    if not settings.openai_api_key or settings.openai_api_key.startswith("sk-..."):
        return _fallback_lesson(chunk_text)

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.openai_model,
        max_tokens=900,
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Você transforma trechos de livros em uma lição diária curta, clara e prática. "
                    "Responda apenas com JSON válido."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Crie uma lição de microaprendizagem a partir do trecho abaixo. "
                    "Use as chaves title, content, key_insight e reflection_question.\n\n"
                    f"{chunk_text}"
                ),
            }
        ],
    )
    content = response.choices[0].message.content
    if not content:
        return _fallback_lesson(chunk_text)
    return json.loads(content)


def process_book(db: Session, pdf_path: str | Path, title: str | None = None, author: str | None = None) -> Book:
    pdf_path = Path(pdf_path)
    pages = extract_pdf_pages(pdf_path)
    chunks = chunk_pages(pages)

    book = Book(title=title or pdf_path.stem, author=author, file_path=str(pdf_path))
    db.add(book)
    db.flush()

    for day_number, chunk in enumerate(chunks, start=1):
        data = generate_lesson(chunk["text"])
        db.add(
            Lesson(
                book_id=book.id,
                day_number=day_number,
                title=data["title"],
                content=data["content"],
                key_insight=data["key_insight"],
                reflection_question=data["reflection_question"],
                source_pages=chunk["pages"],
            )
        )

    db.commit()
    db.refresh(book)
    return book


def _fallback_lesson(chunk_text: str) -> dict:
    first_sentence = chunk_text.replace("\n", " ").strip().split(".")[0][:180]
    return {
        "title": "Lição extraída do trecho",
        "content": first_sentence or "Releia o trecho e identifique a ideia central.",
        "key_insight": "Transforme uma ideia do texto em uma ação pequena para hoje.",
        "reflection_question": "Qual decisão prática este trecho ajuda você a tomar?",
    }


def _format_pages(pages: list[int]) -> str:
    unique_pages = sorted(set(pages))
    if not unique_pages:
        return ""
    if len(unique_pages) == 1:
        return str(unique_pages[0])
    return f"{unique_pages[0]}-{unique_pages[-1]}"
