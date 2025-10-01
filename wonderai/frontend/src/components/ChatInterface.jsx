import React, { 
  useCallback, 
  useMemo, 
  useRef, 
  useEffect,
  useOptimistic,
  useTransition
} from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { MessageList } from './MessageList'
import { MessageComposer } from './MessageComposer'
import { TypingIndicator, StreamingMessage } from './TypingIndicator'
import { MessageLoadingStates } from './MessageLoadingStates'
import { 
  selectVisibleMessages,
  selectIsStreaming,
  selectStreamingMessage,
  selectError,
  addMessage,
  setError,
  clearError
} from '@/store/chatSlice'
import { useSendMessageMutation } from '@/store'
import { useStreamingChat } from '@/hooks/useStreaming'
import { toast } from 'sonner'
import {
  Bot,
  AlertCircle,
  Loader2
} from 'lucide-react'

/**
 * Main chat interface component using React 19 features
 * Implements useOptimistic for immediate UI updates and useTransition for smooth interactions
 */
export const ChatInterface = React.memo(() => {
  const dispatch = useDispatch()
  const messages = useSelector(selectVisibleMessages)
  const isStreaming = useSelector(selectIsStreaming)
  const streamingMessage = useSelector(selectStreamingMessage)
  const error = useSelector(selectError)
  
  // React 19 hooks for modern state management
  const [isPending, startTransition] = useTransition()
  const [sendMessage, { isLoading: isSendingMessage }] = useSendMessageMutation()
  const { startStreaming } = useStreamingChat()
  const currentConversationId = useSelector(state => state.chat.currentConversationId) || 'conv-123' // Default for testing
  
  // Refs for scroll management
  const messagesEndRef = useRef(null)
  const scrollAreaRef = useRef(null)

  // React 19 useOptimistic hook for immediate UI feedback
  const [optimisticMessages, addOptimisticMessageLocal] = useOptimistic(
    messages,
    (state, optimisticMessage) => [...state, optimisticMessage]
  )

  // Scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [optimisticMessages.length, streamingMessage, scrollToBottom])

  // Handle streaming message sending
  const handleStreamMessage = useCallback(async (messageContent) => {
    if (!messageContent.trim() || isSendingMessage) return

    const optimisticId = `optimistic_${Date.now()}`
    
    // Add optimistic user message immediately for React 19 smooth UX
    const optimisticMessage = {
      id: optimisticId,
      role: 'user',
      text: messageContent.trim(),
      timestamp: new Date().toISOString(),
      isOptimistic: true,
    }

    // Use React 19 useOptimistic for immediate UI update
    addOptimisticMessageLocal(optimisticMessage)

    // Clear any existing errors
    dispatch(clearError())

    // Add the user message to store
    dispatch(addMessage({
      role: 'user',
      text: messageContent.trim(),
    }))

    try {
      // Start streaming response with conversation ID
      const stream = await startStreaming(currentConversationId, messageContent.trim())
      
      // Process the streaming response
      const reader = stream.getReader()
      let assistantMessage = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        text: '',
        timestamp: new Date().toISOString(),
        isStreaming: true,
      }
      
      // Add initial empty assistant message
      dispatch(addMessage(assistantMessage))
      
      try {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          if (value.type === 'content' && value.content) {
            // Update the assistant message with streaming content
            assistantMessage.text = value.fullContent
            dispatch(addMessage({...assistantMessage, text: value.fullContent}))
          } else if (value.type === 'complete') {
            // Finalize the message
            assistantMessage.isStreaming = false
            assistantMessage.text = value.fullContent
            dispatch(addMessage({...assistantMessage, isStreaming: false}))
            break
          }
        }
      } catch (streamError) {
        console.error('Stream processing error:', streamError)
        dispatch(setError('Streaming interrupted'))
      }
      
      toast.success('Streaming response completed')
    } catch (error) {
      console.error('Failed to start streaming:', error)
      const errorMessage = error?.message || 'Failed to start streaming response'
      dispatch(setError(errorMessage))
      toast.error(errorMessage)
    }
  }, [isSendingMessage, addOptimisticMessageLocal, dispatch, startStreaming, currentConversationId])

  // Handle message sending with React 19 Actions pattern
  const handleSendMessage = useCallback(async (messageContent) => {
    if (!messageContent.trim() || isSendingMessage) return

    const optimisticId = `optimistic_${Date.now()}`
    
    // Add optimistic message immediately for React 19 smooth UX
    const optimisticMessage = {
      id: optimisticId,
      role: 'user',
      text: messageContent.trim(),
      timestamp: new Date().toISOString(),
      isOptimistic: true,
    }

    // Use React 19 useOptimistic for immediate UI update
    addOptimisticMessageLocal(optimisticMessage)

    // Clear any existing errors
    dispatch(clearError())

    // Use React 19 useTransition for smooth state updates
    startTransition(async () => {
      try {
        // Add the user message to store
        dispatch(addMessage({
          role: 'user',
          text: messageContent.trim(),
        }))

        // Send to backend using RTK Query
        const response = await sendMessage({
          conversationId: currentConversationId,
          content: messageContent.trim(),
          messageType: 'text'
        }).unwrap()

        // Add assistant response from backend
        if (response.ai_response) {
          dispatch(addMessage({
            role: 'assistant',
            text: response.ai_response.content || 'I received your message but couldn\'t generate a response.',
            images: [],
            map: null,
            metadata: {
              tokensUsed: response.ai_response.tokens_used || 0,
              messageId: response.ai_response.id
            },
          }))
        }

        toast.success('Message sent successfully')

      } catch (error) {
        console.error('Failed to send message:', error)
        
        const errorMessage = error?.data?.detail || error?.message || 'Failed to send message'
        dispatch(setError(errorMessage))
        
        toast.error(errorMessage)
      }
    })
  }, [
    dispatch, 
    sendMessage, 
    isSendingMessage, 
    addOptimisticMessageLocal,
    currentConversationId
  ])

  // Memoized empty state component
  const EmptyState = useMemo(() => (
    <div className="flex flex-col items-center justify-center h-full p-8 text-center">
      <div className="flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mb-4">
        <Bot className="w-8 h-8 text-primary" />
      </div>
      <h2 className="text-xl font-semibold mb-2">Welcome to WonderAI</h2>
      <p className="text-muted-foreground mb-6 max-w-md">
        I'm your AI assistant powered by advanced language models. I can help with:
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-6 max-w-2xl">
        <Badge variant="secondary" className="p-2">🤔 Answer questions</Badge>
        <Badge variant="secondary" className="p-2">🎨 Generate images</Badge>
        <Badge variant="secondary" className="p-2">🗺️ Provide maps</Badge>
        <Badge variant="secondary" className="p-2">📝 Write content</Badge>
        <Badge variant="secondary" className="p-2">💡 Brainstorm ideas</Badge>
        <Badge variant="secondary" className="p-2">🔍 Research topics</Badge>
      </div>
      <p className="text-sm text-muted-foreground">
        Start by typing a message below or try: "Plan a trip to Paris"
      </p>
    </div>
  ), [])

  // Error state component
  const ErrorState = useMemo(() => error && (
    <Card className="m-4 p-4 border-destructive bg-destructive/5">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
        <div className="flex-1">
          <h3 className="font-medium text-destructive mb-1">Something went wrong</h3>
          <p className="text-sm text-destructive/80">{error}</p>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => dispatch(clearError())}
        >
          Dismiss
        </Button>
      </div>
    </Card>
  ), [error, dispatch])

  // Enhanced streaming state display
  const StreamingDisplay = useMemo(() => {
    if (isStreaming && streamingMessage?.text) {
      return <StreamingMessage content={streamingMessage.text} isComplete={false} />
    }
    if (isStreaming && !streamingMessage?.text) {
      return <TypingIndicator />
    }
    return null
  }, [isStreaming, streamingMessage])
  
  // Loading state for message sending
  const LoadingDisplay = useMemo(() => {
    if (isPending || isSendingMessage) {
      return <MessageLoadingStates.Sending />
    }
    return null
  }, [isPending, isSendingMessage])

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Error Display */}
      {ErrorState}

      {/* Messages Area */}
      <div className="flex-1 overflow-hidden">
        {optimisticMessages.length === 0 ? (
          EmptyState
        ) : (
          <ScrollArea ref={scrollAreaRef} className="h-full">
            <div className="p-4 space-y-4">
              <MessageList 
                messages={optimisticMessages}
                isStreaming={isStreaming}
                streamingMessage={streamingMessage}
              />
              
              {LoadingDisplay}
              {StreamingDisplay}
              
              {/* Scroll anchor */}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>
        )}
      </div>

      {/* Message Composer */}
      <div className="border-t bg-background">
        <MessageComposer
          onSendMessage={handleSendMessage}
          onStreamMessage={handleStreamMessage}
          disabled={isSendingMessage || isPending}
          isLoading={isSendingMessage || isPending}
        />
      </div>
    </div>
  )
})

ChatInterface.displayName = 'ChatInterface'
