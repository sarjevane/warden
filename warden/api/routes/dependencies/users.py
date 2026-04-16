from typing import Annotated

from fastapi import Depends, FastAPI, Request

from warden.lib.config import UsersConfig


def init_users(app: FastAPI, user_config: UsersConfig):
    app.state.users_config = user_config


def get_config(request: Request) -> UsersConfig:
    conf = getattr(request.app.state, "users_config", None)
    if conf is None:
        raise RuntimeError(
            "Config not initialized. init_users(app, ...) was not called."
        )
    return conf


UsersConfigDep = Annotated[UsersConfig, Depends(get_config)]
