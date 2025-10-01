import React from 'react'
import { Card } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Bot } from 'lucide-react'

/**
 * Loading states for different message sending scenarios
 */
export const MessageLoadingStates = {
    // When message is being sent to backend
    Sending: React.memo(() => (
        <div className="flex justify-end mb-4">
            <Card className="p-3 bg-primary/10 border-primary/20 animate-pulse max-w-[85%]">
                <div className="flex items-center gap-2 text-primary">
                    <div className="w-1 h-4 bg-primary/40 animate-pulse"></div>
                    <span className="text-sm">Sending...</span>
                </div>
            </Card>
        </div>
    )),

    // When streaming is starting
    StreamingStart: React.memo(() => (
        <div className="flex gap-3 mb-4">
            <Avatar className="w-8 h-8 mt-1 shrink-0">
                <AvatarFallback className="bg-secondary text-secondary-foreground">
                    <Bot className="w-4 h-4" />
                </AvatarFallback>
            </Avatar>
            <Card className="p-3 bg-blue-50/50 border-blue-200 dark:bg-blue-950/20 dark:border-blue-800 max-w-[85%]">
                <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400">
                    <div className="w-1 h-4 bg-blue-500 animate-pulse"></div>
                    <span className="text-sm">Starting response...</span>
                </div>
            </Card>
        </div>
    )),

    // General error state
    Error: React.memo(({ message = 'Something went wrong' }) => (
        <div className="flex gap-3 mb-4">
            <Avatar className="w-8 h-8 mt-1 shrink-0">
                <AvatarFallback className="bg-destructive text-destructive-foreground">
                    <Bot className="w-4 h-4" />
                </AvatarFallback>
            </Avatar>
            <Card className="p-3 bg-destructive/10 border-destructive/20 max-w-[85%]">
                <div className="text-sm text-destructive">
                    {message}
                </div>
            </Card>
        </div>
    ))
}
