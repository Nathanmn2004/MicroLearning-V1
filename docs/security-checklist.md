# Checklist de seguranca e conformidade

## Secrets e arquivos sensiveis

- `.env` e variantes locais estao ignorados por `.gitignore`.
- `.env.example` pode ser versionado porque contem apenas nomes de variaveis e valores vazios/exemplos.
- PDFs em `Livros/` nao devem ser commitados nem servidos pelo frontend.
- `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, `GEMINI_API_KEY`, `CAKTO_WEBHOOK_SECRET` e chaves equivalentes devem existir apenas em variaveis de ambiente de producao.

## Webhooks e pagamentos

- `CAKTO_WEBHOOK_SECRET` deve estar configurado em producao.
- Em producao, o webhook da Cakto sem segredo configurado deve ser rejeitado.
- Eventos duplicados devem continuar sendo deduplicados por `provider_event_id`.
- Eventos de cancelamento, reembolso e chargeback devem cancelar entregas pendentes.

## Conteudo e direitos autorais

- O produto deve entregar sinteses educacionais autorais, nao PDFs, capitulos ou livros completos.
- Citacoes literais devem ser curtas e contextualizadas.
- O processamento de livro descarta citacoes acima de 90 caracteres.
- Citacoes salvas como verificadas precisam aparecer no texto extraido do PDF.
- O frontend, a pagina de obrigado e o rodape devem comunicar que livros completos e PDFs nao sao distribuidos.

## Dados pessoais e suporte

- Dados de assinantes devem ser usados apenas para ativacao, suporte e entrega das microlicoes.
- O suporte deve conseguir corrigir e-mail/telefone informado incorretamente no checkout.
- Cancelamentos e reembolsos vindos da Cakto devem bloquear novas entregas.

## Validacoes antes de producao

- Testar `POST /api/webhooks/cakto` sem segredo em ambiente de producao.
- Testar `POST /api/webhooks/cakto` com segredo incorreto.
- Testar `POST /api/webhooks/cakto` com segredo correto.
- Confirmar que o backend de producao nao expoe a pasta `Livros/`.
- Confirmar que o worker de envio usa apenas assinaturas ativas.
