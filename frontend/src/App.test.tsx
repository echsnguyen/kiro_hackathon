import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />)
    const heading = screen.getByText(/AI Allied Health Assessment Automator/i)
    expect(heading).toBeInTheDocument()
  })

  it('renders the description', () => {
    render(<App />)
    const description = screen.getByText(/Clinical documentation automation system/i)
    expect(description).toBeInTheDocument()
  })

  it('renders a button', () => {
    render(<App />)
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
  })
})
