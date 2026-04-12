import uuid
from fastapi import Request, Response

async def get_session_id(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    response.set_cookie(key="session_id", value=session_id,
    httponly=True,
    # secure=True,
    samesite="lax",
    max_age=60*60*24*7, # 1 week
    path="/"
    )
    return session_id
