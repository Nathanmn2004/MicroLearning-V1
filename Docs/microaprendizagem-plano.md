# Plano: Aplicação de Microaprendizagem com Envio Diário por Email

## Contexto

O objetivo é criar uma aplicação que processa livros famosos em PDF, extrai lições diárias usando IA (OpenAI), e envia automaticamente um email por dia para todos os assinantes. O frontend é uma SPA em React JS que se comunica com o backend FastAPI via REST API.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React JS (Vite) + React Router + Axios |
| Backend/API | Python + FastAPI (REST API pura) |
| Banco de dados | SQLite (SQLAlchemy ORM) |
| PDF parsing | `pdfplumber` |
| Geração de conteúdo | OpenAI API (`openai`) |
| Envio de email | Resend SDK Python |
| Templates de email | Jinja2 (apenas para emails, não web) |
| Agendamento | APScheduler |
| CORS | `fastapi-cors` (middleware FastAPI) |

---

## Estrutura de Pastas

```
microlearning/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI: rotas REST + CORS
│   │   ├── models.py            # SQLAlchemy: Book, Lesson, Subscriber, EmailLog
│   │   ├── database.py          # Conexão SQLite + sessão
│   │   ├── scheduler.py         # Job diário (APScheduler)
│   │   ├── email_service.py     # Integração Resend
│   │   ├── pdf_processor.py     # Parsing PDF + geração de lições via OpenAI
│   │   └── templates/
│   │       ├── daily_email.html # Template HTML do email diário
│   │       └── confirm_email.html # Template email de confirmação
│   ├── scripts/
│   │   └── process_book.py      # CLI: python scripts/process_book.py livro.pdf
│   ├── books/                   # PDFs armazenados aqui
│   ├── .env                     # OPENAI_API_KEY, RESEND_API_KEY, etc.
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── main.jsx             # Entry point React
    │   ├── App.jsx              # Rotas (React Router)
    │   ├── api/
    │   │   └── client.js        # Axios instance (baseURL do backend)
    │   ├── pages/
    │   │   ├── Home.jsx         # Landing page com formulário de inscrição
    │   │   ├── Confirmed.jsx    # Página pós-confirmação de email
    │   │   └── Unsubscribed.jsx # Página pós-cancelamento
    │   └── components/
    │       ├── SubscribeForm.jsx # Formulário nome + email
    │       └── LessonPreview.jsx # Preview de uma lição (opcional/admin)
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## Banco de Dados (models.py)

**`books`** — livros cadastrados
`id, title, author, file_path, processed_at`

**`lessons`** — lições geradas por IA
`id, book_id, day_number, title, content, key_insight, reflection_question, source_pages`

**`subscribers`** — inscritos
`id, name, email, confirmed (bool), subscribed_at, confirm_token, unsubscribe_token`

**`email_log`** — histórico de envios
`id, subscriber_id, lesson_id, sent_at, status`

---

## API REST (main.py)

O FastAPI expõe endpoints JSON consumidos pelo React. CORS habilitado para `http://localhost:5173` (dev) e o domínio de produção.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/subscribe` | Recebe `{name, email}`, cria subscriber, envia email de confirmação |
| `GET` | `/api/confirm/{token}` | Confirma assinante, retorna `{success: true}` |
| `GET` | `/api/unsubscribe/{token}` | Remove assinante, retorna `{success: true}` |
| `GET` | `/api/health` | Health check |

---

## Fluxo 1 — Processar um Livro (CLI)

```bash
cd backend
python scripts/process_book.py books/"A Arte da Guerra.pdf"
```

1. `pdfplumber` extrai o texto completo do PDF
2. Texto é dividido em chunks (~800 tokens cada, respeitando parágrafos)
3. Para cada chunk, OpenAI gera uma lição estruturada:
   ```json
   {
     "title": "O poder do silêncio estratégico",
     "content": "Sun Tzu ensina que...",
     "key_insight": "Quem fala menos, observa mais.",
     "reflection_question": "Em que situação você usou o silêncio como vantagem?"
   }
   ```
4. Lições salvas na tabela `lessons` com `day_number` sequencial

---

## Fluxo 2 — Cadastro de Assinante (React + API)

1. Usuário acessa `http://localhost:5173` → `Home.jsx` renderiza `SubscribeForm.jsx`
2. Submit do form → `POST /api/subscribe` via Axios → backend cria subscriber + envia email de confirmação (Resend)
3. Usuário clica no link do email → `GET /api/confirm/{token}` → backend confirma
4. React Router redireciona para `/confirmed` → `Confirmed.jsx`
5. Cancelamento: `GET /api/unsubscribe/{token}` → redireciona para `/unsubscribed` → `Unsubscribed.jsx`

---

## Fluxo 3 — Email Diário (Scheduler)

APScheduler roda todo dia às **7h00 (configurável via .env)**:

1. Calcula `dia_atual = dias desde 2026-01-01 % total_lessons`
2. Busca a lição do dia na tabela `lessons`
3. Busca todos os `subscribers` com `confirmed=True`
4. Renderiza `daily_email.html` (Jinja2) com os dados da lição
5. Envia um email por assinante via Resend
6. Registra cada envio em `email_log`

**Template do email:**
- Cabeçalho: "Sua lição de hoje — {title}"
- Corpo: `content` + destaque para `key_insight`
- Pergunta do dia: `reflection_question`
- Rodapé: link de cancelamento `(/api/unsubscribe/{token})`

---

## Arquivos Críticos a Criar

### Backend

| Arquivo | Responsabilidade |
|---|---|
| `backend/app/main.py` | FastAPI com CORS + endpoints REST |
| `backend/app/models.py` | Modelos SQLAlchemy |
| `backend/app/database.py` | Setup SQLite + create_all |
| `backend/app/pdf_processor.py` | pdfplumber + chunking + OpenAI API |
| `backend/app/email_service.py` | Resend: confirmação + email diário |
| `backend/app/scheduler.py` | APScheduler: job diário |
| `backend/app/templates/daily_email.html` | Template Jinja2 do email |
| `backend/scripts/process_book.py` | CLI para processar PDFs |
| `backend/.env` | OPENAI_API_KEY, OPENAI_MODEL, RESEND_API_KEY, FROM_EMAIL, SEND_HOUR, FRONTEND_URL |

### Frontend

| Arquivo | Responsabilidade |
|---|---|
| `frontend/src/App.jsx` | React Router: `/`, `/confirmed`, `/unsubscribed` |
| `frontend/src/api/client.js` | Axios com baseURL da API |
| `frontend/src/pages/Home.jsx` | Landing page + chamada `POST /api/subscribe` |
| `frontend/src/pages/Confirmed.jsx` | Página de boas-vindas pós-confirmação |
| `frontend/src/components/SubscribeForm.jsx` | Form controlado com validação |

---

## requirements.txt (backend)

```
fastapi
uvicorn
sqlalchemy
pdfplumber
openai
resend
apscheduler
jinja2
python-dotenv
python-multipart
fastapi-cors
```

## package.json (frontend)

Dependências principais:
```
react, react-dom, react-router-dom, axios
```
Dev:
```
vite, @vitejs/plugin-react
```

---

## Variáveis de Ambiente (.env)

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
RESEND_API_KEY=re_...
FROM_EMAIL=noreply@suaempresa.com
SEND_HOUR=7
FRONTEND_URL=http://localhost:5173
```

---

## Verificação / Como Testar

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
python scripts/process_book.py books/livro.pdf  # processar um livro
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

### Testes de ponta a ponta
1. Abrir `http://localhost:5173` → preencher formulário
2. Confirmar que email de confirmação chega via Resend
3. Clicar no link → página `/confirmed` aparece, subscriber fica `confirmed=True` no banco
4. Disparar job manualmente via Python shell (`from app.scheduler import run_daily_job; run_daily_job()`)
5. Confirmar email diário chega e `email_log` registra o envio
