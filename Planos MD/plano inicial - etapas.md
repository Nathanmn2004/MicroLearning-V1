# Plano inicial - etapas de execução

Este documento substitui a ideia de uma plataforma administrativa completa por um MVP mais direto:

```text
Usuário acessa landing page
  -> entende a oferta
  -> clica em comprar
  -> vai para o checkout da Cakto
  -> pagamento/assinatura é confirmado por webhook
  -> sistema registra o assinante
  -> usuário recebe microlições por WhatsApp e/ou e-mail
```

O objetivo inicial não é criar uma área administrativa complexa, biblioteca pública, editor visual ou dashboard. O objetivo é vender uma assinatura e entregar conteúdos curtos baseados em livros selecionados.

---

## Etapa 0 - Decisões do MVP

**Objetivo:** deixar o escopo simples e coerente com o produto que será vendido.

**Decisões definidas:**

1. O site principal será uma landing page em `https://microaprendizagem.com.br`.
2. O botão de compra redirecionará para o checkout da Cakto.
3. A URL do checkout ficará em variável de ambiente ou configuração simples.
4. O backend ficará em `https://api.microaprendizagem.com.br`.
5. A Cakto será responsável por checkout, pagamento e assinatura.
6. O backend receberá webhooks da Cakto para ativar, renovar, cancelar ou bloquear assinantes.
7. O usuário não precisa criar conta no MVP.
8. O usuário receberá os conteúdos por WhatsApp e/ou e-mail.
9. A integração com banco será direta com Supabase.
10. Gemini será o provedor inicial de IA.
11. Grok ficará para fase posterior.
12. A pasta `Livros/` continuará sendo a fonte dos PDFs internos.
13. Novos livros poderão ser adicionados manualmente na pasta `Livros/`.
14. As citações literais serão curtas, limitadas e sempre contextualizadas.
15. O processamento de livros pode começar como rotina interna, sem painel administrativo.

**Fila assíncrona:**

Fila assíncrona é o mecanismo para executar tarefas demoradas em segundo plano.

No MVP, ela será usada somente quando necessário para:

1. processar livros;
2. chamar a IA;
3. preparar microlições;
4. enviar e-mails;
5. enviar mensagens no WhatsApp;
6. reprocessar falhas.

**Entregável:** escopo confirmado e variáveis de ambiente mínimas definidas.

---

## Etapa 1 - Landing page de venda

**Objetivo:** criar uma página pública que convença o visitante a comprar.

**Tarefas:**

1. Criar frontend com React, Vite e Tailwind CSS.
2. Criar primeira tela focada na oferta, não em dashboard.
3. Explicar claramente o que o usuário recebe.
4. Mostrar benefícios: aprendizado rápido, curadoria de livros, envio automático, leitura em poucos minutos.
5. Mostrar exemplos de conteúdos que serão enviados.
6. Mostrar canais de entrega: WhatsApp e e-mail.
7. Mostrar frequência prometida de envio.
8. Incluir seção de prova/autoridade ou explicação do método.
9. Incluir perguntas frequentes.
10. Criar botão principal de compra.
11. Redirecionar o botão para `CAKTO_CHECKOUT_URL` ou `VITE_CAKTO_CHECKOUT_URL`.
12. Preparar responsividade mobile.

**Entregável:** landing page funcional com CTA de compra.

---

## Etapa 2 - Backend mínimo

**Objetivo:** criar somente a API necessária para webhooks, saúde do sistema e entregas.

**Tarefas:**

1. Criar backend com FastAPI.
2. Configurar CORS para `microaprendizagem.com.br`.
3. Criar endpoint `GET /api/health`.
4. Criar endpoint `GET /api/health/supabase`.
5. Configurar logs básicos.
6. Configurar variáveis de ambiente.
7. Criar estrutura para webhooks.
8. Criar estrutura para tarefas assíncronas.

**Entregável:** backend simples, sem área administrativa.

---

## Etapa 3 - Banco de dados no Supabase

**Objetivo:** armazenar assinantes, pagamentos, livros, microlições e envios.

**Tabelas principais:**

1. `subscribers` - comprador/assinante vindo da Cakto.
2. `subscriptions` - status da assinatura.
3. `payment_events` - eventos recebidos da Cakto.
4. `books` - livros internos disponíveis para curadoria.
5. `lessons` - microlições prontas para envio.
6. `lesson_quotes` - citações curtas e verificadas.
7. `deliveries` - envios por WhatsApp e e-mail.
8. `delivery_parts` - partes de uma entrega longa, principalmente WhatsApp.

**Tarefas:**

1. Criar migration SQL versionada.
2. Criar índices por e-mail, telefone, status, canal e data.
3. Registrar eventos duplicados sem processar duas vezes.
4. Criar camada de acesso direto ao Supabase.
5. Manter dados sensíveis fora de arquivos versionados.

**Entregável:** schema do banco pronto para checkout e entrega.

---

## Etapa 4 - Checkout Cakto

**Objetivo:** mandar o visitante da landing page para o checkout correto.

**Tarefas:**

1. Criar produto/oferta na Cakto.
2. Obter URL pública do checkout.
3. Configurar `CAKTO_CHECKOUT_URL` no backend.
4. Configurar `VITE_CAKTO_CHECKOUT_URL` no frontend.
5. Fazer o botão de compra abrir o checkout.
6. Validar que o checkout recebe o produto correto.
7. Definir página de obrigado ou pós-compra, se a Cakto permitir redirect.

**Entregável:** clique em comprar leva o usuário para o checkout da Cakto.

---

## Etapa 5 - Webhook da Cakto

**Objetivo:** ativar ou bloquear assinantes automaticamente após eventos da Cakto.

**Eventos iniciais:**

1. `initiate_checkout` - registrar interesse, sem liberar acesso.
2. `checkout_abandonment` - registrar abandono, sem liberar acesso.
3. `purchase_approved` - liberar acesso quando aplicável.
4. `purchase_refused` - registrar recusa, sem liberar acesso.
5. `subscription_created` - criar assinatura.
6. `subscription_renewed` - manter assinatura ativa.
7. `subscription_renewal_refused` - marcar como pendente/inadimplente.
8. `subscription_canceled` - cancelar assinatura.
9. `refund` - bloquear acesso.
10. `chargeback` - bloquear acesso.

**Tarefas:**

1. Criar endpoint `POST /api/webhooks/cakto`.
2. Validar segredo ou assinatura do webhook.
3. Salvar payload bruto em `payment_events`.
4. Evitar processamento duplicado.
5. Extrair e-mail, telefone, nome, produto e identificadores da Cakto.
6. Criar ou atualizar assinante.
7. Criar ou atualizar assinatura.
8. Bloquear entregas quando a assinatura não estiver ativa.

**Entregável:** assinante fica ativo/inativo automaticamente conforme a Cakto.

---

## Etapa 6 - Conteúdo dos livros

**Objetivo:** transformar livros internos em microlições entregáveis.

**Tarefas:**

1. Manter PDFs em `Livros/`.
2. Criar `Livros/metadata.json` com título, autor, categoria e arquivo.
3. Criar rotina interna para processar um livro.
4. Extrair texto com PyMuPDF.
5. Limpar texto.
6. Dividir em blocos.
7. Analisar com Gemini.
8. Criar mapa geral do livro.
9. Gerar microlição curta.
10. Validar citações literais curtas contra o texto original.
11. Salvar microlição pronta em `lessons`.

**Observação:** no MVP, essa rotina pode ser operada pelo desenvolvedor, sem painel administrativo.

**Entregável:** microlições prontas no banco para envio.

---

## Etapa 7 - Entrega por e-mail

**Objetivo:** enviar microlições para assinantes ativos por Resend.

**Tarefas:**

1. Criar provider do Resend.
2. Criar template HTML responsivo.
3. Converter microlição para HTML.
4. Enviar e-mail de teste.
5. Enviar microlição para assinantes ativos.
6. Registrar entrega em `deliveries`.
7. Processar webhook do Resend, se necessário.
8. Repetir envio em caso de falha temporária.

**Entregável:** assinante ativo recebe microlição por e-mail.

---

## Etapa 8 - Entrega por WhatsApp

**Objetivo:** enviar microlições para assinantes ativos por Evolution API.

**Tarefas:**

1. Criar provider da Evolution API.
2. Formatar microlição para WhatsApp.
3. Dividir conteúdo em partes.
4. Evitar cortar frases.
5. Evitar separar citação da explicação.
6. Controlar intervalo entre mensagens.
7. Registrar cada envio.
8. Processar webhook/status da Evolution API, se disponível.
9. Repetir envio em caso de falha temporária.

**Entregável:** assinante ativo recebe microlição por WhatsApp.

---

## Etapa 9 - Agendamento de conteúdos

**Objetivo:** enviar conteúdos de forma recorrente conforme a promessa da oferta.

**Tarefas:**

1. Definir frequência de envio.
2. Definir horário padrão de envio.
3. Selecionar assinantes ativos.
4. Selecionar próxima microlição.
5. Evitar enviar a mesma lição duas vezes para a mesma pessoa.
6. Criar registros de entrega.
7. Executar envios por canal.
8. Registrar falhas.

**Entregável:** rotina recorrente de envio.

---

## Etapa 10 - Página de obrigado e suporte

**Objetivo:** melhorar a experiência depois da compra.

**Tarefas:**

1. Criar página `/obrigado`.
2. Explicar que o pagamento será confirmado pela Cakto.
3. Informar que o conteúdo chegará por WhatsApp/e-mail.
4. Incluir orientação de suporte.
5. Incluir aviso para conferir dados informados no checkout.

**Entregável:** fluxo pós-checkout mais claro.

---

## Etapa 11 - Segurança e conformidade

**Objetivo:** proteger chaves, PDFs e uso de conteúdo.

**Tarefas:**

1. Manter PDFs fora do acesso público.
2. Não servir PDF diretamente ao usuário.
3. Validar webhooks.
4. Não confiar apenas no e-mail do payload.
5. Usar identificadores da Cakto quando disponíveis.
6. Limitar citações literais.
7. Não reproduzir capítulos inteiros.
8. Identificar obra e autor.
9. Informar que o conteúdo é uma síntese educacional.
10. Manter `SUPABASE_SERVICE_ROLE_KEY` fora de arquivos versionados.

**Entregável:** checklist de segurança do MVP.

---

## Etapa 12 - Testes

**Objetivo:** validar o fluxo real que gera receita e entrega valor.

**Tarefas:**

1. Testar landing page no mobile e desktop.
2. Testar clique para checkout.
3. Testar webhook da Cakto.
4. Testar compra aprovada.
5. Testar assinatura cancelada.
6. Testar reembolso e chargeback.
7. Testar envio por e-mail.
8. Testar envio por WhatsApp.
9. Testar usuário sem telefone.
10. Testar usuário sem e-mail.
11. Testar assinatura inativa.
12. Testar duplicidade de webhook.

**Entregável:** fluxo principal validado de ponta a ponta.

---

## Etapa 13 - Deploy e lançamento

**Objetivo:** colocar o MVP em produção.

**Tarefas:**

1. Publicar frontend em `https://microaprendizagem.com.br`.
2. Publicar backend em `https://api.microaprendizagem.com.br`.
3. Configurar Supabase de produção.
4. Configurar variáveis de produção.
5. Configurar URL do checkout Cakto.
6. Configurar webhook da Cakto.
7. Configurar Resend.
8. Configurar Evolution API.
9. Processar primeiras microlições.
10. Fazer compra de teste.
11. Confirmar ativação do assinante.
12. Confirmar entrega por e-mail.
13. Confirmar entrega por WhatsApp.

**Entregável:** landing vendendo e entrega funcionando.

---

## Primeira fatia vertical recomendada

Implementar primeiro:

1. Landing page.
2. Botão para checkout da Cakto.
3. Webhook da Cakto.
4. Registro de assinante ativo no Supabase.
5. Uma microlição manual cadastrada no banco.
6. Envio manual de teste por e-mail.
7. Envio manual de teste por WhatsApp.

Essa fatia valida o essencial: vender, ativar e entregar.

---

## Critérios finais do MVP

O MVP estará pronto quando:

1. A landing page estiver publicada.
2. O botão de compra redirecionar para o checkout da Cakto.
3. A Cakto enviar webhooks para o backend.
4. O backend registrar assinantes e assinaturas.
5. Somente assinantes ativos receberem conteúdo.
6. Existirem microlições prontas para envio.
7. O Resend enviar e-mails.
8. A Evolution API enviar WhatsApp.
9. Os envios ficarem registrados.
10. O fluxo completo compra -> ativação -> entrega estiver testado.
