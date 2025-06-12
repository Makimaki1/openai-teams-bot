# GoogleChat MCP Server

This repository contains two components:

1. **Google Chat Bot (Node.js)** – see [bot/README.md](./bot/README.md) for instructions on running the existing Express-based bot that integrates with the OpenAI API.
2. **FastAPI MCP Server (Python)** – a lightweight server exposing Google Chat functionality as MCP tools.

The FastAPI server provides endpoints for sending messages, fetching users, and listing channels using Google OAuth credentials.  See [mcp_server/README.md](./mcp_server/README.md) for setup details.

If you need a Microsoft Teams bot, see the [ChatGPT Teams Bot app](https://github.com/formulahendry/chatgpt-teams-bot) which uses the latest `gpt-3.5-turbo` model.

![OpenAI](./bot/images/openai-chat.png)

## Testing

Install Python dependencies and run all tests (Node and Python) with:

```bash
npm install --prefix bot
pip install -r mcp_server/requirements.txt
pip install pytest
npm test
```

This runs the Jest tests in `bot/` and the Pytest suite under `mcp_server/tests`.
