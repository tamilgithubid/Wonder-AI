import React, { useMemo, useState, useCallback } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import { CodeBlock } from './CodeBlock'
import {
    User,
    Bot,
    Image as ImageIcon,
    Map as MapIcon,
    Copy,
    ThumbsUp,
    ThumbsDown,
    Clock,
    Loader2,
    CheckCircle,
    AlertCircle
} from 'lucide-react'
import { toast } from 'sonner'
import { cn } from '@/lib/utils'

/**
 * Individual message component with enhanced UI/UX for loading states and code display
 */
const MessageItem = React.memo(({ message }) => {
    const isUser = message.role === 'user'
    const isOptimistic = message.isOptimistic
    const isStreaming = message.isStreaming
    const isError = message.error

    // Format timestamp
    const timestamp = useMemo(() => {
        if (!message.timestamp) return ''

        const date = new Date(message.timestamp)
        const now = new Date()
        const diffInMinutes = Math.floor((now - date) / (1000 * 60))

        if (diffInMinutes < 1) return 'Just now'
        if (diffInMinutes < 60) return `${diffInMinutes}m ago`
        if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`

        return date.toLocaleDateString()
    }, [message.timestamp])

    // Parse message content for code blocks and regular text
    const parsedContent = useMemo(() => {
        if (!message.text) return []

        const parts = []
        const text = message.text

        // Regex to match code blocks with optional language specification
        const codeBlockRegex = /```(\w+)?\n?([\s\S]*?)```/g
        let lastIndex = 0
        let match

        while ((match = codeBlockRegex.exec(text)) !== null) {
            // Add text before code block
            if (match.index > lastIndex) {
                const beforeText = text.slice(lastIndex, match.index).trim()
                if (beforeText) {
                    parts.push({ type: 'text', content: beforeText })
                }
            }

            // Add code block
            const language = match[1] || 'text'
            const code = match[2].trim()
            parts.push({ type: 'code', language, content: code })

            lastIndex = match.index + match[0].length
        }

        // Add remaining text
        if (lastIndex < text.length) {
            const remainingText = text.slice(lastIndex).trim()
            if (remainingText) {
                parts.push({ type: 'text', content: remainingText })
            }
        }

        // If no code blocks found, return the entire text as one part
        if (parts.length === 0) {
            parts.push({ type: 'text', content: text })
        }

        return parts
    }, [message.text])

    // Copy message content to clipboard
    const handleCopy = React.useCallback(() => {
        navigator.clipboard.writeText(message.text)
        toast.success('Message copied to clipboard')
    }, [message.text])

    // Handle feedback (placeholder for future implementation)
    const handleFeedback = React.useCallback((isPositive) => {
        toast.success(isPositive ? 'Positive feedback sent' : 'Negative feedback sent')
        // TODO: Implement feedback API call
    }, [])

    // Render status indicator
    const StatusIndicator = React.memo(() => {
        if (isOptimistic) {
            return (
                <div className="flex items-center gap-1 mb-2 text-xs opacity-70">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Sending...</span>
                </div>
            )
        }

        if (isStreaming) {
            return (
                <div className="flex items-center gap-1 mb-2 text-xs opacity-70">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                    <span>AI is typing...</span>
                </div>
            )
        }

        if (isError) {
            return (
                <div className="flex items-center gap-1 mb-2 text-xs text-destructive">
                    <AlertCircle className="w-3 h-3" />
                    <span>Failed to send</span>
                </div>
            )
        }

        return null
    })

    return (
        <div className={`
      flex gap-3 group
      ${isUser ? 'flex-row-reverse' : 'flex-row'}
      ${isOptimistic ? 'opacity-70' : ''}
      ${isError ? 'opacity-60' : ''}
    `}>
            {/* Avatar */}
            <Avatar className="w-8 h-8 mt-1 shrink-0">
                <AvatarFallback className={
                    isUser
                        ? 'bg-primary text-primary-foreground'
                        : isError
                            ? 'bg-destructive text-destructive-foreground'
                            : 'bg-secondary text-secondary-foreground'
                }>
                    {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </AvatarFallback>
            </Avatar>

            {/* Message Content */}
            <div className={`
        flex-1 max-w-[85%] space-y-2
        ${isUser ? 'items-end' : 'items-start'}
      `}>
                {/* Message Bubble */}
                <Card className={`
          relative overflow-hidden
          ${isUser
                        ? 'bg-primary text-primary-foreground ml-auto'
                        : isError
                            ? 'bg-destructive/5 border-destructive/20'
                            : 'bg-card border'
                    }
          ${isOptimistic ? 'animate-pulse' : ''}
          ${isStreaming ? 'border-blue-200 bg-blue-50/50 dark:border-blue-800 dark:bg-blue-950/20' : ''}
        `}>
                    {/* Status Indicator */}
                    <StatusIndicator />

                    {/* Content */}
                    <div className="space-y-3">
                        {parsedContent.map((part, index) => {
                            if (part.type === 'code') {
                                return (
                                    <div key={index} className={isUser ? '' : '-mx-3 -mb-3 mt-3'}>
                                        <CodeBlock
                                            language={part.language}
                                            showLineNumbers={part.content.split('\n').length > 3}
                                            allowCopy={true}
                                            allowDownload={true}
                                        >
                                            {part.content}
                                        </CodeBlock>
                                    </div>
                                )
                            }

                            return (
                                <div key={index} className="prose prose-sm max-w-none">
                                    <p className="whitespace-pre-wrap break-words m-0">
                                        {part.content}
                                    </p>
                                </div>
                            )
                        })}
                    </div>

                    {/* Images */}
                    {message.images && message.images.length > 0 && (
                        <div className="mt-3 space-y-2">
                            <div className="flex items-center gap-1 text-xs opacity-70">
                                <ImageIcon className="w-3 h-3" />
                                <span>{message.images.length} image(s)</span>
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                {message.images.map((imageUrl, index) => (
                                    <img
                                        key={index}
                                        src={imageUrl}
                                        alt={`Generated image ${index + 1}`}
                                        className="rounded border bg-muted max-w-full h-auto"
                                        loading="lazy"
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Map */}
                    {message.map && (
                        <div className="mt-3 space-y-2">
                            <div className="flex items-center gap-1 text-xs opacity-70">
                                <MapIcon className="w-3 h-3" />
                                <span>Map location</span>
                            </div>
                            <Card className="p-2 bg-muted">
                                <p className="text-xs">
                                    📍 {message.map.center?.lat?.toFixed(4)}, {message.map.center?.lng?.toFixed(4)}
                                </p>
                                {message.map.markers && message.map.markers.length > 0 && (
                                    <p className="text-xs mt-1">
                                        {message.map.markers.length} marker(s)
                                    </p>
                                )}
                                {/* TODO: Integrate actual map component */}
                                <div className="w-full h-24 bg-muted rounded border mt-2 flex items-center justify-center">
                                    <MapIcon className="w-6 h-6 opacity-50" />
                                </div>
                            </Card>
                        </div>
                    )}

                    {/* Streaming indicator with cursor */}
                    {isStreaming && (
                        <div className="inline-block w-2 h-4 bg-current animate-pulse ml-1" />
                    )}
                </Card>

                {/* Message Actions & Timestamp */}
                <div className={`
          flex items-center gap-2 px-1
          ${isUser ? 'justify-end' : 'justify-start'}
        `}>
                    <span className="text-xs text-muted-foreground">
                        {timestamp}
                    </span>

                    {/* Token usage for AI messages */}
                    {!isUser && message.metadata?.tokensUsed && (
                        <Badge variant="outline" className="text-xs">
                            {message.metadata.tokensUsed} tokens
                        </Badge>
                    )}

                    {!isOptimistic && !isStreaming && (
                        <div className={`
              flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity
              ${isUser ? 'flex-row-reverse' : 'flex-row'}
            `}>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-6 w-6"
                                onClick={handleCopy}
                                title="Copy message"
                            >
                                <Copy className="w-3 h-3" />
                            </Button>

                            {!isUser && !isError && (
                                <>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-6 w-6"
                                        onClick={() => handleFeedback(true)}
                                        title="Good response"
                                    >
                                        <ThumbsUp className="w-3 h-3" />
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-6 w-6"
                                        onClick={() => handleFeedback(false)}
                                        title="Poor response"
                                    >
                                        <ThumbsDown className="w-3 h-3" />
                                    </Button>
                                </>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
})

MessageItem.displayName = 'MessageItem'

/**
 * MessageList component that renders all messages with React 19 performance optimizations
 */
export const MessageList = React.memo(({
    messages = [],
    isStreaming = false,
    streamingMessage = null
}) => {
    const displayMessages = useMemo(() => {
        const allMessages = [...messages]

        // Add streaming message if active
        if (streamingMessage && isStreaming) {
            allMessages.push({
                ...streamingMessage,
                isStreaming: true,
            })
        }

        return allMessages
    }, [messages, streamingMessage, isStreaming])

    if (displayMessages.length === 0) {
        return null
    }

    return (
        <div className="space-y-6">
            {displayMessages.map((message, index) => (
                <React.Fragment key={message.id || `msg-${index}`}>
                    <MessageItem
                        message={message}
                    />

                    {/* Add separator between different speakers */}
                    {index < displayMessages.length - 1 &&
                        displayMessages[index].role !== displayMessages[index + 1].role && (
                            <Separator className="my-4" />
                        )}
                </React.Fragment>
            ))}
        </div>
    )
})

MessageList.displayName = 'MessageList'
