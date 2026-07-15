from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = ROOT_DIR / "backend" / "app" / "templates" / "emails" / "templateFull.html"


def plain_text(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def markdown_to_email_html(markdown: str | None) -> str:
    if not markdown:
        return "Microlicao em preparacao."

    blocks = [block.strip() for block in re.split(r"\n{2,}", markdown) if block.strip()]
    rendered: list[str] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and all(line.startswith(("- ", "* ")) for line in lines):
            items = "".join(f"<li>{html.escape(line[2:].strip())}</li>" for line in lines)
            rendered.append(f"<ul>{items}</ul>")
            continue
        rendered.append(f"<p>{html.escape(' '.join(lines))}</p>")
    return "\n".join(rendered)


def render_template(context: dict[str, Any], template_path: Path = TEMPLATE_PATH) -> str:
    template = template_path.read_text(encoding="utf-8")
    values = {key: "" if value is None else str(value) for key, value in context.items()}

    def replace(match: re.Match[str]) -> str:
        return values.get(match.group(1), "")

    return re.sub(r"{{([A-Z_]+)}}", replace, template)


def build_lesson_email_context(
    *,
    lesson: dict[str, Any],
    book: dict[str, Any] | None = None,
    quote: dict[str, Any] | None = None,
) -> dict[str, Any]:
    content_html = lesson.get("content_html") or markdown_to_email_html(lesson.get("content_markdown"))
    reading_minutes = lesson.get("estimated_reading_minutes") or 5
    book_title = (book or {}).get("title") or "Microlicao do dia"
    book_author = (book or {}).get("author") or "MicroAprendizagem"
    quote_text = (quote or {}).get("quote_text") or "A melhor leitura e aquela que vira acao."
    quote_reference = (quote or {}).get("source_note") or book_title

    return {
        "PREHEADER_TEXT": plain_text(lesson.get("title")) or "Sua microlicao chegou",
        "TEMPO_LEITURA": reading_minutes,
        "DIA_NUMERO": 1,
        "LIVRO_TITULO": html.escape(book_title),
        "LIVRO_AUTOR": html.escape(book_author),
        "CAPITULO_NUMERO": 1,
        "CITACAO_TEXTO": html.escape(quote_text),
        "CITACAO_REFERENCIA": html.escape(quote_reference),
        "INSIGHT_TEXTO": content_html,
        "REFLEXAO_PERGUNTA": "Qual pequena acao voce pode aplicar hoje a partir desta ideia?",
        "CTA_URL": "https://microaprendizagem.com.br",
        "SEQUENCIA_PONTOS": "* * * - - - -",
        "SEQUENCIA_DIAS": 3,
        "PREFERENCES_URL": "https://microaprendizagem.com.br",
        "UNSUBSCRIBE_URL": "https://microaprendizagem.com.br",
        "EMPRESA_NOME": "MicroAprendizagem",
        "EMPRESA_ENDERECO": "Brasil",
    }


def render_lesson_email(
    *,
    lesson: dict[str, Any],
    book: dict[str, Any] | None = None,
    quote: dict[str, Any] | None = None,
) -> str:
    return render_template(build_lesson_email_context(lesson=lesson, book=book, quote=quote))
