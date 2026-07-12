# Plano de Desenvolvimento — Plataforma de Microaprendizagem com IA

## 1. Visão geral

A aplicação será uma plataforma de microaprendizagem baseada em livros previamente selecionados e armazenados no próprio repositório do projeto.

Os usuários finais não poderão enviar livros ou arquivos PDF. Apenas os livros previamente adicionados pelo administrador ou desenvolvedor estarão disponíveis para processamento e distribuição.

O sistema deverá:

* acessar PDFs armazenados no projeto;
* extrair e processar todo o conteúdo textual de cada livro;
* fazer com que a IA analise o livro completo, e não apenas partes isoladas;
* identificar ideias, conceitos, argumentos, exemplos e aprendizados relevantes;
* gerar uma microlição com tempo estimado de leitura de aproximadamente 15 a 20 minutos;
* incluir trechos literais do livro, exatamente como estão escritos no PDF;
* explicar e contextualizar os trechos selecionados;
* adaptar o conteúdo para WhatsApp;
* gerar um e-mail HTML bonito e responsivo;
* enviar conteúdos usando Evolution API e Resend;
* utilizar Supabase como banco de dados;
* controlar o acesso dos usuários conforme o status da assinatura na Cakto.

---

# 2. Objetivo do produto

A plataforma terá como objetivo transformar o conteúdo de livros completos em experiências curtas de aprendizado.

Cada microlição deverá representar uma síntese dos conceitos mais relevantes do livro, permitindo que o usuário compreenda:

* a principal proposta da obra;
* os conceitos fundamentais;
* os principais argumentos apresentados;
* os aprendizados mais úteis;
* exemplos apresentados pelo autor;
* formas práticas de aplicar o conhecimento.

A microlição não deverá ser apenas um resumo superficial do livro.

O sistema deverá realizar um processamento estruturado de todo o texto da obra, compreender a relação entre capítulos e selecionar os conteúdos que melhor representem os ensinamentos do livro.

---

# 3. Escopo inicial

## 3.1 Funcionalidades do administrador

O administrador poderá:

* cadastrar livros disponíveis na plataforma;
* associar um arquivo PDF já existente no projeto;
* iniciar o processamento de um livro;
* acompanhar o status da análise;
* visualizar o texto extraído;
* visualizar capítulos e blocos identificados;
* gerar uma microlição;
* editar a microlição;
* revisar os trechos literais selecionados;
* aprovar uma microlição;
* cadastrar ou visualizar usuários;
* visualizar o status de assinatura de cada usuário;
* acompanhar envios por WhatsApp;
* acompanhar envios por e-mail;
* visualizar erros de processamento ou entrega.

---

## 3.2 Funcionalidades do usuário

O usuário poderá:

* criar uma conta;
* contratar uma assinatura pela Cakto;
* escolher receber conteúdos por WhatsApp, e-mail ou ambos;
* informar telefone e e-mail;
* definir preferências de recebimento;
* visualizar o status da assinatura;
* receber microlições somente enquanto a assinatura estiver ativa;
* cancelar o recebimento;
* atualizar seus dados e preferências.

---

## 3.3 Funcionalidades fora do MVP

Inicialmente, não serão incluídos:

* upload de PDFs por usuários;
* biblioteca aberta para envio de documentos;
* aplicativo mobile;
* comentários;
* comunidade;
* ranking;
* gamificação;
* certificados;
* áudio;
* vídeos;
* chat com o livro;
* geração de imagens;
* marketplace de livros;
* planos corporativos;
* recomendação personalizada por IA.

---

# 4. Tecnologias principais

## Backend

* FastAPI;
* Python;
* SQLAlchemy ou integração direta com Supabase;
* Pydantic;
* Celery, Dramatiq ou Arq para tarefas assíncronas;
* Redis para filas e cache;
* PyMuPDF para leitura dos PDFs.

## Frontend

* React JS;
* Vite;
* React Router;
* Axios ou Fetch API;
* Tailwind CSS;
* TanStack Query;
* editor Markdown ou rich text para revisão das lições.

## Banco de dados

* Supabase PostgreSQL.

## Autenticação

* Supabase Auth.

## Inteligência artificial inicial

* Gemini;
* Grok como alternativa;
* arquitetura preparada para troca futura de provedor.

## WhatsApp

* Evolution API.

## E-mail

* Resend.

## Pagamentos

* Cakto;
* assinatura mensal;
* verificação de pagamento ativo;
* atualização do status por webhook ou consulta da API disponibilizada pela plataforma.

---

# 5. Funcionamento geral da aplicação

```text
PDF armazenado no projeto
        |
        v
Extração completa do texto
        |
        v
Limpeza e organização
        |
        v
Divisão em capítulos e blocos
        |
        v
Análise de todos os blocos pela IA
        |
        v
Resumo estruturado de cada capítulo
        |
        v
Compreensão geral do livro
        |
        v
Seleção dos principais ensinamentos
        |
        v
Seleção de trechos literais
        |
        v
Geração da microlição
        |
        v
Revisão e aprovação
        |
        v
Envio por Evolution API ou Resend
```

---

# 6. Armazenamento dos PDFs

Os PDFs não serão enviados pelos usuários.

Eles estarão armazenados dentro do próprio projeto ou em um diretório privado acessível pelo backend.

Estrutura sugerida:

```text
backend/
├── app/
├── books/
│   ├── habitos_atomicos.pdf
│   ├── o_poder_do_habito.pdf
│   ├── livro_exemplo.pdf
│   └── metadata.json
```

Exemplo do arquivo `metadata.json`:

```json
[
  {
    "id": "habitos-atomicos",
    "title": "Hábitos Atômicos",
    "author": "James Clear",
    "filename": "habitos_atomicos.pdf",
    "category": "Desenvolvimento pessoal",
    "language": "pt-BR",
    "enabled": true
  }
]
```

O banco de dados deverá guardar:

* título;
* autor;
* nome interno do arquivo;
* caminho do PDF;
* categoria;
* descrição;
* quantidade de páginas;
* status do processamento;
* data da última análise;
* versão da análise;
* versão da microlição.

---

# 7. Leitura completa do livro

## 7.1 Regra principal

Todo o conteúdo textual relevante do livro deverá ser processado pela aplicação.

A IA não deverá receber somente o primeiro capítulo, o índice ou algumas páginas aleatórias.

O sistema deverá:

1. extrair o texto de todas as páginas;
2. remover elementos repetitivos;
3. dividir o texto em blocos processáveis;
4. enviar todos os blocos para análise;
5. construir resumos intermediários;
6. relacionar os capítulos;
7. criar uma visão completa do livro;
8. gerar a microlição final somente após o processamento de toda a obra.

---

## 7.2 Limitação de contexto dos modelos

Normalmente, um livro completo não poderá ser enviado em uma única requisição para a IA.

Por isso, a aplicação utilizará uma estratégia hierárquica.

O livro será completamente analisado, porém em diferentes etapas.

```text
Livro completo
   |
   ├── Bloco 1
   ├── Bloco 2
   ├── Bloco 3
   ├── Bloco 4
   └── ...
        |
        v
Análises dos blocos
        |
        v
Análises dos capítulos
        |
        v
Mapa completo do livro
        |
        v
Microlição final
```

Dessa forma, nenhum trecho importante deverá ser ignorado apenas por causa da limitação de tokens do modelo.

---

# 8. Extração do texto dos PDFs

## 8.1 Biblioteca principal

Para o MVP, utilizar:

* PyMuPDF.

Alternativas:

* pypdf;
* pdfplumber.

OCR somente será necessário caso algum PDF seja composto por imagens escaneadas.

Nesse caso, poderão ser utilizados:

* Tesseract OCR;
* OCRmyPDF.

---

## 8.2 Processo de extração

Para cada página, armazenar:

```json
{
  "book_id": "habitos-atomicos",
  "page_number": 25,
  "text": "Conteúdo completo extraído da página..."
}
```

O sistema deverá preservar a relação entre o texto e o número da página.

Essa associação será essencial para:

* localizar citações;
* validar trechos literais;
* mostrar a origem de cada trecho;
* impedir que a IA invente referências.

---

## 8.3 Limpeza do conteúdo

O texto extraído deverá passar por uma etapa de limpeza.

Remover ou corrigir:

* números de páginas isolados;
* cabeçalhos repetidos;
* rodapés;
* nome do livro repetido em cada página;
* espaços duplicados;
* caracteres quebrados;
* hifenização incorreta;
* quebras de linha excessivas;
* índices repetidos;
* páginas vazias.

O sistema não deverá modificar o conteúdo original utilizado como citação.

Por isso, recomenda-se armazenar duas versões:

```text
original_text
cleaned_text
```

A versão limpa será utilizada na compreensão do livro.

A versão original será utilizada para validar e recuperar citações literais.

---

# 9. Divisão do livro em blocos

O texto deverá ser dividido em blocos menores para que possa ser processado pela IA.

Cada bloco deverá conter:

* identificador;
* livro;
* capítulo;
* página inicial;
* página final;
* texto original;
* texto limpo;
* posição dentro do livro;
* quantidade aproximada de tokens.

Exemplo:

```json
{
  "book_id": "habitos-atomicos",
  "chapter": "Capítulo 2",
  "page_start": 31,
  "page_end": 39,
  "position": 7,
  "original_text": "Texto original...",
  "cleaned_text": "Texto processado...",
  "token_count": 6200
}
```

A divisão não deve cortar o texto no meio de:

* uma frase;
* um parágrafo;
* uma explicação;
* um exemplo;
* uma citação;
* uma seção.

Sempre que possível, a divisão deverá respeitar a estrutura lógica do livro.

---

# 10. Processo de compreensão do livro

## 10.1 Etapa 1 — Análise de cada bloco

Cada bloco deverá ser lido pela IA.

A resposta deverá conter:

* resumo do bloco;
* conceitos apresentados;
* argumentos do autor;
* exemplos utilizados;
* possíveis aprendizados;
* trechos relevantes;
* relação com partes anteriores;
* importância do bloco para o livro;
* páginas de origem.

Exemplo:

```json
{
  "summary": "Resumo do conteúdo do bloco.",
  "concepts": [
    {
      "name": "Identidade baseada em hábitos",
      "explanation": "Explicação do conceito."
    }
  ],
  "arguments": [
    "Argumento principal apresentado pelo autor."
  ],
  "examples": [
    {
      "description": "Exemplo utilizado no livro.",
      "page": 35
    }
  ],
  "relevant_passages": [
    {
      "text": "Trecho exatamente como aparece no livro.",
      "page": 36,
      "reason": "Representa diretamente o conceito principal."
    }
  ],
  "learning_points": [
    "Aprendizado retirado deste bloco."
  ]
}
```

---

## 10.2 Etapa 2 — Análise de cada capítulo

Depois que todos os blocos de um capítulo forem analisados, a IA deverá produzir:

* resumo do capítulo;
* objetivo do capítulo;
* principais conceitos;
* argumentos;
* exemplos;
* trechos mais importantes;
* aprendizados;
* relação com outros capítulos.

---

## 10.3 Etapa 3 — Construção do mapa completo do livro

Após a análise de todos os capítulos, o sistema deverá construir uma visão geral da obra.

O mapa deverá conter:

```json
{
  "main_thesis": "Ideia central defendida pelo livro.",
  "book_objective": "Objetivo principal da obra.",
  "main_concepts": [],
  "secondary_concepts": [],
  "main_arguments": [],
  "important_examples": [],
  "practical_lessons": [],
  "chapter_relationships": [],
  "recommended_passages": [],
  "final_conclusion": "Conclusão geral da obra."
}
```

Esse mapa deverá representar o entendimento construído a partir da leitura de todo o conteúdo.

A microlição final não deverá ser gerada diretamente com base em apenas um bloco ou capítulo.

---

# 11. Geração da microlição de 15 a 20 minutos

## 11.1 Objetivo da microlição

A microlição deverá transmitir os pontos mais importantes do livro em aproximadamente 15 a 20 minutos de leitura.

Ela não deverá simplesmente reduzir proporcionalmente todos os capítulos.

O objetivo é criar uma experiência educacional que:

* apresente a proposta principal;
* explique os conceitos mais relevantes;
* mostre como os conceitos se relacionam;
* utilize exemplos claros;
* apresente trechos reais do livro;
* destaque lições práticas;
* estimule reflexão;
* mantenha fidelidade ao autor.

---

## 11.2 Tamanho recomendado

A quantidade de palavras deverá ser ajustada conforme a complexidade da obra.

Faixa inicial sugerida:

* entre 2.500 e 3.800 palavras;
* máximo aproximado de 4.000 palavras;
* tempo estimado entre 15 e 20 minutos.

O cálculo poderá considerar uma velocidade de leitura entre 180 e 220 palavras por minuto.

```text
tempo_estimado = quantidade_de_palavras / 200
```

O valor será apenas uma estimativa.

---

## 11.3 Estrutura da microlição

```markdown
# Título da microlição

## O que você aprenderá

Descrição breve dos principais aprendizados.

## Sobre o livro

Apresentação da obra, do autor e de sua proposta.

## A ideia central

Explicação clara da principal tese do livro.

## Primeiro aprendizado

Explicação do conceito.

> “Trecho exatamente como aparece no livro.”

**Página:** 35

Explicação do motivo pelo qual esse trecho é importante.

### Exemplo

Exemplo apresentado no livro ou criado para facilitar a compreensão.

### Aplicação prática

Como esse aprendizado pode ser usado no cotidiano.

## Segundo aprendizado

Explicação do conceito.

> “Outro trecho exatamente como aparece no livro.”

**Página:** 74

Contextualização do trecho.

## Terceiro aprendizado

Explicação do conceito e sua relação com os demais.

## Como os conceitos se conectam

Explicação da estrutura geral do pensamento do autor.

## Principais lições do livro

Síntese dos aprendizados mais relevantes.

## Como aplicar

Ações práticas baseadas no conteúdo.

## Reflexão final

Conclusão baseada na mensagem central da obra.

## Perguntas para reflexão

1. Pergunta relacionada ao conteúdo.
2. Pergunta de aplicação prática.
3. Pergunta de reflexão pessoal.

## Referências

Livro, autor, capítulos e páginas utilizadas.
```

---

# 12. Uso de trechos literais do livro

## 12.1 Requisito principal

A microlição deverá conter alguns trechos exatamente como aparecem no PDF.

Esses trechos deverão:

* ser relevantes para o ensinamento;
* possuir contexto;
* representar corretamente a ideia do autor;
* ser armazenados com a página de origem;
* ser comparados com o texto extraído;
* não ser reescritos ou alterados;
* não ser inventados pela IA.

---

## 12.2 Fluxo de seleção de trechos

```text
Texto original extraído
        |
        v
IA identifica um trecho relevante
        |
        v
Backend busca o trecho no texto original
        |
        v
Trecho encontrado?
   |             |
   | sim         | não
   v             v
Salvar          Rejeitar
citação         citação
```

O trecho somente poderá entrar na versão final caso seja localizado no conteúdo original extraído.

---

## 12.3 Estrutura da citação

```json
{
  "book_id": "habitos-atomicos",
  "lesson_id": "uuid",
  "quote_text": "Trecho exatamente como aparece no livro.",
  "page_number": 42,
  "chapter": "Capítulo 3",
  "source_chunk_id": "uuid",
  "verified": true
}
```

---

## 12.4 Contextualização dos trechos

Cada trecho deverá ser acompanhado por:

* explicação;
* contexto;
* relação com o conceito;
* possível aplicação;
* página de origem.

Exemplo:

```markdown
> “Trecho literal selecionado do livro.”

Esse trecho demonstra que o autor considera a mudança de identidade mais importante do que apenas a busca por resultados. Na prática, isso significa que uma pessoa deve pensar em quem deseja se tornar, e não apenas no resultado final que deseja alcançar.
```

---

# 13. Redução de alucinações

O modelo deverá receber instruções rigorosas.

Exemplo:

```text
Você está analisando o conteúdo de um livro.

Utilize somente as informações presentes nos textos fornecidos.

Não invente fatos, exemplos, conceitos, citações, capítulos ou números de páginas.

Ao apresentar uma citação direta, copie o trecho exatamente como ele aparece no conteúdo original.

Toda citação deverá informar sua página de origem.

Não altere palavras em citações diretas.

Caso não consiga localizar um trecho que comprove uma afirmação, não crie uma citação.

Diferencie claramente:
1. ideias apresentadas pelo autor;
2. explicações educacionais criadas para facilitar o entendimento;
3. exemplos adicionais criados para contextualização.
```

---

# 14. Provedor de inteligência artificial

## 14.1 Arquitetura desacoplada

Criar uma interface comum:

```python
from abc import ABC, abstractmethod
from typing import Any

class AIProvider(ABC):

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_instruction: str | None = None,
    ) -> str:
        pass

    @abstractmethod
    async def generate_structured_output(
        self,
        prompt: str,
        response_schema: dict[str, Any],
    ) -> dict[str, Any]:
        pass
```

Implementações:

```text
GeminiProvider
GrokProvider
```

Implementações futuras:

```text
OpenAIProvider
ClaudeProvider
LocalModelProvider
```

---

## 14.2 Configuração

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=
GEMINI_MODEL=

GROK_API_KEY=
GROK_MODEL=
```

A troca de modelo não deverá exigir mudanças nos serviços de processamento.

---

# 15. Backend com FastAPI

## 15.1 Estrutura sugerida

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── books.py
│   │       ├── lessons.py
│   │       ├── users.py
│   │       ├── subscriptions.py
│   │       ├── deliveries.py
│   │       └── webhooks.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   │   ├── pdf_extraction_service.py
│   │   ├── text_cleaning_service.py
│   │   ├── chunking_service.py
│   │   ├── book_analysis_service.py
│   │   ├── lesson_generation_service.py
│   │   ├── quote_validation_service.py
│   │   ├── subscription_service.py
│   │   ├── whatsapp_service.py
│   │   └── email_service.py
│   ├── providers/
│   │   ├── ai/
│   │   ├── whatsapp/
│   │   ├── email/
│   │   └── payments/
│   ├── workers/
│   │   ├── book_processing_tasks.py
│   │   ├── delivery_tasks.py
│   │   └── subscription_tasks.py
│   ├── templates/
│   │   └── emails/
│   └── books/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

# 16. Principais endpoints

## Livros

```text
GET  /books
GET  /books/{book_id}
POST /books/{book_id}/process
GET  /books/{book_id}/processing-status
GET  /books/{book_id}/chapters
GET  /books/{book_id}/analysis
```

Não será necessário um endpoint público de upload de livros.

---

## Lições

```text
POST   /books/{book_id}/lessons
GET    /lessons
GET    /lessons/{lesson_id}
PATCH  /lessons/{lesson_id}
POST   /lessons/{lesson_id}/regenerate
POST   /lessons/{lesson_id}/approve
POST   /lessons/{lesson_id}/send
GET    /lessons/{lesson_id}/quotes
```

---

## Usuários

```text
POST  /users
GET   /users
GET   /users/{user_id}
PATCH /users/{user_id}
GET   /users/{user_id}/preferences
PATCH /users/{user_id}/preferences
```

---

## Assinaturas

```text
GET  /subscriptions/me
POST /subscriptions/sync
POST /webhooks/cakto
GET  /subscriptions/{user_id}
```

---

## Envios

```text
POST /deliveries
GET  /deliveries
GET  /deliveries/{delivery_id}
POST /deliveries/{delivery_id}/retry
```

---

## Webhooks

```text
POST /webhooks/cakto
POST /webhooks/evolution
POST /webhooks/resend
```

---

# 17. Supabase

## 17.1 Responsabilidades

O Supabase será utilizado para:

* PostgreSQL;
* autenticação;
* controle de usuários;
* armazenamento de preferências;
* livros cadastrados;
* conteúdo extraído;
* blocos;
* análises;
* lições;
* citações;
* assinaturas;
* histórico de pagamentos;
* histórico de envios.

---

## 17.2 Tabelas principais

### `profiles`

```text
id
name
email
phone
preferred_channel
preferred_time
timezone
whatsapp_enabled
email_enabled
created_at
updated_at
```

O campo `id` deverá estar relacionado ao usuário do Supabase Auth.

---

### `books`

```text
id
slug
title
author
description
category
file_path
page_count
processing_status
processing_version
processed_at
created_at
updated_at
```

---

### `book_pages`

```text
id
book_id
page_number
original_text
cleaned_text
created_at
```

---

### `book_chunks`

```text
id
book_id
chapter
page_start
page_end
position
original_text
cleaned_text
token_count
created_at
```

---

### `chunk_analyses`

```text
id
chunk_id
provider
model
summary
structured_content
prompt_version
created_at
```

---

### `chapter_analyses`

```text
id
book_id
chapter
summary
structured_content
created_at
```

---

### `book_analyses`

```text
id
book_id
main_thesis
book_objective
structured_content
provider
model
version
created_at
```

---

### `lessons`

```text
id
book_id
title
content_markdown
content_html
whatsapp_content
word_count
estimated_reading_minutes
status
version
approved_at
created_at
updated_at
```

---

### `lesson_quotes`

```text
id
lesson_id
book_id
chunk_id
quote_text
page_number
chapter
verified
created_at
```

---

### `subscriptions`

```text
id
user_id
provider
provider_customer_id
provider_subscription_id
plan_name
status
started_at
current_period_end
cancelled_at
last_verified_at
created_at
updated_at
```

Status possíveis:

```text
pending
active
overdue
cancelled
expired
refunded
unknown
```

---

### `payment_events`

```text
id
user_id
event_type
provider_event_id
payload
processed
received_at
processed_at
```

---

### `deliveries`

```text
id
lesson_id
user_id
channel
status
scheduled_at
sent_at
delivered_at
provider_message_id
error_message
retry_count
created_at
updated_at
```

---

# 18. Integração com a Cakto

## 18.1 Objetivo

A Cakto será responsável pela cobrança mensal da plataforma.

O backend deverá verificar se o usuário possui uma assinatura válida antes de:

* permitir acesso ao conteúdo;
* incluir o usuário em envios agendados;
* enviar microlições;
* liberar funcionalidades exclusivas.

---

## 18.2 Fluxo da assinatura

```text
Usuário escolhe um plano
        |
        v
Checkout da Cakto
        |
        v
Pagamento aprovado
        |
        v
Cakto envia evento
        |
        v
FastAPI processa o webhook
        |
        v
Assinatura recebe status ativo
        |
        v
Usuário recebe acesso
```

---

## 18.3 Eventos que deverão ser tratados

O sistema deverá estar preparado para eventos relacionados a:

* pagamento aprovado;
* assinatura criada;
* renovação aprovada;
* pagamento pendente;
* pagamento recusado;
* assinatura atrasada;
* assinatura cancelada;
* assinatura expirada;
* reembolso;
* chargeback.

Os nomes exatos dos eventos deverão seguir a documentação disponibilizada pela Cakto no momento da implementação.

---

## 18.4 Verificação antes do envio

Antes de criar um envio:

```python
if user.subscription.status != "active":
    skip_delivery()
```

Além do status, o sistema deverá verificar:

* data final do período atual;
* data da última confirmação;
* cancelamento;
* inadimplência;
* reembolso;
* bloqueio manual.

---

## 18.5 Sincronização

A principal atualização deverá ocorrer por webhook.

Também deverá existir uma rotina periódica de sincronização para corrigir possíveis inconsistências.

Exemplo:

```text
Webhook: atualização imediata
Rotina periódica: conferência diária
```

---

## 18.6 Segurança do webhook

O endpoint deverá:

* validar assinatura ou token do webhook;
* registrar o evento recebido;
* evitar processamento duplicado;
* não confiar somente no e-mail enviado no payload;
* relacionar o cliente com o usuário correto;
* retornar uma resposta rápida;
* processar tarefas mais pesadas de forma assíncrona.

---

# 19. Integração com Evolution API

## 19.1 Responsabilidade

A Evolution API será utilizada desde a primeira versão para:

* enviar microlições;
* enviar mensagens de boas-vindas;
* confirmar assinatura;
* informar falhas de pagamento;
* enviar notificações;
* receber status das mensagens.

---

## 19.2 Configuração

```env
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
EVOLUTION_WEBHOOK_SECRET=
```

---

## 19.3 Serviço de envio

```python
class EvolutionWhatsAppProvider:

    async def send_text(
        self,
        phone: str,
        message: str,
    ) -> str:
        ...

    async def send_messages(
        self,
        phone: str,
        messages: list[str],
    ) -> list[str]:
        ...
```

---

## 19.4 Formatação para WhatsApp

A lição deverá ser convertida para um formato próprio.

Exemplo:

```text
📘 *Microlição de hoje*

*Hábitos e identidade*

⏱️ Tempo estimado: 18 minutos

Hoje você aprenderá como pequenas ações repetidas podem modificar a forma como uma pessoa enxerga a si mesma.

━━━━━━━━━━━━━━

*1. A mudança começa pela identidade*

O autor explica que mudanças sustentáveis não acontecem apenas quando buscamos um resultado. Elas se tornam mais fortes quando modificamos a forma como nos identificamos.

📖 *Trecho do livro*

“Trecho exatamente como está escrito no livro.”

📄 Página 35

💡 *O que isso significa?*

Esse trecho mostra que o comportamento tende a se tornar mais consistente quando está ligado à identidade.

*Exemplo prático*

Em vez de pensar “quero correr uma maratona”, a pessoa começa a pensar “sou alguém que pratica corrida”.

━━━━━━━━━━━━━━
```

---

## 19.5 Divisão do conteúdo

A microlição não deverá ser enviada em uma única mensagem muito longa.

Ela deverá ser dividida em partes.

```text
Parte 1 de 5 — Introdução
Parte 2 de 5 — Conceitos principais
Parte 3 de 5 — Trechos e explicações
Parte 4 de 5 — Aplicações
Parte 5 de 5 — Resumo e reflexão
```

O sistema deverá:

* dividir por seção;
* não cortar frases;
* não separar uma citação de sua explicação;
* limitar o tamanho das mensagens;
* manter a ordem;
* inserir um intervalo entre envios;
* registrar cada parte enviada.

---

# 20. Integração com Resend

## 20.1 Responsabilidade

O Resend será utilizado para:

* envio das microlições;
* confirmação de cadastro;
* confirmação de assinatura;
* recuperação de acesso;
* avisos de pagamento;
* notificações da plataforma.

---

## 20.2 Configuração

```env
RESEND_API_KEY=
RESEND_FROM_EMAIL=
RESEND_WEBHOOK_SECRET=
```

---

## 20.3 Template HTML

O e-mail deverá ser:

* responsivo;
* visualmente limpo;
* adequado para dispositivos móveis;
* compatível com os principais clientes de e-mail;
* organizado em blocos;
* fácil de ler.

Estrutura:

```text
Logo
Microlição de hoje
Título
Tempo estimado
Introdução
Ideia central
Trecho do livro
Explicação
Exemplo
Aplicação
Resumo
Perguntas
Rodapé
```

---

## 20.4 Componentes visuais

O template poderá possuir:

* cabeçalho com marca;
* card de tempo de leitura;
* blocos de conteúdo;
* caixa de citação;
* caixa de exemplo;
* caixa de aplicação prática;
* resumo destacado;
* botão para acessar a plataforma;
* rodapé com preferências;
* link de descadastro.

---

## 20.5 Exemplo de bloco de citação

```html
<div class="quote-card">
  <p class="quote">
    “Trecho exatamente como aparece no livro.”
  </p>

  <p class="quote-reference">
    Página 35
  </p>
</div>
```

---

# 21. Frontend com React JS

## 21.1 Estrutura sugerida

```text
frontend/
├── src/
│   ├── api/
│   │   ├── auth.js
│   │   ├── books.js
│   │   ├── lessons.js
│   │   ├── subscriptions.js
│   │   └── deliveries.js
│   ├── components/
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── BooksPage.jsx
│   │   ├── BookDetailsPage.jsx
│   │   ├── LessonEditorPage.jsx
│   │   ├── UsersPage.jsx
│   │   ├── SubscriptionsPage.jsx
│   │   └── DeliveriesPage.jsx
│   ├── hooks/
│   ├── contexts/
│   ├── services/
│   ├── utils/
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

---

## 21.2 Área administrativa

### Dashboard

Mostrar:

* livros disponíveis;
* livros processados;
* livros com erro;
* lições geradas;
* assinantes ativos;
* assinaturas atrasadas;
* envios do dia;
* falhas de entrega.

### Página de livros

Mostrar:

* título;
* autor;
* arquivo;
* quantidade de páginas;
* status;
* última análise;
* botão de processamento;
* botão de geração da microlição.

### Detalhes do livro

Mostrar:

* dados gerais;
* capítulos identificados;
* páginas extraídas;
* blocos;
* mapa geral;
* trechos candidatos;
* microlições.

### Editor de microlição

Permitir:

* editar Markdown;
* visualizar HTML;
* visualizar formato de WhatsApp;
* conferir citações;
* conferir páginas;
* remover uma citação;
* gerar novamente uma seção;
* calcular tempo de leitura;
* aprovar;
* enviar teste.

---

## 21.3 Área do usuário

Mostrar:

* assinatura atual;
* status do pagamento;
* próxima renovação;
* preferências de canal;
* telefone;
* e-mail;
* horário de recebimento;
* últimas lições;
* opção de atualização de dados;
* link para gerenciar ou cancelar assinatura.

---

# 22. Processamento assíncrono

A análise completa do livro poderá demorar e não deverá ocorrer dentro de uma requisição HTTP comum.

Usar uma fila para:

* extrair páginas;
* limpar textos;
* criar blocos;
* analisar blocos;
* analisar capítulos;
* gerar mapa do livro;
* gerar microlição;
* validar citações;
* enviar mensagens;
* enviar e-mails;
* sincronizar assinaturas.

Arquitetura:

```text
FastAPI
   |
   v
Redis
   |
   v
Worker
   |
   ├── PDF
   ├── IA
   ├── Evolution API
   ├── Resend
   └── Cakto
```

---

# 23. Controle de processamento

Cada livro deverá possuir um status.

```text
pending
extracting
cleaning
chunking
analyzing_chunks
analyzing_chapters
building_book_map
generating_lesson
validating_quotes
completed
failed
```

Também deverão ser armazenados:

* etapa atual;
* porcentagem estimada;
* erro;
* data de início;
* data de conclusão;
* número de tentativas.

---

# 24. Segurança e direitos autorais

Os livros deverão ser:

* de propriedade do responsável pela plataforma;
* licenciados;
* de domínio público;
* utilizados com autorização.

A aplicação deverá:

* limitar o acesso aos arquivos;
* não disponibilizar o PDF diretamente;
* não reproduzir capítulos inteiros;
* utilizar citações de forma limitada;
* identificar autor e obra;
* informar que o conteúdo é uma síntese educacional;
* evitar substituir integralmente a leitura da obra;
* proteger os PDFs armazenados no projeto.

---

# 25. Monitoramento

Registrar:

* processamento de livros;
* chamadas à IA;
* consumo de tokens;
* erros de extração;
* erros de análise;
* citações rejeitadas;
* tempo de geração;
* eventos da Cakto;
* alterações em assinaturas;
* mensagens enviadas;
* e-mails enviados;
* erros da Evolution API;
* erros do Resend.

Ferramentas futuras:

* Sentry;
* OpenTelemetry;
* Grafana;
* Prometheus.

---

# 26. Testes necessários

## Testes de PDF

* extração de todas as páginas;
* preservação dos números das páginas;
* limpeza;
* divisão em blocos;
* PDFs corrompidos;
* PDFs sem texto;
* PDFs muito longos.

## Testes de IA

* análise de todos os blocos;
* geração de resumos estruturados;
* identificação de conceitos;
* fidelidade ao conteúdo;
* ausência de informações inventadas;
* qualidade da microlição;
* tempo de leitura.

## Testes de citações

* trecho existe no PDF;
* texto é idêntico ao original;
* página correta;
* rejeição de citações inventadas;
* preservação de pontuação.

## Testes de assinatura

* pagamento aprovado;
* renovação;
* inadimplência;
* cancelamento;
* reembolso;
* webhook duplicado;
* usuário sem assinatura ativa.

## Testes de envio

* WhatsApp;
* e-mail;
* usuário sem telefone;
* usuário sem e-mail;
* usuário sem consentimento;
* assinatura inativa;
* falha de provedor;
* reenvio.

---

# 27. Etapas de desenvolvimento

## Fase 1 — Estrutura base

* criar backend FastAPI;
* criar frontend React;
* configurar Supabase;
* configurar Supabase Auth;
* criar Docker;
* configurar variáveis de ambiente;
* criar estrutura de logs.

---

## Fase 2 — Catálogo interno de livros

* adicionar diretório de PDFs;
* criar metadados;
* cadastrar livros no Supabase;
* criar listagem administrativa;
* criar tela de detalhes.

---

## Fase 3 — Extração completa

* extrair todas as páginas;
* preservar texto original;
* criar versão limpa;
* salvar páginas;
* detectar capítulos;
* dividir em blocos.

---

## Fase 4 — Análise com IA

* criar interface de provedor;
* implementar Gemini;
* implementar Grok;
* analisar todos os blocos;
* analisar capítulos;
* construir mapa do livro;
* armazenar resultados.

---

## Fase 5 — Geração da microlição

* selecionar conceitos;
* selecionar aprendizados;
* selecionar trechos literais;
* gerar microlição;
* calcular tempo;
* armazenar referências;
* validar citações.

---

## Fase 6 — Editor administrativo

* criar editor;
* mostrar citações;
* mostrar páginas;
* permitir ajustes;
* gerar novamente seções;
* aprovar conteúdo.

---

## Fase 7 — Usuários e assinaturas

* criar cadastro;
* criar login;
* criar perfil;
* criar preferências;
* integrar checkout da Cakto;
* criar webhook;
* armazenar assinatura;
* bloquear usuários inativos.

---

## Fase 8 — Resend

* criar templates;
* gerar HTML;
* enviar e-mail de teste;
* enviar microlições;
* processar webhooks;
* registrar entregas.

---

## Fase 9 — Evolution API

* configurar instância;
* criar serviço;
* formatar microlições;
* dividir mensagens;
* controlar intervalos;
* processar webhooks;
* registrar status.

---

## Fase 10 — Agendamento

* definir frequência;
* definir horário;
* verificar assinatura;
* criar envios;
* impedir duplicidade;
* implementar tentativas automáticas.

---

## Fase 11 — Testes e lançamento

* revisar segurança;
* revisar citações;
* testar livros diferentes;
* testar pagamentos;
* testar envios;
* configurar monitoramento;
* realizar deploy.

---

# 28. Critérios de conclusão do MVP

O MVP estará concluído quando:

* os PDFs estiverem armazenados no projeto;
* o sistema conseguir extrair o texto de todas as páginas;
* todo o livro for processado por blocos;
* todos os capítulos forem analisados;
* um mapa geral do livro for criado;
* uma microlição de 15 a 20 minutos for gerada;
* a microlição contiver trechos literais validados;
* os trechos indicarem as páginas corretas;
* o administrador puder revisar o conteúdo;
* usuários puderem contratar pela Cakto;
* o status da assinatura puder ser atualizado;
* somente usuários ativos receberem conteúdo;
* a lição puder ser enviada pela Evolution API;
* a lição puder ser enviada pelo Resend;
* os envios ficarem registrados no Supabase.
