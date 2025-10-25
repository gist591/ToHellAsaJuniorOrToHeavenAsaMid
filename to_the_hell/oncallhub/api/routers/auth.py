from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from to_the_hell.oncallhub.api.deps.auth import get_current_user
from to_the_hell.oncallhub.api.schemas.user import (
    RefreshTokenSchema,
    TokenPairSchema,
    UserLoginSchema,
)
from to_the_hell.oncallhub.domain.services.auth_service import (
    create_token_pair,
    get_password_hash,
    refresh_access_token,
    verify_password,
)
from to_the_hell.oncallhub.domain.services.auth_service import logout as logout_user

router = APIRouter()

FAKE_USERS_DB: dict[str, dict[str, Any]] = {
    "john": {
        "id": 123,
        "username": "john",
        "email": "john@example.com",
        "hashed_password": get_password_hash("secret"),
    }
}


@router.post("/login", response_model=TokenPairSchema)
async def login(user_data: UserLoginSchema) -> TokenPairSchema:
    """
    Login - get tokens
    """
    user = FAKE_USERS_DB.get(user_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    hashed_password: str = user["hashed_password"]
    assert isinstance(hashed_password, str)

    if not verify_password(user_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token, refresh_token = create_token_pair(user["id"], user["username"])

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=dict[str, str])
async def refresh_token(token_data: RefreshTokenSchema) -> dict[str, str]:
    """
    Refresh access token
    """
    new_access = refresh_access_token(token_data.refresh_token)

    if not new_access:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    return {"access_token": new_access, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    token_data: RefreshTokenSchema,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    """
    Logout - revoken refresh token
    """
    logout_user(token_data.refresh_token)
    return {"detail": "Successfully logged out"}


@router.get("/me")
async def get_me(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Get current user
    """
    return current_user
