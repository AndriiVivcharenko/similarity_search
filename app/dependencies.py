from typing import Annotated

from fastapi import Header, HTTPException

from app.config import settings


async def get_token_header(x_token: Annotated[str, Header(description="Secret token for auth")] = ""):
    if x_token != settings.x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")