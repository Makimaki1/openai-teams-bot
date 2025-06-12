# FastAPI MCP Server

This Python service exposes Google Chat functionality as simple tools for the MCP ecosystem.
It uses Google OAuth service account credentials and provides three endpoints:

- `POST /send_message` – send a text message to a space.
- `POST /fetch_users` – retrieve members in a space.
- `GET  /list_channels` – list spaces available to the bot.

All Google Chat API calls are run in a thread pool using FastAPI's
`run_in_threadpool` helper so the async endpoints remain non-blocking.

## Setup

1. Create a service account in Google Cloud and enable the Chat API.
2. Download the service account key JSON file and set `GOOGLE_SERVICE_ACCOUNT_FILE` to its path.
3. Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn mcp_server.main:app --reload
```

The service account must be added to the desired chat spaces so it can post messages and read membership information.
