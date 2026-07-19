# Plano inicial - etapas de execução

Este documento substitui a ideia de uma plataforma administrativa completa por um MVP mais direto:

```text
Usuário acessa landing page
  -> entende a oferta
  -> escolhe uma trilha de livros ou escolhe receber todos
  -> clica em comprar
  -> vai para o checkout da Cakto
  -> pagamento/assinatura é confirmado por webhook
  -> sistema registra o assinante
  -> usuário recebe microlições da trilha escolhida por WhatsApp e/ou e-mail
```

O objetivo inicial não é criar uma área administrativa complexa, biblioteca pública, editor visual ou dashboard. O objetivo é vender uma assinatura e entregar conteúdos curtos baseados em livros selecionados, respeitando a trilha de interesse escolhida pelo assinante.

---

## Status atual para colocar em execução

Esta seção registra o que já foi feito no projeto e o que ainda falta antes de considerar o fluxo pronto para rodar em produção.

### Já foi feito

- Landing page já possui seletor de trilha com quatro opções: `todos`, `mente-desenvolvimento-pessoal`, `carreira-negocios-dinheiro` e `historia-sociedade`.
- CTAs da landing já apontam para o checkout correto da Cakto conforme a trilha selecionada.
- Página `/obrigado` já foi criada no frontend e o rewrite da Vercel para SPA já foi configurado.
- Checkouts da Cakto já foram registrados nos arquivos de configuração de exemplo:
  - `todos`: `https://pay.cakto.com.br/qgza2fd_977495`;
  - `mente-desenvolvimento-pessoal`: `https://pay.cakto.com.br/qgza2fd_989199`;
  - `carreira-negocios-dinheiro`: `https://pay.cakto.com.br/qgza2fd_989202`;
  - `historia-sociedade`: `https://pay.cakto.com.br/qgza2fd_989204`.
- `.env` principal da raiz foi atualizado localmente com as variáveis faltantes das trilhas e do agendador.
- PDFs foram reorganizados em subpastas por trilha dentro de `Livros/`.
- `Livros/metadata.json` foi atualizado com `content_track` e caminho dos arquivos nas subpastas.
- Migration `0006_content_tracks.sql` foi criada para adicionar `content_track` em `subscribers`, `books` e `lessons`, com constraints, índices e fallback para `todos`.
- Migration de trilhas já foi aplicada no banco configurado localmente.
- Schemas do backend foram atualizados para expor `content_track` em assinantes, livros e lições.
- Webhook da Cakto já tenta inferir a trilha por `content_track`, URL de checkout, oferta, produto ou identificadores que contenham os IDs dos checkouts.
- Backend já evita sobrescrever uma trilha específica com fallback `todos`.
- `process_book.py` já aceita trilha, lê PDFs nas subpastas e salva livros/lições com `content_track`.
- Agendador já filtra a próxima lição pela trilha do assinante.
- Assinantes com `todos` já podem receber lições de qualquer trilha.
- Script de envio manual por e-mail já respeita a trilha do assinante.
- Template de e-mail já foi ajustado para lições longas e tópicos completos.
- Validações locais já executadas: build do frontend, compilação dos módulos Python alterados, verificação de schema, teste dos IDs de checkout no webhook e dry-run do agendador.
- Checklist de segurança/conformidade já foi criada em `docs/security-checklist.md`.

### Ainda falta para executar em produção

- Fazer commit e push das alterações atuais de trilhas, landing page, migrations, exemplos de `.env` e reorganização dos PDFs.
- Configurar no Render ou na VPS as novas variáveis do backend:
  - `CAKTO_CHECKOUT_URL`;
  - `CAKTO_CHECKOUT_URL_MENTE_DESENVOLVIMENTO_PESSOAL`;
  - `CAKTO_CHECKOUT_URL_CARREIRA_NEGOCIOS_DINHEIRO`;
  - `CAKTO_CHECKOUT_URL_HISTORIA_SOCIEDADE`;
  - `CONTENT_DELIVERY_FREQUENCY`;
  - `CONTENT_DELIVERY_TIME`;
  - `CONTENT_DELIVERY_TIMEZONE`;
  - `CONTENT_DELIVERY_CHANNELS`;
  - `CONTENT_DELIVERY_LESSON_STATUSES`;
  - `CONTENT_DELIVERY_BATCH_LIMIT`;
  - `GENERATED_LESSON_STATUS`;
  - `VALID_CONTENT_TRACKS`.
- Configurar na Vercel as novas variáveis do frontend:
  - `VITE_CAKTO_CHECKOUT_URL`;
  - `VITE_CAKTO_CHECKOUT_URL_MENTE_DESENVOLVIMENTO_PESSOAL`;
  - `VITE_CAKTO_CHECKOUT_URL_CARREIRA_NEGOCIOS_DINHEIRO`;
  - `VITE_CAKTO_CHECKOUT_URL_HISTORIA_SOCIEDADE`.
- Fazer novo deploy do frontend depois de configurar as variáveis `VITE_*`, porque elas entram no build.
- Fazer novo deploy do backend depois de configurar as variáveis de trilha e agendamento.
- Confirmar na Cakto se os quatro checkouts estão apontando para o webhook correto do backend.
- Confirmar na Cakto se os quatro checkouts redirecionam para `/obrigado` após a compra, quando essa configuração estiver disponível.
- Confirmar que o payload real da Cakto contém URL, oferta, produto ou outro identificador suficiente para o backend inferir a trilha.
- Rodar um teste real ou simulado de webhook para cada checkout: `todos`, `mente-desenvolvimento-pessoal`, `carreira-negocios-dinheiro` e `historia-sociedade`.
- Conferir no Supabase se cada assinante criado pelo webhook fica com `content_track` correto.
- Processar ou revisar microlições suficientes em cada trilha, garantindo que existam lições com status liberado para envio.
- Fazer um envio de teste por e-mail para um assinante de cada trilha e para um assinante `todos`.
- Validar que um assinante de uma trilha não recebe lição exclusiva de outra trilha.
- Configurar a execução recorrente do agendador no ambiente escolhido, seja Render, VPS, cron ou worker.
- Decidir se o lançamento inicial será somente por e-mail. Se WhatsApp fizer parte da promessa de venda no lançamento, a Etapa 8 ainda precisa ser implementada e testada antes de abrir para clientes.
- Monitorar os primeiros envios reais e conferir registros em `deliveries`.

### Bloqueadores reais antes de vender

1. Deploy das alterações atuais ainda precisa acontecer.
2. Variáveis novas precisam ser configuradas nos ambientes de produção.
3. Webhook real da Cakto precisa ser validado com os quatro checkouts.
4. É necessário ter microlições aprovadas suficientes em cada trilha.
5. O agendador precisa estar rodando de forma recorrente no ambiente de produção.
6. WhatsApp ainda não deve ser prometido como canal ativo enquanto a Etapa 8 não estiver pronta.

### Ordem recomendada a partir de agora

1. Commit e push do estado atual.
2. Configurar variáveis na Vercel e no backend de produção.
3. Fazer deploy do frontend e backend.
4. Aplicar ou confirmar migration `0006_content_tracks.sql` no Supabase de produção.
5. Configurar webhooks e redirects dos quatro checkouts na Cakto.
6. Processar microlições por trilha.
7. Criar assinantes de teste por webhook para cada checkout.
8. Rodar envio manual por e-mail para cada trilha.
9. Ativar agendamento recorrente.
10. Liberar venda somente depois do teste completo compra -> webhook -> assinante com trilha -> lição filtrada -> e-mail entregue.

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
13. A pasta `Livros/` será organizada em subpastas por trilha de conteúdo.
14. As citações literais serão curtas, limitadas e sempre contextualizadas.
15. O processamento de livros pode começar como rotina interna, sem painel administrativo.
16. O usuário poderá escolher uma das três trilhas ou a opção `todos`.
17. A preferência de trilha ficará registrada no assinante.
18. O agendamento selecionará apenas microlições compatíveis com a trilha escolhida.
19. A opção `todos` permite receber microlições de qualquer trilha.
20. A escolha da trilha deve ser capturada antes do checkout e precisa chegar ao backend pelo webhook, parâmetro rastreável ou mapeamento de oferta/produto.

**Trilhas de conteúdo:**

1. `mente-desenvolvimento-pessoal` - Mente & Desenvolvimento Pessoal: psicologia, hábitos, produtividade, inteligência emocional e autoajuda em geral. O "como viver melhor".
2. `carreira-negocios-dinheiro` - Carreira, Negócios & Dinheiro: liderança, empreendedorismo, marketing, investimentos e educação financeira. O lado profissional/prático da vida.
3. `historia-sociedade` - História & Sociedade: grandes eventos históricos, biografias, política, cultura, guerras e civilizações. O "como chegamos até aqui".
4. `todos` - mistura todas as trilhas disponíveis.

**Organização proposta dos PDFs:**

```text
Livros/
  metadata.json
  mente-desenvolvimento-pessoal/
  carreira-negocios-dinheiro/
  historia-sociedade/
```

**Mapeamento inicial sugerido:**

1. Mente & Desenvolvimento Pessoal: `habitos`, `produtividade`, `desenvolvimento-pessoal`, `comunicacao`, `filosofia`.
2. Carreira, Negócios & Dinheiro: `negocios`, `financas`, `estrategia`.
3. História & Sociedade: `historia`, `ciencia`, `tecnologia`.

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
10. Incluir seletor de trilha antes do checkout:
    - Mente & Desenvolvimento Pessoal;
    - Carreira, Negócios & Dinheiro;
    - História & Sociedade;
    - Todos.
11. Explicar que a escolha define a curadoria das microlições recebidas.
12. Criar botão principal de compra.
13. Redirecionar o botão para o checkout correto, preservando a trilha escolhida.
14. Preparar responsividade mobile.

**Entregável:** landing page funcional com CTA de compra e seleção de trilha.

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

1. `subscribers` - comprador/assinante vindo da Cakto, incluindo a trilha escolhida.
2. `subscriptions` - status da assinatura.
3. `payment_events` - eventos recebidos da Cakto.
4. `books` - livros internos disponíveis para curadoria, incluindo trilha de conteúdo.
5. `lessons` - microlições prontas para envio, herdando a trilha do livro.
6. `lesson_quotes` - citações curtas e verificadas.
7. `deliveries` - envios por WhatsApp e e-mail.
8. `delivery_parts` - partes de uma entrega longa, principalmente WhatsApp.

**Tarefas:**

1. Criar migration SQL versionada.
2. Criar índices por e-mail, telefone, status, canal e data.
3. Registrar eventos duplicados sem processar duas vezes.
4. Criar camada de acesso direto ao Supabase.
5. Manter dados sensíveis fora de arquivos versionados.
6. Adicionar campo `content_track` em `subscribers`.
7. Adicionar campo `content_track` em `books` e/ou `lessons`.
8. Criar índice para seleção de microlições por trilha e status.
9. Definir valor padrão `todos` para assinantes sem preferência.

**Entregável:** schema do banco pronto para checkout, entrega e curadoria por trilha.

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
8. Definir como a trilha escolhida chegará ao webhook:
   - parâmetro customizado no checkout;
   - oferta/produto diferente por trilha;
   - ou URL de checkout diferente por trilha.
9. Configurar URLs/identificadores por trilha se a Cakto não repassar parâmetros customizados.

**Checkouts configurados:**

1. `todos` - Checkout Principal - Todos os temas: `https://pay.cakto.com.br/qgza2fd_977495`.
2. `mente-desenvolvimento-pessoal` - Checkout - Mente e Desenvolvimento Pessoal: `https://pay.cakto.com.br/qgza2fd_989199`.
3. `carreira-negocios-dinheiro` - Checkout - Carreira e Negócios: `https://pay.cakto.com.br/qgza2fd_989202`.
4. `historia-sociedade` - Checkout - Historia e Sociedade: `https://pay.cakto.com.br/qgza2fd_989204`.

**Entregável:** clique em comprar leva o usuário para o checkout da Cakto mantendo a trilha escolhida.

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
9. Extrair ou inferir a trilha de conteúdo escolhida.
10. Salvar `content_track` no assinante.
11. Preservar `todos` quando a trilha não vier no payload.

**Entregável:** assinante fica ativo/inativo automaticamente conforme a Cakto e com trilha de conteúdo registrada.

---

## Etapa 6 - Conteúdo dos livros

**Objetivo:** transformar livros internos em microlições entregáveis.

**Tarefas:**

1. Manter PDFs em `Livros/`.
2. Organizar PDFs nas subpastas da trilha correspondente.
3. Criar `Livros/metadata.json` com título, autor, categoria, trilha e arquivo.
4. Criar rotina interna para processar um livro.
5. Extrair texto com PyMuPDF.
6. Limpar texto.
7. Dividir em blocos.
8. Analisar com Gemini.
9. Criar mapa geral do livro.
10. Gerar microlição curta.
11. Validar citações literais curtas contra o texto original.
12. Salvar microlição pronta em `lessons` com a trilha correta.
13. Permitir processar livros por slug ou por trilha.

**Observação:** no MVP, essa rotina pode ser operada pelo desenvolvedor, sem painel administrativo.

**Entregável:** microlições prontas no banco para envio e classificadas por trilha.

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
4. Ler a trilha escolhida em `subscribers.content_track`.
5. Selecionar próxima microlição compatível com a trilha.
6. Para `todos`, permitir qualquer trilha disponível.
7. Evitar enviar a mesma lição duas vezes para a mesma pessoa.
8. Criar registros de entrega.
9. Executar envios por canal.
10. Registrar falhas.

**Entregável:** rotina recorrente de envio filtrada pela trilha do assinante.

---

## Etapa 10 - Página de obrigado e suporte

**Objetivo:** melhorar a experiência depois da compra.

**Tarefas:**

1. Criar página `/obrigado`.
2. Explicar que o pagamento será confirmado pela Cakto.
3. Informar que o conteúdo chegará por WhatsApp/e-mail.
4. Incluir orientação de suporte.
5. Incluir aviso para conferir dados informados no checkout.
6. Reforçar qual trilha foi escolhida, se essa informação estiver disponível no retorno da Cakto.

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
11. Garantir que a escolha de trilha não exponha PDFs ou caminhos internos.
12. Garantir que a trilha não possa liberar conteúdo para assinatura inativa.

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
13. Testar cada trilha de conteúdo.
14. Testar opção `todos`.
15. Testar assinante sem trilha definida, usando fallback `todos`.
16. Testar se assinante de uma trilha não recebe lição exclusiva de outra trilha.

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
14. Configurar checkout/URLs/ofertas por trilha.
15. Confirmar que o webhook registra `content_track`.
16. Confirmar que o worker envia conteúdos da trilha correta.

**Entregável:** landing vendendo e entrega funcionando.

---

## Alterações necessárias para trilhas de livros

**Objetivo:** adaptar o projeto atual para que o assinante receba conteúdos da trilha escolhida.

1. `Livros/`
   - Criar subpastas `mente-desenvolvimento-pessoal/`, `carreira-negocios-dinheiro/` e `historia-sociedade/`.
   - Mover cada PDF para a subpasta correta.
   - Atualizar `Livros/metadata.json` para incluir `content_track` e caminho relativo com subpasta.

2. Supabase
   - Criar migration para adicionar `content_track` em `subscribers`.
   - Criar migration para adicionar `content_track` em `books` e, se necessário, em `lessons`.
   - Criar índices para buscar próximas lições por `status`, `content_track` e data.
   - Definir fallback `todos` para assinantes antigos.

3. Backend
   - Atualizar schemas de assinante, livros e lições.
   - Atualizar webhook da Cakto para extrair a trilha escolhida.
   - Atualizar `process_book.py` para ler PDFs nas subpastas e salvar a trilha.
   - Atualizar o agendador para filtrar lições pela trilha do assinante.
   - Garantir que `todos` continue funcionando como mistura de todas as trilhas.

4. Frontend
   - Adicionar seletor de trilha na landing.
   - Ajustar CTAs para levar a trilha escolhida ao checkout.
   - Explicar o que cada trilha entrega.
   - Validar mobile.

5. Cakto
   - Decidir se haverá um checkout único com parâmetro customizado ou uma oferta/URL por trilha.
   - Garantir que o webhook entregue informação suficiente para o backend persistir `content_track`.
   - Testar compra para cada trilha e para `todos`.

6. Operação
   - Reprocessar ou revisar livros já cadastrados para preencher `content_track`.
   - Conferir se lições antigas entram no filtro correto.
   - Rodar envio de teste por trilha antes de liberar em produção.

---

## Primeira fatia vertical recomendada

Implementar primeiro:

1. Landing page.
2. Seletor de trilha na landing.
3. Botão para checkout da Cakto preservando a trilha.
4. Webhook da Cakto registrando `content_track`.
5. Registro de assinante ativo no Supabase.
6. Uma microlição manual cadastrada no banco com trilha.
7. Envio manual de teste por e-mail filtrado pela trilha.
8. Envio manual de teste por WhatsApp.

Essa fatia valida o essencial: vender, ativar e entregar.

---

## Critérios finais do MVP

O MVP estará pronto quando:

1. A landing page estiver publicada.
2. O botão de compra redirecionar para o checkout da Cakto.
3. O usuário conseguir escolher uma trilha ou `todos`.
4. A Cakto enviar webhooks para o backend.
5. O backend registrar assinantes, assinaturas e `content_track`.
6. Somente assinantes ativos receberem conteúdo.
7. Existirem microlições prontas para envio em cada trilha.
8. O agendador respeitar a trilha escolhida.
9. O Resend enviar e-mails.
10. A Evolution API enviar WhatsApp.
11. Os envios ficarem registrados.
12. O fluxo completo compra -> escolha de trilha -> ativação -> entrega estiver testado.
