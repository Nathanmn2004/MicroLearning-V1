# MicroAprendizagem

Landing page e backend mínimo para vender uma assinatura de microlições baseadas em livros selecionados.

## Estrutura inicial

```text
backend/   API FastAPI para health checks, webhooks e entregas
frontend/  Landing page React com CTA para checkout da Cakto
Livros/    PDFs internos usados para curadoria e geração de microlições
Planos MD/ Documentos de planejamento
```

## Execução local

1. Copie `.env.example` para `.env`.
2. Preencha as chaves necessárias.
3. Suba os serviços:

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

Configure `VITE_CAKTO_CHECKOUT_URL` para apontar o botão de compra para o checkout da Cakto.
