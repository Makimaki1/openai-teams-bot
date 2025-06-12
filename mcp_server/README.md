# FastAPI MCP Server

This Python service exposes Google Chat functionality as simple tools for the MCP ecosystem.
It uses Google OAuth service account credentials and provides these endpoints:

- `POST /send_message` – send a text message to a space.
- `POST /fetch_users` – retrieve members in a space.
- `GET  /list_channels` – list spaces available to the bot.
- `POST /is_group_member` – check if a user belongs to a Google Group.
- `POST /list_group_members` – list members of a Google Group.

## Setup

1. Create a service account in Google Cloud and enable the Chat API.
2. Enable the [Admin SDK Directory API](https://developers.google.com/admin-sdk/directory).
3. Download the service account key JSON file and set `GOOGLE_SERVICE_ACCOUNT_FILE` to its path.
4. (Optional) If using domain-wide delegation, set `GOOGLE_ADMIN_SUBJECT` to an admin user's email so the service account can query groups.
5. Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn mcp_server.main:app --reload
```

The service account must be added to the desired chat spaces so it can post messages and read membership information.
If you want to query Google Groups, delegate domain-wide authority to the service account and set `GOOGLE_ADMIN_SUBJECT` accordingly.
