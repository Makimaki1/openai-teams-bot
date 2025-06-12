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


class GroupRequest(BaseModel):
    group_email: str


class GroupMemberCheckRequest(BaseModel):
    user_email: str
    group_email: str


@app.post("/send_message")
async def send_message(req: MessageRequest):
    try:
        result = google_chat.send_message(req.space_id, req.text)
        return {"message": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/fetch_users")
async def fetch_users(req: SpaceRequest):
    try:
        users = google_chat.fetch_users(req.space_id)
        return {"users": users}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/list_channels")
async def list_channels():
    try:
        spaces = google_chat.list_channels()
        return {"channels": spaces}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/is_group_member")
async def is_group_member(req: GroupMemberCheckRequest):
    try:
        result = google_chat.is_group_member(req.user_email, req.group_email)
        return {"is_member": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/list_group_members")
async def list_group_members(req: GroupRequest):
    try:
        members = google_chat.list_group_members(req.group_email)
        return {"members": members}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, reload=True)
