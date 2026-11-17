from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mard.database import get_session
from mard.models import Romancist
from mard.schema import (
    FilterPage,
    RomancistList,
    RomancistPublic,
    RomancistSchema,
)

router = APIRouter(prefix='/romancists', tags=['romancists'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=RomancistPublic
)
async def create_romancist(romancist: RomancistSchema, session: SessionDep):
    db_romancist = await session.scalar(
        select(Romancist).where(Romancist.name == romancist.name)
    )

    if db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancist already exists',
        )

    db_romancist = Romancist(name=romancist.name)

    session.add(db_romancist)
    await session.commit()
    await session.refresh(db_romancist)

    return db_romancist


@router.get('/', status_code=HTTPStatus.OK, response_model=RomancistList)
async def read_romancists(
    session: SessionDep, filter_romancists: Annotated[FilterPage, Query()]
):
    query = await session.scalars(
        select(Romancist)
        .offset(filter_romancists.offset)
        .limit(filter_romancists.limit)
    )

    return {'romancists': query.all()}


@router.get(
    '/{romancist_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistPublic,
)
async def find_romancist(romancist_id: int, session: SessionDep):
    db_romancist = await session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Romancist not found')

    return db_romancist


@router.put(
    '/{romancist_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistPublic,
)
async def update_romancist(
    romancist_id: int, romancist: RomancistSchema, session: SessionDep
):
    db_romancist = await session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Romancist not found')

    db_conflict = await session.scalar(
        select(Romancist).where(
            Romancist.id != romancist_id,
            Romancist.name == romancist.name,
        )
    )

    if db_conflict:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancist already exists',
        )

    db_romancist.name = romancist.name

    await session.commit()
    await session.refresh(db_romancist)

    return db_romancist


@router.delete('/{romancist_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_romancist(romancist_id: int, session: SessionDep):
    db_romancist = await session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Romancist not found')

    await session.delete(db_romancist)
    await session.commit()
