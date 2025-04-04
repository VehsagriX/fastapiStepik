from fastapi import Depends, HTTPException, status


from src.security import get_user_from_token
from src.database import get_user
from src.schemas.user_schemas import User


async def get_current_user(username: str = Depends(get_user_from_token))-> User:
    user = await get_user(username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
