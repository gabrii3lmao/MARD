from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mard.database import get_session
from mard.models import User
from mard.schema import UserList, UserPublic, UserSchema, FilterPage

router = APIRouter(prefix='/users', tags=['users'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: SessionDep):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists'
            )

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username already exists'
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: SessionDep, filter_users: Annotated[FilterPage, Query()]
):
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    users = query.all()

    return {'users': users}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def find_user(user_id: int, session: SessionDep):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')

    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.NO_CONTENT, response_model=UserPublic)
async def update_user(user_id: int, user: UserSchema, session: SessionDep):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')
