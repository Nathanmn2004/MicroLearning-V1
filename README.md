# MicroAprendizagem

MicroAprendizagem é uma landing page com backend de apoio para vender e operar uma assinatura de microlições baseadas em livros selecionados. A proposta do produto é transformar ideias de livros completos em leituras curtas, práticas e entregáveis por WhatsApp e e-mail.

## O que existe no projeto

- Landing page em React com copy comercial, seções de benefícios, planos, FAQ e CTA para checkout da Cakto.
- API FastAPI com configuração centralizada, CORS e health checks.
- Worker Arq preparado para tarefas assíncronas com Redis.
- Migrations SQL para Supabase/Postgres com tabelas de assinantes, livros, lições, pagamentos e entregas.
- Scripts para aplicar migrations e validar o schema esperado.
- Pasta `Livros/` usada como fonte interna de curadoria. Os PDFs não são distribuídos pela aplicação.

## Stack

### Frontend

- React 18
- Vite
- Tailwind CSS
- React Query
- Axios
- Lucide React

### Backend

- Python 3
- FastAPI
- Uvicorn
- Pydantic Settings
- Supabase client
- Redis + Arq
- Psycopg

### Infra e dados

- Docker Compose para desenvolvimento local
- Supabase/Postgres para dados e migrations
- Redis para fila de tarefas
- Cakto, Resend, Evolution API e Gemini configurados por variáveis de ambiente

## Estrutura

```text
backend/      API FastAPI, repositórios, schemas, workers e scripts
frontend/     Landing page React/Vite
supabase/     Migrations SQL do banco
Livros/       PDFs internos para curadoria e geração de conteúdo
Planos MD/    Documentos de planejamento e copy
```

## Configuração

Copie o arquivo de exemplo e preencha as variáveis necessárias:

```bash
cp .env.example .env
```

Variáveis principais:

```text
VITE_API_BASE_URL=http://localhost:8000/api
VITE_CAKTO_CHECKOUT_URL=
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
DIRECT_URL=
REDIS_URL=redis://redis:6379/0
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
CAKTO_CHECKOUT_URL=
CAKTO_WEBHOOK_SECRET=
RESEND_API_KEY=
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
```

Para rodar apenas a landing page, `VITE_CAKTO_CHECKOUT_URL` é suficiente para direcionar os botões de compra. Para usar health check do Supabase, scripts de migration e futuras rotas de dados, configure as credenciais do Supabase/Postgres.

## Execução com Docker

Suba todos os serviços:

```bash
docker compose up --build
```

Serviços locais:

```text
Frontend:        http://localhost:5173
Backend:         http://localhost:8000
Health:          http://localhost:8000/api/health
Supabase health: http://localhost:8000/api/health/supabase
Redis:           localhost:6379
```

## Execução sem Docker

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Worker:

```bash
cd backend
arq app.workers.arq_settings.WorkerSettings
```

## Banco de dados

As migrations ficam em `supabase/migrations`.

Para aplicar migrations usando `DIRECT_URL` ou `DATABASE_URL`:

```bash
cd backend
python scripts/apply_migrations.py
```

Para conferir se o schema esperado está presente:

```bash
cd backend
python scripts/verify_schema.py
```

Tabelas esperadas atualmente:

```text
schema_migrations
subscribers
books
lessons
lesson_quotes
subscriptions
payment_events
deliveries
delivery_parts
```

## Rotas disponíveis

```text
GET /api/health
GET /api/health/supabase
```

## Scripts úteis

Frontend:

```bash
npm run dev
npm run build
npm run preview
npm run lint
```

Backend:

```bash
uvicorn app.main:app --reload
python scripts/apply_migrations.py
python scripts/verify_schema.py
python scripts/process_book.py --slug habitos-atomicos --dry-run
python scripts/process_book.py --slug habitos-atomicos
python scripts/send_lesson_email.py --to seu-email@exemplo.com --dry-run
python scripts/send_lesson_email.py --to seu-email@exemplo.com
python scripts/send_lesson_email.py --lesson-id UUID_DA_LICAO --active-subscribers
arq app.workers.arq_settings.WorkerSettings
```

Processamento de livros:

- Os PDFs ficam em `Livros/`.
- Os metadados ficam em `Livros/metadata.json`.
- `--dry-run` gera a microlicao com Gemini sem salvar no Supabase.
- Sem `--dry-run`, o script cria/atualiza o livro e salva a microlicao como `review`.

Envio por email:

- Configure `RESEND_API_KEY` e `RESEND_FROM_EMAIL`.
- O template usado fica em `backend/app/templates/emails/templateFull.html`.
- `--dry-run` renderiza o HTML sem enviar.
- `--to` envia um email de teste.
- `--lesson-id ... --active-subscribers` envia a licao para assinantes com assinatura `active` e email habilitado.

## Observações

- O checkout é externo e deve ser configurado via Cakto.
- As entregas por e-mail e WhatsApp dependem das credenciais de Resend e Evolution API.
- A geração/apoio com IA usa Gemini e depende de `GEMINI_API_KEY`. O modelo padrão é `gemini-3.5-flash`.
- A pasta `Livros/` é material interno de curadoria; a aplicação não deve expor ou redistribuir os PDFs.
