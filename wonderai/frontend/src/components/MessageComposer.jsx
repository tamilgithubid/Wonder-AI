import React, {
    useState,
    useCallback,
    useRef,
    useEffect,
    useActionState
} from 'react'
import {
    MagicButton,
    MagicTextarea,
    MagicBadge,
    MagicProgress,
    MagicAlert
} from '@/components/magicui'
import {
    Send,
    Paperclip,
    Image as ImageIcon,
    Map as MapIcon,
    Loader2,
    Mic,
    Square,
    Activity
} from 'lucide-react'

/**
 * MessageComposer component using React 19 Actions and useActionState
 * Handles message input, file attachments, and various input methods
 */
export const MessageComposer = React.memo(({
    onSendMessage,
    onStreamMessage,
    disabled = false,
    isLoading = false
}) => {
    const [message, setMessage] = useState('')
    const [attachments, setAttachments] = useState([])
    const [isRecording, setIsRecording] = useState(false)
    const [useStreaming, setUseStreaming] = useState(true)
    const textareaRef = useRef(null)
    const fileInputRef = useRef(null)

    // Action function for form submission
    const submitMessageAction = useCallback(async (previousState, formData) => {
        const messageText = formData.get('message')

        if (!messageText?.trim()) {
            return { error: 'Please enter a message' }
        }

        try {
            if (useStreaming && onStreamMessage) {
                // Use streaming for real-time responses
                await onStreamMessage(messageText)
            } else {
                // Use regular message sending
                await onSendMessage(messageText)
            }
            return { success: true }
        } catch (error) {
            return { error: error.message || 'Failed to send message' }
        }
    }, [useStreaming, onStreamMessage, onSendMessage])

    // React 19 useActionState for form submission
    const [submitState, submitAction, isPending] = useActionState(
        submitMessageAction,
        null
    )

    // Enhanced loading state tracking


    // Auto-resize textarea
    const adjustTextareaHeight = useCallback(() => {
        const textarea = textareaRef.current
        if (textarea) {
            textarea.style.height = 'auto'
            textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
        }
    }, [])

    // Handle input changes
    const handleInputChange = useCallback((e) => {
        setMessage(e.target.value)
        adjustTextareaHeight()
    }, [adjustTextareaHeight])

    // Handle form submission using React 19 Actions pattern
    const handleSubmit = useCallback((e) => {
        e.preventDefault()

        if (!message.trim() || disabled || isPending) return

        const formData = new FormData()
        formData.append('message', message.trim())

        submitAction(formData)

        // Clear form on successful submission
        setMessage('')
        setAttachments([])

        // Reset textarea height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
        }
    }, [message, disabled, isPending, submitAction])

    // Handle keyboard shortcuts
    const handleKeyDown = useCallback((e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }, [handleSubmit])

    // Handle file attachments
    const handleFileUpload = useCallback((e) => {
        const files = Array.from(e.target.files || [])

        const newAttachments = files.map(file => ({
            id: `${Date.now()}_${Math.random()}`,
            file,
            name: file.name,
            type: file.type,
            size: file.size,
        }))

        setAttachments(prev => [...prev, ...newAttachments])

        // Clear file input
        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }, [])

    // Remove attachment
    const removeAttachment = useCallback((attachmentId) => {
        setAttachments(prev => prev.filter(att => att.id !== attachmentId))
    }, [])

    // Voice recording placeholder (future implementation)
    const toggleRecording = useCallback(() => {
        setIsRecording(!isRecording)
        // TODO: Implement voice recording functionality
    }, [isRecording])

    // Quick action buttons
    const QuickActions = React.memo(() => (
        <div className="flex items-center gap-1">
            <MagicButton
                type="button"
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => fileInputRef.current?.click()}
                title="Attach files"
            >
                <Paperclip className="w-4 h-4" />
            </MagicButton>

            <MagicButton
                type="button"
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                title="Generate image"
                onClick={() => {
                    // Auto-fill image generation prompt
                    setMessage(prev => prev + ' [Generate an image of: ]')
                    textareaRef.current?.focus()
                }}
            >
                <ImageIcon className="w-4 h-4" />
            </MagicButton>

            <MagicButton
                type="button"
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                title="Get map"
                onClick={() => {
                    // Auto-fill map request prompt
                    setMessage(prev => prev + ' [Show me a map of: ]')
                    textareaRef.current?.focus()
                }}
            >
                <MapIcon className="w-4 h-4" />
            </MagicButton>

            <MagicButton
                type="button"
                variant="ghost"
                size="icon"
                className={`h-8 w-8 ${isRecording ? 'text-red-500' : ''}`}
                onClick={toggleRecording}
                title={isRecording ? 'Stop recording' : 'Start voice recording'}
            >
                {isRecording ? <Square className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </MagicButton>
        </div>
    ))

    // File input component
    const FileInput = React.memo(() => (
        <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="image/*,text/*,.pdf,.doc,.docx"
            onChange={handleFileUpload}
            className="hidden"
        />
    ))

    // Attachments display
    const AttachmentsDisplay = React.memo(() =>
        attachments.length > 0 && (
            <div className="flex flex-wrap gap-2 p-3 border-b bg-muted/30">
                {attachments.map(attachment => (
                    <MagicBadge
                        key={attachment.id}
                        variant="secondary"
                        className="flex items-center gap-2 px-3 py-1"
                    >
                        <span className="text-xs truncate max-w-32">
                            {attachment.name}
                        </span>
                        <MagicButton
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="h-4 w-4 p-0 hover:bg-transparent"
                            onClick={() => removeAttachment(attachment.id)}
                        >
                            ×
                        </MagicButton>
                    </MagicBadge>
                ))}
            </div>
        )
    )

    // Error display
    const ErrorDisplay = React.memo(() =>
        submitState?.error && (
            <div className="px-4 py-2">
                <MagicAlert variant="error">
                    {submitState.error}
                </MagicAlert>
            </div>
        )
    )

    useEffect(() => {
        adjustTextareaHeight()
    }, [adjustTextareaHeight])

    const isFormDisabled = disabled || isPending || isLoading
    const showSpinner = isPending || isLoading

    // Loading state component
    const LoadingIndicator = React.memo(() => {
        if (!showSpinner) return null

        return (
            <div className="px-4 py-2 border-b bg-muted/30">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>
                        {useStreaming ? 'Starting AI response...' : 'Sending message...'}
                    </span>
                </div>
            </div>
        )
    })

    return (
        <div className="bg-background border-t">
            <ErrorDisplay />
            <LoadingIndicator />
            <AttachmentsDisplay />

            <form onSubmit={handleSubmit} className="p-4">
                <div className="flex items-end gap-3">
                    {/* Quick Actions */}
                    <QuickActions />

                    {/* Message Input */}
                    <div className="flex-1 relative">
                        <MagicTextarea
                            ref={textareaRef}
                            name="message"
                            value={message}
                            onChange={handleInputChange}
                            onKeyDown={handleKeyDown}
                            placeholder={
                                isRecording
                                    ? 'Recording... Press mic to stop'
                                    : 'Type your message... (Enter to send, Shift+Enter for new line)'
                            }
                            disabled={isFormDisabled}
                            className="min-h-[40px] pr-12"
                            autoResize={true}
                            maxHeight={120}
                        />

                        {/* Character count for long messages */}
                        {message.length > 500 && (
                            <div className="absolute bottom-2 right-2 text-xs text-muted-foreground">
                                {message.length}
                            </div>
                        )}
                    </div>

                    {/* Streaming Toggle */}
                    <MagicButton
                        type="button"
                        onClick={() => setUseStreaming(!useStreaming)}
                        size="icon"
                        variant={useStreaming ? "magic" : "outline"}
                        className="h-10 w-10"
                        aria-label={useStreaming ? 'Streaming enabled' : 'Streaming disabled'}
                        title={useStreaming ? 'Streaming enabled' : 'Streaming disabled'}
                        glow={useStreaming}
                    >
                        <Activity className="w-4 h-4" />
                    </MagicButton>

                    {/* Send Button */}
                    <MagicButton
                        type="submit"
                        disabled={isFormDisabled || !message.trim()}
                        size="icon"
                        variant="magic"
                        className="h-10 w-10"
                        aria-label="Send message"
                        shimmer
                        glow
                    >
                        {showSpinner ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <Send className="w-4 h-4" />
                        )}
                    </MagicButton>
                </div>

                {/* Voice Recording Indicator */}
                {isRecording && (
                    <div className="flex items-center gap-2 mt-2 text-sm text-muted-foreground">
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                        <span>Recording... Click mic to stop</span>
                    </div>
                )}
            </form>

            <FileInput />
        </div>
    )
})

MessageComposer.displayName = 'MessageComposer'
