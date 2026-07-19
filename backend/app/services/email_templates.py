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


def _strip_markdown(value: str) -> str:
    value = re.sub(r"^#{1,6}\s+", "", value.strip())
    value = re.sub(r"[*_`>\[\]]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _paragraph_html(value: str) -> str:
    text = _strip_markdown(value)
    if not text:
        return ""
    return (
        '<p style="margin:0 0 14px 0; font-family: Helvetica, Arial, sans-serif; '
        'font-size:14px; line-height:23px; color:#1E2A24;">'
        f"{html.escape(text)}"
        "</p>"
    )


def _topic_body_html(sections: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for section_index, section in enumerate(sections):
        if section_index > 0:
            parts.append(
                '<p style="margin:18px 0 8px 0; font-family: Georgia, '
                "'Times New Roman', serif; font-size:15px; line-height:22px; "
                'font-weight:bold; color:#12312A;">'
                f"{html.escape(section['title'])}"
                "</p>"
            )
        parts.extend(
            paragraph
            for paragraph in (_paragraph_html(line) for line in section["paragraphs"])
            if paragraph
        )
    return "".join(parts)


def _group_sections(sections: list[dict[str, Any]], max_groups: int) -> list[list[dict[str, Any]]]:
    if len(sections) <= max_groups:
        return [[section] for section in sections]

    total_chars = sum(section["char_count"] for section in sections)
    target_chars = max(1, total_chars // max_groups)
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0

    for index, section in enumerate(sections):
        remaining_sections = len(sections) - index
        remaining_groups = max_groups - len(groups)
        if (
            current
            and current_chars >= target_chars
            and remaining_sections >= remaining_groups
        ):
            groups.append(current)
            current = []
            current_chars = 0

        current.append(section)
        current_chars += section["char_count"]

    if current:
        groups.append(current)

    while len(groups) < max_groups:
        groups.append([])

    return groups[:max_groups]


def extract_key_topics(markdown: str | None, max_topics: int = 3) -> list[dict[str, str]]:
    if not markdown:
        return []

    sections: list[dict[str, Any]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    def append_section() -> None:
        if not current_title or not current_lines:
            return
        paragraphs = [_strip_markdown(line) for line in current_lines if _strip_markdown(line)]
        if not paragraphs:
            return
        sections.append(
            {
                "title": _strip_markdown(current_title),
                "paragraphs": paragraphs,
                "char_count": sum(len(paragraph) for paragraph in paragraphs),
            }
        )

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading = re.match(r"^#{2,3}\s+(.+)$", line)
        if heading:
            append_section()
            current_title = heading.group(1)
            current_lines = []
            continue

        if current_title:
            current_lines.append(line)

    append_section()

    if not sections:
        paragraphs = [
            _strip_markdown(block)
            for block in re.split(r"\n{2,}", markdown)
            if _strip_markdown(block)
        ]
        sections = [
            {
                "title": f"Ponto {index + 1}",
                "paragraphs": [paragraph],
                "char_count": len(paragraph),
            }
            for index, paragraph in enumerate(paragraphs[:max_topics])
        ]

    topics: list[dict[str, str]] = []
    for group in _group_sections(sections, max_topics):
        if not group:
            continue
        topics.append(
            {
                "title": group[0]["title"],
                "text": _topic_body_html(group),
            }
        )

    return topics


def render_template(context: dict[str, Any], template_path: Path = TEMPLATE_PATH) -> str:
    template = template_path.read_text(encoding="utf-8")
    values = {key: "" if value is None else str(value) for key, value in context.items()}

    def replace(match: re.Match[str]) -> str:
        return values.get(match.group(1), "")

    return re.sub(r"{{([A-Z0-9_]+)}}", replace, template)


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
    topics = extract_key_topics(lesson.get("content_markdown"))
    topic_context: dict[str, str] = {}
    for index in range(1, 4):
        topic = topics[index - 1] if index <= len(topics) else None
        topic_context[f"TOPICO_{index}_TITULO"] = html.escape(
            topic["title"] if topic else "Ideia central"
        )
        topic_context[f"TOPICO_{index}_TEXTO"] = (
            topic["text"] if topic else _paragraph_html(
                "A microlicao de hoje aprofunda este ponto no contexto do livro."
            )
        )

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
        **topic_context,
    }


def render_lesson_email(
    *,
    lesson: dict[str, Any],
    book: dict[str, Any] | None = None,
    quote: dict[str, Any] | None = None,
) -> str:
    return render_template(build_lesson_email_context(lesson=lesson, book=book, quote=quote))
