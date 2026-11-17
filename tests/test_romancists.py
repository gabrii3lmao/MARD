from http import HTTPStatus

from sqlalchemy import select

from mard.models import Book


async def test_create_romancist(client):
    response = await client.post(
        '/romancists/', json={'name': 'Machado de Assis'}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'Machado de Assis'}


async def test_create_romancist_conflict(client, romancist):
    response = await client.post('/romancists/', json={'name': romancist.name})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancist already exists'}


async def test_read_romancists(client, romancist):
    response = await client.get('/romancists/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancists': [{'id': romancist.id, 'name': romancist.name}]
    }


async def test_find_romancist(client, romancist):
    response = await client.get(f'/romancists/{romancist.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancist.id,
        'name': romancist.name,
    }


async def test_find_romancist_not_found(client):
    response = await client.get('/romancists/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found'}


async def test_update_romancist(client, romancist):
    response = await client.put(
        f'/romancists/{romancist.id}', json={'name': 'Assis'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': romancist.id, 'name': 'Assis'}


async def test_update_romancist_not_found(client):
    response = await client.put('/romancists/1', json={'name': 'Assis'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found'}


async def test_update_romancist_conflict(client, romancist):
    await client.post('/romancists/', json={'name': 'Outro Autor'})

    response = await client.put(
        f'/romancists/{romancist.id}', json={'name': 'Outro Autor'}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancist already exists'}


async def test_delete_romancist(client, romancist):
    response = await client.delete(f'/romancists/{romancist.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


async def test_delete_romancist_not_found(client):
    response = await client.delete('/romancists/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found'}


async def test_delete_romancist_cascades_books(client, session, book):
    response = await client.delete(f'/romancists/{book.romancist_id}')

    assert response.status_code == HTTPStatus.NO_CONTENT

    db_book = await session.scalar(select(Book).where(Book.id == book.id))

    assert db_book is None
