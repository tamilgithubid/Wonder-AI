import { configureStore } from '@reduxjs/toolkit'
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import chatReducer from './chatSlice'

// API slice with RTK Query for all backend communication
export const api = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://localhost:8000/api',
        prepareHeaders: (headers) => {
            headers.set('Content-Type', 'application/json')
            return headers
        },
    }),
    tagTypes: ['Conversation', 'Message', 'Image', 'Map', 'Health'],
    endpoints: (builder) => ({
        // Health check endpoint
        getHealth: builder.query({
            query: () => '/health',
            providesTags: ['Health'],
        }),

        // Chat/Conversation endpoints
        getConversations: builder.query({
            query: () => '/chat/conversations',
            providesTags: ['Conversation'],
        }),

        createConversation: builder.mutation({
            query: (conversationData) => ({
                url: '/chat/conversations',
                method: 'POST',
                body: conversationData,
            }),
            invalidatesTags: ['Conversation'],
        }),

        getMessages: builder.query({
            query: ({ conversationId, limit = 50, offset = 0 }) =>
                `/chat/conversations/${conversationId}/messages?limit=${limit}&offset=${offset}`,
            providesTags: (result, error, { conversationId }) => [
                { type: 'Message', id: conversationId }
            ],
        }),

        sendMessage: builder.mutation({
            query: ({ conversationId, content, messageType = 'text' }) => ({
                url: `/chat/conversations/${conversationId}/messages`,
                method: 'POST',
                body: { content, message_type: messageType },
            }),
            invalidatesTags: (result, error, { conversationId }) => [
                { type: 'Message', id: conversationId },
                'Conversation'
            ],
        }),

        // Image generation endpoints  
        generateImage: builder.mutation({
            query: ({ prompt, model = 'dall-e-3', size = '1024x1024', quality = 'standard', style = 'natural' }) => ({
                url: '/images/generate',
                method: 'POST',
                body: { prompt, model, size, quality, style },
            }),
            invalidatesTags: ['Image'],
        }),

        analyzeImage: builder.mutation({
            query: ({ imageUrl, prompt = 'What do you see in this image?', model = 'gpt-4o-mini' }) => ({
                url: '/images/analyze',
                method: 'POST',
                body: { image_url: imageUrl, prompt, model },
            }),
        }),

        // Map endpoints
        searchLocations: builder.mutation({
            query: ({ query, limit = 5 }) => ({
                url: '/maps/search',
                method: 'POST',
                body: { query, limit },
            }),
            providesTags: ['Map'],
        }),

        calculateRoute: builder.mutation({
            query: ({ start, end, mode = 'driving' }) => ({
                url: '/maps/route',
                method: 'POST',
                body: { start, end, mode },
            }),
        }),

        generateMap: builder.mutation({
            query: ({ center, zoom = 12, width = 800, height = 600, markers = [], style = 'streets' }) => ({
                url: '/maps/generate',
                method: 'POST',
                body: { center, zoom, width, height, markers, style },
            }),
        }),
    }),
})

// Export hooks for usage in components
export const {
    // Health
    useGetHealthQuery,

    // Conversations
    useGetConversationsQuery,
    useCreateConversationMutation,

    // Messages
    useGetMessagesQuery,
    useSendMessageMutation,

    // Images
    useGenerateImageMutation,
    useAnalyzeImageMutation,

    // Maps
    useSearchLocationsMutation,
    useCalculateRouteMutation,
    useGenerateMapMutation,
} = api

// Configure store with RTK Query and chat slice
export const store = configureStore({
    reducer: {
        chat: chatReducer,
        [api.reducerPath]: api.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [api.reducerPath + '/executeQuery/pending'],
            },
        }).concat(api.middleware),
    devTools: import.meta.env.MODE !== 'production',
})

export default store
