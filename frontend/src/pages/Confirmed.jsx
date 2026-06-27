import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import api from '../api/client.js'

export default function Confirmed() {
  const [searchParams] = useSearchParams()
  const [status, setStatus] = useState('loading')
  const token = searchParams.get('token')

  useEffect(() => {
    async function confirmSubscription() {
      if (!token) {
        setStatus('missing-token')
        return
      }

      try {
        await api.get(`/api/confirm/${token}`)
        setStatus('success')
      } catch {
        setStatus('error')
      }
    }

    confirmSubscription()
  }, [token])

  return (
    <main className="status-page">
      <section>
        <p className="eyebrow">Confirmação</p>
        <h1>{copyByStatus[status].title}</h1>
        <p>{copyByStatus[status].description}</p>
        <Link to="/">Voltar ao início</Link>
      </section>
    </main>
  )
}

const copyByStatus = {
  loading: {
    title: 'Confirmando sua assinatura...',
    description: 'Aguarde um instante enquanto validamos seu link.',
  },
  success: {
    title: 'Assinatura confirmada.',
    description: 'Você receberá a próxima lição diária no email cadastrado.',
  },
  error: {
    title: 'Link inválido ou expirado.',
    description: 'Faça uma nova inscrição para receber outro email de confirmação.',
  },
  'missing-token': {
    title: 'Token não encontrado.',
    description: 'Use o link enviado no email de confirmação.',
  },
}

