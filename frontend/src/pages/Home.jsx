import LessonPreview from '../components/LessonPreview.jsx'
import SubscribeForm from '../components/SubscribeForm.jsx'

export default function Home() {
  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Microaprendizagem diária</p>
          <h1>Uma lição curta de grandes livros no seu email.</h1>
          <p>
            Transforme leituras densas em ideias práticas, enviadas todos os dias no
            horário certo para manter o hábito sem sobrecarga.
          </p>
        </div>
        <SubscribeForm />
      </section>

      <LessonPreview />
    </main>
  )
}

