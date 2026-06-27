import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import api from '../api/client.js'

export default function Unsubscribed() {
  const [searchParams] = useSearchParams()
  const [status, setStatus] = useState('loading')
  const token = searchParams.get('token')

  useEffect(() => {
    async function unsubscribe() {
      if (!token) {
        setStatus('missing-token')
        return
      }

      try {
        await api.get(`/api/unsubscribe/${token}`)
        setStatus('success')
      } catch {
        setStatus('error')
      }
    }

    unsubscribe()
  }, [token])

  return (
    <main className="status-page">
      <section>
        <p className="eyebrow">Cancelamento</p>
        <h1>{copyByStatus[status].title}</h1>
        <p>{copyByStatus[status].description}</p>
        <Link to="/">Voltar ao início</Link>
      </section>
    </main>
  )
}

const copyByStatus = {
  loading: {
    title: 'Cancelando sua assinatura...',
    description: 'Aguarde um instante enquanto processamos o pedido.',
  },
  success: {
    title: 'Assinatura cancelada.',
    description: 'Seu email foi removido da lista de envios diários.',
  },
  error: {
    title: 'Link inválido ou já utilizado.',
    description: 'A assinatura pode já ter sido cancelada.',
  },
  'missing-token': {
    title: 'Token não encontrado.',
    description: 'Use o link de cancelamento enviado no email da lição.',
  },
}

