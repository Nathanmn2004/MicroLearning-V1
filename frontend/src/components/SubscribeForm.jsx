import { useState } from 'react'
import api from '../api/client.js'

const initialForm = {
  name: '',
  email: '',
}

export default function SubscribeForm() {
  const [form, setForm] = useState(initialForm)
  const [status, setStatus] = useState('idle')
  const [message, setMessage] = useState('')

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setStatus('loading')
    setMessage('')

    try {
      const response = await api.post('/api/subscribe', form)
      setStatus('success')
      setMessage(response.data.message || 'Confira seu email para confirmar a assinatura.')
      setForm(initialForm)
    } catch (error) {
      setStatus('error')
      setMessage(error.response?.data?.detail || 'Não foi possível concluir a inscrição.')
    }
  }

  return (
    <form className="subscribe-form" onSubmit={handleSubmit}>
      <label>
        Nome
        <input
          name="name"
          type="text"
          value={form.name}
          onChange={updateField}
          minLength={2}
          placeholder="Seu nome"
          required
        />
      </label>

      <label>
        Email
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={updateField}
          placeholder="voce@email.com"
          required
        />
      </label>

      <button type="submit" disabled={status === 'loading'}>
        {status === 'loading' ? 'Enviando...' : 'Receber lições diárias'}
      </button>

      {message && <p className={`form-message ${status}`}>{message}</p>}
    </form>
  )
}

