import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db
from app.pdf_processor import process_book


def main() -> None:
    parser = argparse.ArgumentParser(description="Processa um PDF e gera lições diárias.")
    parser.add_argument("pdf_path", help="Caminho do arquivo PDF.")
    parser.add_argument("--title", help="Título do livro.")
    parser.add_argument("--author", help="Autor do livro.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        raise SystemExit(f"PDF não encontrado: {pdf_path}")

    init_db()
    db = SessionLocal()
    try:
        book = process_book(db, pdf_path, title=args.title, author=args.author)
        print(f"Livro processado: {book.title} ({len(book.lessons)} lições)")
    finally:
        db.close()


if __name__ == "__main__":
    main()

