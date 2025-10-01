import React, { useCallback } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
    selectAllMessages,
    selectUserId,
    clearCurrentConversation,
    setUserId
} from '@/store/chatSlice'
import {
    Plus,
    MessageSquare,
    Trash2,
    User,
    History,
    Bot
} from 'lucide-react'

/**
 * Sidebar component for conversation history and user management
 * Implements SOLID principles and React 19 patterns
 */
export const Sidebar = React.memo(({ isMobile = false }) => {
    const dispatch = useDispatch()
    const messages = useSelector(selectAllMessages)
    const userId = useSelector(selectUserId)

    // Memoized handlers for performance optimization
    const handleNewConversation = useCallback(() => {
        dispatch(clearCurrentConversation())
    }, [dispatch])

    const handleRegenerateUserId = useCallback(() => {
        const newUserId = `user_${Date.now()}`
        dispatch(setUserId(newUserId))
    }, [dispatch])

    // Group messages into conversation sessions
    const conversationSessions = React.useMemo(() => {
        const sessions = []
        let currentSession = null

        messages.forEach((message, index) => {
            if (message.role === 'user') {
                if (currentSession) {
                    sessions.push(currentSession)
                }
                currentSession = {
                    id: `session_${index}`,
                    title: message.text.length > 30
                        ? message.text.substring(0, 30) + '...'
                        : message.text,
                    timestamp: message.timestamp,
                    messageCount: 1,
                }
            } else if (currentSession) {
                currentSession.messageCount++
            }
        })

        if (currentSession) {
            sessions.push(currentSession)
        }

        return sessions.reverse() // Show most recent first
    }, [messages])

    const ConversationHistory = React.memo(() => (
        <div className="space-y-2">
            <div className="flex items-center gap-2 mb-3">
                <History className="h-4 w-4" />
                <span className="text-sm font-medium">Recent Conversations</span>
                <Badge variant="secondary" className="ml-auto text-xs">
                    {conversationSessions.length}
                </Badge>
            </div>

            <ScrollArea className="h-64">
                <div className="space-y-1">
                    {conversationSessions.length === 0 ? (
                        <div className="text-center text-muted-foreground text-sm py-8">
                            <MessageSquare className="h-8 w-8 mx-auto mb-2 opacity-50" />
                            <p>No conversations yet</p>
                            <p className="text-xs">Start chatting to see history</p>
                        </div>
                    ) : (
                        conversationSessions.map((session) => (
                            <Card
                                key={session.id}
                                className="p-3 cursor-pointer hover:bg-accent transition-colors"
                            >
                                <div className="flex items-start justify-between gap-2">
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium truncate">
                                            {session.title}
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            {session.messageCount} messages
                                        </p>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-6 w-6 opacity-0 group-hover:opacity-100"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            // TODO: Implement individual conversation deletion
                                        }}
                                    >
                                        <Trash2 className="h-3 w-3" />
                                    </Button>
                                </div>
                            </Card>
                        ))
                    )}
                </div>
            </ScrollArea>
        </div>
    ))

    const UserSection = React.memo(() => (
        <div className="space-y-3">
            <div className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span className="text-sm font-medium">User Settings</span>
            </div>

            <Card className="p-3 space-y-3">
                <div>
                    <label className="text-xs font-medium text-muted-foreground">
                        User ID
                    </label>
                    <p className="text-sm font-mono break-all">{userId}</p>
                </div>

                <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRegenerateUserId}
                    className="w-full gap-2"
                >
                    <Bot className="h-3 w-3" />
                    New Session
                </Button>
            </Card>
        </div>
    ))

    return (
        <div className={`
      flex flex-col h-full bg-card
      ${isMobile ? 'w-full' : ''}
    `}>
            {/* Header */}
            <div className="p-4 border-b">
                <Button
                    onClick={handleNewConversation}
                    className="w-full gap-2"
                    size="sm"
                >
                    <Plus className="h-4 w-4" />
                    New Conversation
                </Button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-hidden p-4 space-y-6">
                <ConversationHistory />

                <Separator />

                <UserSection />
            </div>

            {/* Footer */}
            <div className="p-4 border-t">
                <div className="text-xs text-muted-foreground text-center">
                    <p>WonderAI v1.0</p>
                    <p>Built with React 19 & FastAPI</p>
                </div>
            </div>
        </div>
    )
})

Sidebar.displayName = 'Sidebar'
