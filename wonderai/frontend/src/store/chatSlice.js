import { createSlice } from '@reduxjs/toolkit'

/**
 * Initial state for the chat slice following Redux Toolkit patterns
 * Includes optimistic updates support for React 19 useOptimistic integration
 */
const initialState = {
    messages: [],
    currentConversation: null,
    streamingMessage: null,
    isConnected: false,
    isStreaming: false,
    error: null,
    userId: localStorage.getItem('wonderai_user_id') || `user_${Date.now()}`,

    // UI state
    isSidebarOpen: true,
    currentView: 'chat', // 'chat', 'images', 'maps'

    // Optimistic updates state
    optimisticMessages: [],
    pendingActions: [],
}

/**
 * Chat slice with actions for managing chat state
 * Uses React 19 compatible patterns for optimistic updates
 */
const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        // Connection management
        setConnectionStatus: (state, action) => {
            state.isConnected = action.payload
            if (!action.payload) {
                state.isStreaming = false
                state.streamingMessage = null
            }
        },

        // Message management
        addMessage: (state, action) => {
            const message = {
                id: action.payload.id || `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                role: action.payload.role, // 'user' or 'assistant'
                text: action.payload.text,
                images: action.payload.images || [],
                map: action.payload.map || null,
                timestamp: action.payload.timestamp || new Date().toISOString(),
                metadata: action.payload.metadata || {},
            }

            state.messages.push(message)

            // Clear optimistic message if this is the real response
            if (message.role === 'assistant') {
                state.optimisticMessages = state.optimisticMessages.filter(
                    optMsg => optMsg.pendingId !== action.payload.pendingId
                )
            }
        },

        // Optimistic updates for React 19 useOptimistic hook integration
        addOptimisticMessage: (state, action) => {
            const optimisticMessage = {
                id: `optimistic_${Date.now()}`,
                pendingId: action.payload.pendingId,
                role: action.payload.role,
                text: action.payload.text,
                images: action.payload.images || [],
                timestamp: new Date().toISOString(),
                isOptimistic: true,
            }

            state.optimisticMessages.push(optimisticMessage)
        },

        removeOptimisticMessage: (state, action) => {
            state.optimisticMessages = state.optimisticMessages.filter(
                msg => msg.pendingId !== action.payload.pendingId
            )
        },

        // Streaming support
        setStreamingMessage: (state, action) => {
            state.streamingMessage = action.payload
            state.isStreaming = !!action.payload
        },

        updateStreamingMessage: (state, action) => {
            if (state.streamingMessage) {
                state.streamingMessage = {
                    ...state.streamingMessage,
                    text: action.payload.text,
                    images: action.payload.images || state.streamingMessage.images,
                    map: action.payload.map || state.streamingMessage.map,
                }
            }
        },

        completeStreamingMessage: (state) => {
            if (state.streamingMessage) {
                // Add the completed streaming message to regular messages
                state.messages.push({
                    ...state.streamingMessage,
                    id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    timestamp: new Date().toISOString(),
                })

                state.streamingMessage = null
                state.isStreaming = false
            }
        },

        // Error handling
        setError: (state, action) => {
            state.error = action.payload
        },

        clearError: (state) => {
            state.error = null
        },

        // UI state management
        toggleSidebar: (state) => {
            state.isSidebarOpen = !state.isSidebarOpen
        },

        setCurrentView: (state, action) => {
            state.currentView = action.payload
        },

        // Conversation management
        setCurrentConversation: (state, action) => {
            state.currentConversation = action.payload
        },

        clearCurrentConversation: (state) => {
            state.messages = []
            state.streamingMessage = null
            state.optimisticMessages = []
            state.currentConversation = null
            state.isStreaming = false
        },

        // User management
        setUserId: (state, action) => {
            state.userId = action.payload
            localStorage.setItem('wonderai_user_id', action.payload)
        },

        // Pending actions for optimistic updates
        addPendingAction: (state, action) => {
            state.pendingActions.push({
                id: action.payload.id,
                type: action.payload.type,
                timestamp: Date.now(),
            })
        },

        removePendingAction: (state, action) => {
            state.pendingActions = state.pendingActions.filter(
                pendingAction => pendingAction.id !== action.payload.id
            )
        },
    },
})

// Action creators
export const {
    setConnectionStatus,
    addMessage,
    addOptimisticMessage,
    removeOptimisticMessage,
    setStreamingMessage,
    updateStreamingMessage,
    completeStreamingMessage,
    setError,
    clearError,
    toggleSidebar,
    setCurrentView,
    setCurrentConversation,
    clearCurrentConversation,
    setUserId,
    addPendingAction,
    removePendingAction,
} = chatSlice.actions

// Selectors with memoization for performance
export const selectAllMessages = (state) => state.chat.messages
export const selectOptimisticMessages = (state) => state.chat.optimisticMessages
export const selectStreamingMessage = (state) => state.chat.streamingMessage
export const selectIsConnected = (state) => state.chat.isConnected
export const selectIsStreaming = (state) => state.chat.isStreaming
export const selectError = (state) => state.chat.error
export const selectUserId = (state) => state.chat.userId
export const selectIsSidebarOpen = (state) => state.chat.isSidebarOpen
export const selectCurrentView = (state) => state.chat.currentView
export const selectCurrentConversation = (state) => state.chat.currentConversation
export const selectPendingActions = (state) => state.chat.pendingActions

// Combined selector for all visible messages (regular + optimistic + streaming)
export const selectVisibleMessages = (state) => {
    const regularMessages = selectAllMessages(state)
    const optimisticMessages = selectOptimisticMessages(state)
    const streamingMessage = selectStreamingMessage(state)

    const allMessages = [...regularMessages, ...optimisticMessages]

    if (streamingMessage) {
        allMessages.push(streamingMessage)
    }

    return allMessages.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
}

export default chatSlice.reducer
