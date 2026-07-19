from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import fitz
from dotenv import dotenv_values
from google import genai
from google.genai import types


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
BOOKS_DIR = ROOT_DIR / "Livros"
METADATA_PATH = BOOKS_DIR / "metadata.json"

sys.path.insert(0, str(BACKEND_DIR))


def load_env() -> None:
    for env_path in (ROOT_DIR / ".env", ROOT_DIR / "backend" / ".env"):
        values = dotenv_values(env_path)
        for key, value in values.items():
            if value is not None:
                os.environ.setdefault(key, value)


load_env()

from app.core.config import settings  # noqa: E402
from app.repositories.supabase_client import get_supabase_admin_client  # noqa: E402


def load_metadata() -> list[dict[str, Any]]:
    if not METADATA_PATH.exists():
        raise RuntimeError(f"Metadata file not found: {METADATA_PATH}")
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def find_book(slug: str) -> dict[str, Any]:
    for book in load_metadata():
        if book["slug"] == slug:
            return book
    raise RuntimeError(f"Book slug not found in metadata: {slug}")


def find_books_by_track(content_track: str) -> list[dict[str, Any]]:
    books = [
        book
        for book in load_metadata()
        if book.get("content_track") == content_track or content_track == "todos"
    ]
    if not books:
        raise RuntimeError(f"No books found for content track: {content_track}")
    return books


def normalize_whitespace(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pages(pdf_path: Path, max_pages: int, max_chars: int) -> tuple[str, int]:
    if not pdf_path.exists():
        raise RuntimeError(f"PDF not found: {pdf_path}")

    parts: list[str] = []
    with fitz.open(pdf_path) as document:
        page_count = document.page_count
        for index, page in enumerate(document):
            if index >= max_pages:
                break
            text = normalize_whitespace(page.get_text("text"))
            if text:
                parts.append(f"[page {index + 1}]\n{text}")
            if sum(len(part) for part in parts) >= max_chars:
                break

    return "\n\n".join(parts)[:max_chars], page_count


def build_prompt(book: dict[str, Any], extracted_text: str) -> str:
    author = book.get("author") or "autor nao informado"
    return f"""
Voce e um editor educacional criando uma microlicao em pt-BR.

Livro: {book["title"]}
Autor: {author}
Categoria: {book.get("category") or "geral"}

Regras:
- Crie uma sintese educacional original, sem substituir a leitura do livro.
- Nao copie paragrafos longos do texto.
- Use no maximo 3 citacoes literais curtas.
- Cada citacao literal deve ter ate 90 caracteres.
- Nao invente citacoes.
- Se nao houver citacao curta confiavel no trecho, retorne "quotes": [].
- O conteudo deve ser uma leitura completa de 15 a 20 minutos.
- Escreva entre 2800 e 3600 palavras no campo "content_markdown".
- Estruture a microlicao com titulo, introducao, 5 a 7 secoes explicativas, exemplos praticos, uma sintese final e um exercicio de aplicacao.
- Use markdown simples com subtitulos "##".
- O WhatsApp deve ser mais curto e direto que o markdown.
- Nao use emojis.
- Responda somente JSON valido, sem markdown fence.

Formato JSON:
{{
  "title": "titulo curto da microlicao",
  "content_markdown": "microlicao em markdown",
  "whatsapp_content": "versao compacta para WhatsApp",
  "quotes": [
    {{
      "quote_text": "citacao curta encontrada no texto",
      "page_number": 1,
      "source_note": "observacao curta sobre o contexto"
    }}
  ]
}}

Trecho extraido:
{extracted_text}
""".strip()


def clean_json_response(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    return json.loads(text)


def strip_unsupported_symbols(value: Any) -> Any:
    if isinstance(value, str):
        return "".join(char for char in value if ord(char) <= 0xFFFF)
    if isinstance(value, list):
        return [strip_unsupported_symbols(item) for item in value]
    if isinstance(value, dict):
        return {key: strip_unsupported_symbols(item) for key, item in value.items()}
    return value


def generate_lesson(book: dict[str, Any], extracted_text: str) -> dict[str, Any]:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=build_prompt(book, extracted_text),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=12000,
            temperature=0.35,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response")
    return strip_unsupported_symbols(clean_json_response(response.text))


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def quote_is_supported(quote_text: str, source_text: str) -> bool:
    normalized_quote = normalize_whitespace(quote_text).casefold()
    normalized_source = normalize_whitespace(source_text).casefold()
    return normalized_quote in normalized_source


def upsert_book(client: Any, book: dict[str, Any], page_count: int) -> dict[str, Any]:
    response = (
        client.table("books")
        .select("*")
        .eq("slug", book["slug"])
        .limit(1)
        .execute()
    )
    data = {
        "slug": book["slug"],
        "title": book["title"],
        "author": book.get("author"),
        "category": book.get("category"),
        "content_track": book.get("content_track") or "todos",
        "file_path": str(Path("Livros") / book["file"]),
        "page_count": page_count,
        "processing_status": "completed",
        "processed_at": datetime.now(UTC).isoformat(),
        "enabled": True,
    }
    if response.data:
        updated = client.table("books").update(data).eq("id", response.data[0]["id"]).execute()
        return updated.data[0]
    created = client.table("books").insert(data).execute()
    return created.data[0]


def save_lesson(
    client: Any,
    book_record: dict[str, Any],
    draft: dict[str, Any],
    extracted_text: str,
) -> dict[str, Any]:
    markdown = str(draft.get("content_markdown") or "").strip()
    whatsapp = str(draft.get("whatsapp_content") or "").strip()
    words = word_count(markdown)
    lesson_data = {
        "book_id": book_record["id"],
        "title": str(draft.get("title") or book_record["title"]).strip(),
        "content_markdown": markdown,
        "whatsapp_content": whatsapp,
        "content_track": book_record.get("content_track") or "todos",
        "word_count": words,
        "estimated_reading_minutes": max(1, round(words / 180)),
        "status": settings.generated_lesson_status,
    }
    if settings.generated_lesson_status == "approved":
        lesson_data["approved_at"] = datetime.now(UTC).isoformat()
    lesson = client.table("lessons").insert(lesson_data).execute().data[0]

    quote_rows = []
    for quote in draft.get("quotes") or []:
        quote_text = str(quote.get("quote_text") or "").strip()
        if not quote_text or len(quote_text) > 90:
            continue
        verified = quote_is_supported(quote_text, extracted_text)
        quote_rows.append(
            {
                "lesson_id": lesson["id"],
                "book_id": book_record["id"],
                "quote_text": quote_text,
                "page_number": quote.get("page_number"),
                "source_note": quote.get("source_note"),
                "verified": verified,
            }
        )
    if quote_rows:
        client.table("lesson_quotes").insert(quote_rows).execute()

    return lesson


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process one book PDF into a draft micro-lesson.")
    parser.add_argument("--slug", help="Book slug from Livros/metadata.json")
    parser.add_argument("--content-track", help="Process every book from this content track.")
    parser.add_argument("--max-pages", type=int, default=30)
    parser.add_argument("--max-chars", type=int, default=90000)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.slug and not args.content_track:
        raise RuntimeError("Use --slug or --content-track")

    books = [find_book(args.slug)] if args.slug else find_books_by_track(args.content_track)
    for book in books:
        process_book(book, args)


def process_book(book: dict[str, Any], args: argparse.Namespace) -> None:
    extracted_text, page_count = extract_pages(BOOKS_DIR / book["file"], args.max_pages, args.max_chars)
    if not extracted_text:
        raise RuntimeError("No text extracted from PDF")

    draft = generate_lesson(book, extracted_text)
    if args.dry_run:
        print(json.dumps(draft, ensure_ascii=True, indent=2))
        return

    client = get_supabase_admin_client()
    book_record = upsert_book(client, book, page_count)
    lesson = save_lesson(client, book_record, draft, extracted_text)
    print(f"Created lesson {lesson['id']} for {book['slug']} using {settings.gemini_model}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise
