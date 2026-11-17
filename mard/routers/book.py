from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mard.database import get_session
from mard.models import Book, Romancist
from mard.schema import BookList, BookPublic, BookSchema, FilterPage

router = APIRouter(prefix='/books', tags=['books'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def _get_romancist(romancist_id: int, session: AsyncSession):
    db_romancist = await session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Romancist not found')

    return db_romancist


async def _check_title_conflict(
    title: str, session: AsyncSession, book_id: int | None = None
):
    query = select(Book).where(Book.title == title)

    if book_id is not None:
        query = query.where(Book.id != book_id)

    if await session.scalar(query):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Book title already exists',
        )


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(book: BookSchema, session: SessionDep):
    await _get_romancist(book.romancist_id, session)
    await _check_title_conflict(book.title, session)

    db_book = Book(
        title=book.title,
        year=book.year,
        romancist_id=book.romancist_id,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.get('/', status_code=HTTPStatus.OK, response_model=BookList)
async def read_books(
    session: SessionDep, filter_books: Annotated[FilterPage, Query()]
):
    query = await session.scalars(
        select(Book).offset(filter_books.offset).limit(filter_books.limit)
    )

    return {'books': query.all()}


@router.get('/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic)
async def find_book(book_id: int, session: SessionDep):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Book not found')

    return db_book


@router.put('/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic)
async def update_book(book_id: int, book: BookSchema, session: SessionDep):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Book not found')

    await _get_romancist(book.romancist_id, session)
    await _check_title_conflict(book.title, session, book_id)

    db_book.title = book.title
    db_book.year = book.year
    db_book.romancist_id = book.romancist_id

    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_book(book_id: int, session: SessionDep):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Book not found')

    await session.delete(db_book)
    await session.commit()
