import React from 'react'
import { Card } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Bot } from 'lucide-react'

/**
 * Typing indicator component for streaming responses
 * Shows when AI is actively generating a response
 */
export const TypingIndicator = React.memo(() => {
    return (
        <div className="flex gap-3 group">
            {/* Avatar */}
            <Avatar className="w-8 h-8 mt-1 shrink-0">
                <AvatarFallback className="bg-secondary text-secondary-foreground">
                    <Bot className="w-4 h-4" />
                </AvatarFallback>
            </Avatar>

            {/* Typing Animation */}
            <div className="flex-1 max-w-[85%] space-y-2">
                <Card className="p-4 border border-blue-200 bg-blue-50/50 dark:border-blue-800 dark:bg-blue-950/20">
                    <div className="flex items-center gap-2">
                        <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                        </div>
                        <span className="text-sm text-muted-foreground">AI is thinking...</span>
                    </div>
                </Card>
            </div>
        </div>
    )
})

TypingIndicator.displayName = 'TypingIndicator'



/**
 * Enhanced streaming message component that shows partial content
 */
export const StreamingMessage = React.memo(({ content = '', isComplete = false }) => {
    return (
        <div className="flex gap-3 mb-4">
            <Avatar className="w-8 h-8 mt-1 shrink-0">
                <AvatarFallback className="bg-secondary text-secondary-foreground">
                    <Bot className="w-4 h-4" />
                </AvatarFallback>
            </Avatar>

            <div className="flex-1 max-w-[85%] space-y-2">
                <Card className={`
          p-3 relative
          ${isComplete
                        ? 'bg-card border'
                        : 'bg-blue-50/50 border-blue-200 dark:bg-blue-950/20 dark:border-blue-800'
                    }
        `}>
                    <div className="prose prose-sm max-w-none">
                        <p className="whitespace-pre-wrap break-words m-0">
                            {content}
                            {!isComplete && (
                                <span className="inline-block w-2 h-4 bg-blue-500 animate-pulse ml-1 align-text-bottom" />
                            )}
                        </p>
                    </div>
                </Card>

                {!isComplete && (
                    <div className="flex items-center gap-1 px-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-blue-500 rounded-full animate-pulse"></div>
                        <span>Streaming response...</span>
                    </div>
                )}
            </div>
        </div>
    )
})

StreamingMessage.displayName = 'StreamingMessage'

export default TypingIndicator
