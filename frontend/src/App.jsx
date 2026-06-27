import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Confirmed from './pages/Confirmed.jsx'
import Home from './pages/Home.jsx'
import Unsubscribed from './pages/Unsubscribed.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/confirmed" element={<Confirmed />} />
        <Route path="/unsubscribed" element={<Unsubscribed />} />
      </Routes>
    </BrowserRouter>
  )
}

