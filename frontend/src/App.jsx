import { useState } from "react";
import {
  ArrowRight,
  BookOpen,
  Bookmark,
  Brain,
  CalendarDays,
  Check,
  ChevronDown,
  Clock,
  Layers,
  Mail,
  Menu,
  MessageCircle,
  ShieldCheck,
  Sparkles,
  Star,
  Target,
  X,
} from "lucide-react";

const checkoutUrl =
  import.meta.env.VITE_CAKTO_CHECKOUT_URL || "https://pay.cakto.com.br/";

const navLinks = [
  { label: "Como funciona", href: "#como-funciona" },
  { label: "Benefícios", href: "#beneficios" },
  { label: "Planos", href: "#planos" },
  { label: "Perguntas", href: "#perguntas" },
];

const readerSignals = [
  "Meu Kindle está cheio.",
  "Eu começo e não termino.",
  "Eu compro mais do que consigo ler.",
  "Eu esqueço o que li.",
];

const processSteps = [
  {
    icon: BookOpen,
    title: "Escolhemos grandes livros",
    text: "Priorizamos obras com ideias práticas para trabalho, dinheiro, comportamento e decisão.",
  },
  {
    icon: Layers,
    title: "Organizamos os aprendizados",
    text: "Separamos tese central, conceitos, exemplos e aplicacoes sem transformar tudo em resumo raso.",
  },
  {
    icon: Clock,
    title: "Criamos uma leitura curta",
    text: "Cada microlição cabe em 15 a 20 minutos, com ordem clara e ritmo de leitura.",
  },
  {
    icon: MessageCircle,
    title: "Você recebe no seu canal",
    text: "WhatsApp para acompanhar no celular e e-mail para guardar, revisar e consultar depois.",
  },
];

const benefits = [
  {
    number: "01",
    title: "Mais repertorio",
    text: "Ideias de grandes livros entram na sua semana sem depender de longas sessões de leitura.",
  },
  {
    number: "02",
    title: "Decisoes melhores",
    text: "Cada lição termina com aplicações práticas para transformar leitura em critério.",
  },
  {
    number: "03",
    title: "Mais clareza",
    text: "Conceitos densos chegam organizados em uma sequencia facil de acompanhar.",
  },
  {
    number: "04",
    title: "Habito consistente",
    text: "Aprender vira um pequeno compromisso diario em vez de uma meta distante.",
  },
  {
    number: "05",
    title: "Crescimento profissional",
    text: "Negócios, finanças e comportamento com foco em decisão, comunicação e execução.",
  },
  {
    number: "06",
    title: "Menos culpa",
    text: "Você aproveita o essencial mesmo quando não consegue terminar todos os livros.",
  },
];

const comparison = [
  ["Resumo genérico", "Leitura estruturada"],
  ["Pouco contexto", "Trechos relevantes"],
  ["Texto distante", "Explicacoes claras"],
  ["Sem aplicação", "Aplicação prática"],
];

const faqs = [
  {
    question: "Quanto tempo dura cada leitura?",
    answer:
      "A maior parte das microlições é pensada para 15 a 20 minutos, com leitura direta, contexto e uma aplicação prática.",
  },
  {
    question: "Preciso ler o livro antes?",
    answer:
      "Não. A microlição foi criada para dar contexto, apresentar ideias essenciais e ajudar você a decidir se quer aprofundar no livro completo.",
  },
  {
    question: "As lições substituem os livros?",
    answer:
      "Não. Elas são uma porta de entrada organizada para aprender melhor, revisar conceitos e escolher o que merece leitura completa.",
  },
  {
    question: "Onde recebo os conteúdos?",
    answer:
      "Você recebe pelo WhatsApp e também por e-mail, usando os dados informados no checkout.",
  },
  {
    question: "Quantas lições recebo?",
    answer:
      "A assinatura libera novas microlições durante o período ativo e o histórico de conteúdos disponível no plano contratado.",
  },
  {
    question: "Posso cancelar?",
    answer:
      "Sim. O cancelamento pode ser feito a qualquer momento pelo fluxo da assinatura.",
  },
];

function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="site-header">
      <div className="header-shell">
        <a className="brand-mark" href="#topo" aria-label="MicroAprendizagem">
          <span className="brand-icon">
            <BookOpen size={18} />
          </span>
          <span>MicroAprendizagem</span>
        </a>

        <nav className="desktop-nav" aria-label="Principal">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href}>
              {link.label}
            </a>
          ))}
        </nav>

        <div className="header-actions">
          <a className="button button-dark header-cta" href={checkoutUrl}>
            Quero começar
          </a>
          <button
            className="menu-button"
            type="button"
            aria-label={isOpen ? "Fechar menu" : "Abrir menu"}
            aria-expanded={isOpen}
            onClick={() => setIsOpen((current) => !current)}
          >
            {isOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="mobile-menu">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href} onClick={() => setIsOpen(false)}>
              {link.label}
            </a>
          ))}
          <a className="button button-dark" href={checkoutUrl}>
            Quero começar
          </a>
        </div>
      )}
    </header>
  );
}

function LessonMockup() {
  return (
    <div className="lesson-stage" aria-label="Exemplo visual de uma microlição">
      <div className="page-card page-card-back">
        <span>300 paginas</span>
      </div>
      <div className="page-card page-card-mid">
        <span>20 minutos</span>
      </div>
      <article className="phone-mockup">
        <div className="phone-top">
          <span>Microlicao</span>
          <span>18 min</span>
        </div>
        <div className="progress-track">
          <span />
        </div>
        <p className="eyebrow">Habitos Atomicos</p>
        <h3>Como pequenos habitos geram grandes resultados</h3>
        <ul>
          <li>Ambiente influencia comportamento</li>
          <li>Identidade sustenta consistencia</li>
          <li>Pequenas repeticoes criam vantagem</li>
        </ul>
        <div className="quote-strip">
          <Bookmark size={16} />
          <span>Aplicação prática para testar hoje</span>
        </div>
      </article>
      <div className="floating-note">
        <Sparkles size={17} />
        <span>1 grande aprendizado</span>
      </div>
    </div>
  );
}

function App() {
  return (
    <main id="topo" className="site-page">
      <Header />

      <section className="hero-section">
        <div className="container hero-grid">
          <div className="hero-copy">
            <p className="pill">Conhecimento para quem tem pouco tempo</p>
            <h1>
              Você não precisa de mais livros.
              <span>Precisa de mais tempo para aprender.</span>
            </h1>
            <p className="hero-subtitle">
              Transforme 20 minutos da sua rotina em aprendizados práticos
              extraídos de grandes livros.
            </p>

            <div className="hero-actions">
              <a className="button button-dark" href={checkoutUrl}>
                Quero aprender todos os dias
                <ArrowRight size={18} />
              </a>
              <a className="button button-light" href="#microlicao">
                Ver uma microlição
              </a>
            </div>

            <div className="hero-proof" aria-label="Benefícios principais">
              <span>
                <Check size={17} /> WhatsApp e e-mail
              </span>
              <span>
                <Check size={17} /> Leitura de 15 a 20 min
              </span>
              <span>
                <Check size={17} /> Aplicação prática
              </span>
            </div>
          </div>

          <LessonMockup />
        </div>
      </section>

      <section className="pain-section">
        <div className="container pain-grid">
          <div>
            <p className="section-kicker">A rotina sempre vence</p>
            <h2>Quantos livros estão esperando por você?</h2>
          </div>
          <div className="pain-copy">
            <p>
              Você compra livros, salva recomendações e promete que vai começar
              na próxima semana.
            </p>
            <p>
              Mas o dia enche, a energia cai e a fila de leitura continua
              crescendo.
            </p>
            <p className="pain-emphasis">
              O problema nunca foi falta de vontade. Foi falta de tempo.
            </p>
          </div>
        </div>
      </section>

      <section className="identity-section">
        <div className="container">
          <div className="section-heading">
            <p className="section-kicker">Identificacao</p>
            <h2>Se alguma dessas frases parece familiar, você está no lugar certo.</h2>
          </div>
          <div className="signal-grid">
            {readerSignals.map((signal) => (
              <blockquote key={signal}>{signal}</blockquote>
            ))}
          </div>
        </div>
      </section>

      <section className="solution-section">
        <div className="container centered-section">
          <p className="section-kicker">A solucao</p>
          <h2>Aprender pode caber na sua rotina.</h2>
          <p>
            A MicroAprendizagem transforma livros completos em uma sequência
            clara: ideia principal, contexto, microlição e aplicação prática.
          </p>
          <div className="flow-row" aria-label="Fluxo da aprendizagem">
            {["Livro completo", "Ideias principais", "Microlição", "Aplicação prática"].map(
              (item, index) => (
                <div key={item} className="flow-item">
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <strong>{item}</strong>
                </div>
              ),
            )}
          </div>
        </div>
      </section>

      <section id="como-funciona" className="how-section">
        <div className="container">
          <div className="section-heading narrow">
            <p className="section-kicker">Como funciona</p>
            <h2>Quatro etapas para transformar leitura em prática.</h2>
          </div>
          <div className="timeline">
            {processSteps.map((step, index) => {
              const Icon = step.icon;
              return (
                <article key={step.title} className="timeline-step">
                  <span className="step-number">{String(index + 1).padStart(2, "0")}</span>
                  <Icon size={24} />
                  <h3>{step.title}</h3>
                  <p>{step.text}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section id="microlicao" className="sample-section">
        <div className="container sample-grid">
          <div>
            <p className="section-kicker">Exemplo de microlição</p>
            <h2>Veja como uma ideia densa vira uma leitura objetiva.</h2>
            <p>
              O conteudo chega com tese central, topicos, trecho contextualizado
              e uma pequena acao para aplicar no mesmo dia.
            </p>
            <ul className="check-list">
              <li>
                <Check size={18} /> Tempo de leitura estimado
              </li>
              <li>
                <Check size={18} /> Principais aprendizados
              </li>
              <li>
                <Check size={18} /> Aplicação prática
              </li>
            </ul>
            <a className="button button-gold" href={checkoutUrl}>
              Quero receber as lições
            </a>
          </div>

          <article className="email-mockup">
            <div className="email-header">
              <span>Habitos Atomicos</span>
              <span>18 minutos</span>
            </div>
            <h3>O que você vai aprender</h3>
            <ol>
              <li>Como pequenos habitos geram grandes resultados</li>
              <li>Como o ambiente influencia o comportamento</li>
              <li>Como construir uma identidade consistente</li>
            </ol>
            <div className="lesson-block">
              <strong>Trecho do livro</strong>
              <p>
                Um trecho curto entra apenas quando ajuda a iluminar o conceito,
                sempre acompanhado de explicacao.
              </p>
            </div>
            <div className="lesson-block muted">
              <strong>Aplicação prática</strong>
              <p>Escolha um habito e reduza a primeira acao para menos de dois minutos.</p>
            </div>
          </article>
        </div>
      </section>

      <section id="beneficios" className="benefits-section">
        <div className="container">
          <div className="section-heading">
            <p className="section-kicker">Benefícios</p>
            <h2>O que muda quando você aprende todos os dias?</h2>
          </div>
          <div className="benefit-layout">
            {benefits.map((benefit, index) => (
              <article
                key={benefit.title}
                className={index < 2 ? "benefit-card feature" : "benefit-card"}
              >
                <span>{benefit.number}</span>
                <h3>{benefit.title}</h3>
                <p>{benefit.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="difference-section">
        <div className="container difference-grid">
          <div>
            <p className="section-kicker">Diferencial</p>
            <h2>Muito mais do que um resumo.</h2>
            <p>
              A proposta não é reduzir livros a frases prontas. É organizar
              conhecimento para que você entenda, revise e aplique.
            </p>
          </div>
          <div className="comparison-grid">
            <div className="comparison-column simple">
              <h3>Modelo comum</h3>
              {comparison.map(([common]) => (
                <p key={common}>{common}</p>
              ))}
            </div>
            <div className="comparison-column premium">
              <h3>Sua plataforma</h3>
              {comparison.map(([, premium]) => (
                <p key={premium}>
                  <Check size={17} /> {premium}
                </p>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="proof-section">
        <div className="container proof-grid">
          <div>
            <p className="section-kicker">Primeiros leitores</p>
            <h2>Uma lista de espera para quem quer aprender com mais constancia.</h2>
          </div>
          <div className="proof-stats">
            <div>
              <Star size={22} />
              <strong>Beta</strong>
              <span>Conteudos testados com leitores iniciais</span>
            </div>
            <div>
              <Brain size={22} />
              <strong>Curadoria</strong>
              <span>Livros de negócios, finanças e desenvolvimento</span>
            </div>
            <div>
              <CalendarDays size={22} />
              <strong>Rotina</strong>
              <span>Formato pensado para poucos minutos por dia</span>
            </div>
          </div>
        </div>
      </section>

      <section id="planos" className="pricing-section">
        <div className="container">
          <div className="section-heading inverted">
            <p className="section-kicker">Planos</p>
            <h2>Um pequeno investimento para aprender o ano inteiro.</h2>
          </div>
          <div className="pricing-grid">
            <article className="plan-card recommended">
              <span className="plan-badge">Melhor escolha</span>
              <h3>Plano anual</h3>
              <p>Todos os beneficios do mensal, com condicao especial para o ano.</p>
              <ul>
                <li>
                  <Check size={17} /> Economia no valor total
                </li>
                <li>
                  <Check size={17} /> Novas microlicoes
                </li>
                <li>
                  <Check size={17} /> WhatsApp, e-mail e histórico
                </li>
              </ul>
              <a className="button button-dark" href={checkoutUrl}>
                Comecar agora
              </a>
            </article>
            <article className="plan-card">
              <h3>Plano mensal</h3>
              <p>Acesso completo com cancelamento a qualquer momento.</p>
              <ul>
                <li>
                  <Check size={17} /> Novas microlicoes
                </li>
                <li>
                  <Check size={17} /> Entrega por WhatsApp
                </li>
                <li>
                  <Check size={17} /> Versão por e-mail
                </li>
              </ul>
              <a className="button button-light" href={checkoutUrl}>
                Comecar agora
              </a>
            </article>
          </div>
        </div>
      </section>

      <section id="perguntas" className="faq-section">
        <div className="container faq-grid">
          <div>
            <p className="section-kicker">Perguntas frequentes</p>
            <h2>Antes de começar</h2>
            <p>
              A compra acontece pelo checkout seguro. Depois da confirmação, os
              envios são liberados para assinantes ativos.
            </p>
          </div>
          <div className="faq-list">
            {faqs.map((item) => (
              <details key={item.question}>
                <summary>
                  {item.question}
                  <ChevronDown size={18} />
                </summary>
                <p>{item.answer}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      <section className="final-cta">
        <div className="container final-cta-grid">
          <div>
            <p className="section-kicker">Comece agora</p>
            <h2>Seu próximo aprendizado está a apenas alguns minutos.</h2>
            <p>
              Você não precisa esperar as férias. Não precisa encontrar duas
              horas livres. Não precisa terminar um livro inteiro hoje.
            </p>
          </div>
          <a className="button button-dark" href={checkoutUrl}>
            Quero aprender todos os dias
            <ArrowRight size={18} />
          </a>
        </div>
      </section>

      <footer className="site-footer">
        <div className="container footer-grid">
          <div>
            <a className="brand-mark footer-brand" href="#topo">
              <span className="brand-icon">
                <BookOpen size={18} />
              </span>
              <span>MicroAprendizagem</span>
            </a>
            <p>Conhecimento que acompanha a sua rotina.</p>
          </div>
          <div className="footer-links">
            <a href="#como-funciona">Como funciona</a>
            <a href="#planos">Planos</a>
            <a href="mailto:suporte@microaprendizagem.com">Suporte</a>
            <a href="#perguntas">Perguntas</a>
          </div>
          <p className="footer-note">
            Conteúdo educacional em formato de síntese. PDFs e livros completos
            não são distribuídos.
          </p>
        </div>
      </footer>
    </main>
  );
}

export default App;
