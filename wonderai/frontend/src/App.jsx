import React from 'react'
import { Provider } from 'react-redux'
import { Toaster } from '@/components/ui/sonner'
import { store } from '@/store'
import { ChatLayout } from '@/components/ChatLayout'

/**
 * Main App component with React 19 features and modern architecture
 * Provides Redux store and sets up the main chat interface
 */
function App() {
  return (
    <Provider store={store}>
      <div className="min-h-screen bg-background font-sans antialiased">
        <ChatLayout />
        <Toaster />
      </div>
    </Provider>
  )
}

export default App
