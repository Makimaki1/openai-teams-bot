"""FastAPI server exposing Google Chat functions as MCP tools."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from . import google_chat

app = FastAPI(title="Google Chat MCP Server")


class MessageRequest(BaseModel):
    space_id: str
    text: str


class SpaceRequest(BaseModel):
    space_id: str


@app.post("/send_message")
async def send_message(req: MessageRequest):
    try:
        result = await google_chat.send_message_async(req.space_id, req.text)
        return {"message": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/fetch_users")
async def fetch_users(req: SpaceRequest):
    try:
        users = await google_chat.fetch_users_async(req.space_id)
        return {"users": users}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/list_channels")
async def list_channels():
    try:
        spaces = await google_chat.list_channels_async()
        return {"channels": spaces}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, reload=True)
