# Google Chat OpenAI Bot

This bot exposes a `/chat` endpoint for [Google Chat](https://developers.google.com/chat) webhook events and replies using the OpenAI API.
It also includes a `/mcp` endpoint for events from the [GitHub MCP server](https://github.com/github/github-mcp-server).

## Prerequisites

- Node.js 18+
- An OpenAI API key

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Configure environment variables in `.env.local` or your shell:
   ```bash
   OPENAI_API_KEY=your_openai_key
   GOOGLE_CLIENT_EMAIL=service-account-email@project.iam.gserviceaccount.com
   GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   PORT=3978 # optional
   # optional: used when posting events from GitHub MCP server
   MCP_SECRET=your_mcp_secret
   ```
3. Start the bot:
   ```bash
   npm run dev
   ```
4. Expose the port to the internet and configure the URL in your Google Chat app.
5. If using the GitHub MCP server, configure it to POST events to `/mcp` with the shared secret.

When Google Chat or MCP sends a message, the bot returns the OpenAI response generated using the ChatGPT model.
