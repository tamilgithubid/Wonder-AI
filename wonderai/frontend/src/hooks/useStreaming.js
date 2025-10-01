import { useEffect, useRef, useCallback } from 'react'

/**
 * Custom hook for Server-Sent Events streaming
 * Provides real-time streaming capabilities for chat responses
 */
export const useServerSentEvents = (url, options = {}) => {
  const eventSourceRef = useRef(null)
  const { onMessage, onError, onOpen, onClose, enabled = true } = options

  const connect = useCallback(() => {
    if (!enabled || !url) return

    // Close existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
    }

    try {
      const eventSource = new EventSource(url)
      eventSourceRef.current = eventSource

      eventSource.onopen = (event) => {
        console.log('SSE connection opened:', event)
        onOpen?.(event)
      }

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          onMessage?.(data)
        } catch (error) {
          console.error('Failed to parse SSE message:', error, event.data)
          onError?.(error)
        }
      }

      eventSource.onerror = (event) => {
        console.error('SSE error:', event)
        onError?.(event)
        
        // Auto-reconnect on error (with backoff)
        setTimeout(() => {
          if (eventSourceRef.current?.readyState !== EventSource.OPEN) {
            connect()
          }
        }, 1000)
      }

      eventSource.onclose = (event) => {
        console.log('SSE connection closed:', event)
        onClose?.(event)
      }

    } catch (error) {
      console.error('Failed to create EventSource:', error)
      onError?.(error)
    }
  }, [url, enabled, onMessage, onError, onOpen, onClose])

  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
  }, [])

  useEffect(() => {
    if (enabled && url) {
      connect()
    }

    return () => {
      disconnect()
    }
  }, [connect, disconnect, enabled, url])

  return {
    connect,
    disconnect,
    isConnected: eventSourceRef.current?.readyState === EventSource.OPEN
  }
}

/**
 * Custom hook for streaming chat messages
 * Handles message streaming with proper state management
 */
export const useStreamingChat = () => {
  const streamingMessageRef = useRef('')
  
  const startStreaming = useCallback(async (conversationId, content) => {
    streamingMessageRef.current = ''
    
    const response = await fetch(`http://localhost:8000/api/chat/conversations/${conversationId}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    })

    if (!response.body) {
      throw new Error('No response body for streaming')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    return new ReadableStream({
      start(controller) {
        function pump() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              controller.close()
              return
            }

            const chunk = decoder.decode(value, { stream: true })
            const lines = chunk.split('\n')

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  
                  if (data.type === 'content' && data.content) {
                    streamingMessageRef.current += data.content
                    controller.enqueue({
                      type: 'content',
                      content: data.content,
                      fullContent: streamingMessageRef.current,
                      finished: data.finished
                    })
                  } else if (data.type === 'complete' || data.finished) {
                    controller.enqueue({
                      type: 'complete',
                      fullContent: streamingMessageRef.current,
                      finished: true
                    })
                  } else if (data.type === 'error') {
                    controller.error(new Error(data.error))
                  }
                } catch (error) {
                  console.error('Error parsing streaming data:', error, line)
                }
              }
            }

            return pump()
          })
        }

        return pump()
      }
    })
  }, [])

  return { startStreaming }
}
