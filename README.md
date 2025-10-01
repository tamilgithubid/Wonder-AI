# 🤖 WonderAI - Advanced AI Chat Application

A modern, full-stack AI chat application powered by **Google Gemini 2.5 Flash** with real-time streaming responses, beautiful UI/UX, and advanced code display features.

## ✨ Features

### 🚀 **Core Functionality**
- **Real-time Streaming**: Live AI responses with typing indicators
- **Google Gemini 2.5 Flash Integration**: Latest AI model with advanced capabilities  
- **Modern UI/UX**: React 19 with shadcn/ui components
- **Code Syntax Highlighting**: Beautiful code blocks with copy functionality
- **Optimistic Updates**: Instant message feedback using React 19 features

### 💻 **Technical Features**
- **Frontend**: React 19, Vite, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, Python 3.10+, Google Generative AI
- **Streaming**: Server-Sent Events for real-time responses
- **State Management**: Redux Toolkit with modern patterns
- **Loading States**: Comprehensive pending and streaming indicators

### 🎨 **UI/UX Enhancements**
- **Message States**: Sending, streaming, success, and error indicators
- **Code Display**: Syntax highlighting, line numbers, copy/download functionality
- **Responsive Design**: Works on desktop and mobile devices
- **Theme Support**: Light/dark mode compatibility
- **Animations**: Smooth transitions and loading states

## 🛠️ **Quick Start**

### Prerequisites
- Node.js 20.19+ or 22.12+
- Python 3.10+
- Google AI API Key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone the Repository
```bash
git clone git@github.com:tamilgithubid/Wonder-AI.git
cd Wonder-AI
```

### 2. Backend Setup
```bash
cd wonderai/backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Add your Google AI API key to .env
GOOGLE_API_KEY=your_google_ai_api_key_here

# Start the backend server
python simple_server.py
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 **Project Structure**

```
Wonder-AI/
├── wonderai/
│   ├── backend/                 # FastAPI Backend
│   │   ├── app/
│   │   │   ├── api/            # API endpoints
│   │   │   ├── core/           # Configuration & utilities
│   │   │   ├── models/         # Data models
│   │   │   └── services/       # Business logic
│   │   ├── simple_server.py    # Main server file
│   │   └── requirements.txt    # Python dependencies
│   │
│   └── frontend/               # React Frontend
│       ├── src/
│       │   ├── components/     # React components
│       │   ├── hooks/          # Custom hooks
│       │   ├── lib/            # Utilities
│       │   └── store/          # Redux store
│       └── package.json        # Node.js dependencies
└── README.md
```

## 🔧 **Configuration**

### Backend Environment Variables
```env
# Google Gemini Configuration
GOOGLE_API_KEY=your_google_ai_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=text-embedding-004

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS Settings (handled automatically)
```

### Frontend Configuration
The frontend automatically connects to the backend on `localhost:8000`. Update the API base URL in the store configuration if needed.

## 🌟 **Key Features in Detail**

### **Real-time Streaming**
- Uses Server-Sent Events (SSE) for live AI responses
- Visual typing indicators and streaming cursors
- Smooth character-by-character display

### **Enhanced Code Display**
- Automatic language detection from code blocks
- Syntax highlighting for 20+ programming languages
- Line numbers for multi-line code
- One-click copy to clipboard
- File download functionality
- Execution placeholder for supported languages

### **Modern State Management**
- React 19's `useOptimistic` for instant UI updates
- `useTransition` for smooth loading states  
- `useActionState` for form handling
- Redux Toolkit for global state

### **Professional UI/UX**
- Loading spinners and pending states
- Error handling with user feedback
- Responsive design for all screen sizes
- Smooth animations and transitions

## 🔌 **API Endpoints**

### Health Check
```http
GET /api/health
```

### Chat Endpoints
```http
# Send a message
POST /api/chat/conversations/{conversation_id}/messages
Content-Type: application/json
{
  "content": "Your message here"
}

# Stream a response
POST /api/chat/conversations/{conversation_id}/stream
Content-Type: application/json
{
  "content": "Your message here"
}
```

## 🧪 **Testing**

### Backend Testing
```bash
cd wonderai/backend

# Test Gemini integration
python test_gemini_direct.py

# Test API endpoints
python test_api.py
```

### Frontend Testing
```bash
cd wonderai/frontend

# Run tests (when available)
npm test
```

## 🚀 **Deployment**

### Backend Deployment
1. Set up a Python 3.10+ environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run: `python simple_server.py`

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy the `dist` folder to your hosting service
3. Update API endpoints for production

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📝 **License**

This project is open source and available under the [MIT License](LICENSE).

## 🙏 **Acknowledgments**

- **Google Gemini 2.5 Flash** for powerful AI capabilities
- **React 19** for modern frontend features
- **FastAPI** for high-performance backend
- **shadcn/ui** for beautiful UI components
- **Tailwind CSS** for utility-first styling

## 📞 **Support**

If you have any questions or need help, please:
1. Check the [Issues](https://github.com/tamilgithubid/Wonder-AI/issues) page
2. Create a new issue if needed  
3. Contact the maintainers

---

**Made with ❤️ by [tamilgithubid](https://github.com/tamilgithubid)**

🌟 **Star this repository if you found it helpful!**
