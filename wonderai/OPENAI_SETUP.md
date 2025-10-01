# 🔑 OpenAI API Key Configuration Guide

## Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in to your OpenAI account (or create one)
3. Click "Create new secret key"
4. Copy the key (it starts with "sk-...")
5. Keep this key secure and never commit it to version control!

## Step 2: Configure the Backend

### Option A: Using .env file (Recommended)

1. Copy the example environment file:
   ```bash
   cd /home/hire/Desktop/AI_CHAT_BOT/wonderai/backend
   cp .env.example .env
   ```

2. Edit the .env file and replace `your_openai_api_key_here` with your actual key:
   ```bash
   nano .env
   # or
   code .env
   ```

3. Add your key to the .env file:
   ```env
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   ```

### Option B: Using Environment Variables

1. Export the environment variable in your terminal:
   ```bash
   export OPENAI_API_KEY="sk-your-actual-openai-api-key-here"
   ```

2. Add to your shell profile for persistence:
   ```bash
   echo 'export OPENAI_API_KEY="sk-your-actual-openai-api-key-here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Step 3: Restart the Backend Server

1. Stop the current backend server (Ctrl+C in the terminal)
2. Start it again:
   ```bash
   cd /home/hire/Desktop/AI_CHAT_BOT/wonderai/backend
   python simple_server.py
   ```

## Step 4: Test Real AI Responses

1. Open the frontend: http://localhost:5173
2. Send a message in the chat
3. You should now see real OpenAI responses instead of mock responses!

## Verification

You can verify the configuration by checking the server logs for:
- "OpenAI service initialized" (instead of "OpenAI package not installed" or "API key not configured")
- Real AI responses in the chat interface

## Security Best Practices

✅ **DO:**
- Keep your API key in .env file (not committed to git)
- Use environment variables in production
- Rotate your API keys regularly
- Monitor your OpenAI usage and billing

❌ **DON'T:**
- Commit .env files to version control
- Share your API keys publicly
- Use API keys in client-side code
- Leave unused API keys active

## Models Available

- **Chat:** gpt-4o-mini (fast, cost-effective), gpt-4o (most capable)
- **Embeddings:** text-embedding-3-small (recommended)
- **Images:** dall-e-3 (highest quality)

## Cost Considerations

- gpt-4o-mini: ~$0.0001 per 1K tokens (very affordable)
- gpt-4o: ~$0.005 per 1K tokens (premium)
- text-embedding-3-small: ~$0.00002 per 1K tokens
- dall-e-3: ~$0.04 per image

Monitor your usage at: https://platform.openai.com/usage
