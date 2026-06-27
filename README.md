# Microaprendizagem

Aplicação full stack para processar livros em PDF, gerar lições diárias com OpenAI e enviar emails automáticos para assinantes confirmados.

## Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Configure `backend/.env` com suas chaves reais antes de enviar emails ou gerar conteúdo com IA. Com os placeholders atuais, o backend roda em modo seco para email e gera lições fallback no processamento de PDFs.

Para processar um livro:

```bash
cd backend
python scripts/process_book.py books\livro.pdf
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

A SPA abre em `http://localhost:5173` e usa `VITE_API_URL` quando definido, ou `http://localhost:8000` por padrão.

## Fluxo principal

1. O usuário se inscreve em `/`.
2. O backend cria o assinante e envia o link de confirmação para `/confirmed?token=...`.
3. A página React confirma chamando `GET /api/confirm/{token}`.
4. O scheduler envia a lição diária às 7h por padrão.
5. O link de cancelamento abre `/unsubscribed?token=...` e chama `GET /api/unsubscribe/{token}`.
