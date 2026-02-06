import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Allied Health Assessment Automator</h1>
        <p>Clinical documentation automation system</p>
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
          <p>
            Frontend is ready. Backend API integration coming soon.
          </p>
        </div>
      </header>
    </div>
  )
}

export default App
