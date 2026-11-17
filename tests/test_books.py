from http import HTTPStatus


async def test_create_book(client, romancist):
    response = await client.post(
        '/books/',
        json={
            'title': 'Dom Casmurro',
            'year': 1899,
            'romancist_id': romancist.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Dom Casmurro',
        'year': 1899,
        'romancist_id': romancist.id,
    }


async def test_create_book_romancist_not_found(client):
    response = await client.post(
        '/books/',
        json={'title': 'Dom Casmurro', 'year': 1899, 'romancist_id': 1},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found'}


async def test_create_book_title_conflict(client, book):
    response = await client.post(
        '/books/',
        json={
            'title': book.title,
            'year': 1900,
            'romancist_id': book.romancist_id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book title already exists'}


async def test_read_books(client, book):
    response = await client.get('/books/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'books': [
            {
                'id': book.id,
                'title': book.title,
                'year': book.year,
                'romancist_id': book.romancist_id,
            }
        ]
    }


async def test_find_book(client, book):
    response = await client.get(f'/books/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'title': book.title,
        'year': book.year,
        'romancist_id': book.romancist_id,
    }


async def test_find_book_not_found(client):
    response = await client.get('/books/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}


async def test_update_book(client, book):
    response = await client.put(
        f'/books/{book.id}',
        json={
            'title': 'Memórias Póstumas',
            'year': 1881,
            'romancist_id': book.romancist_id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'title': 'Memórias Póstumas',
        'year': 1881,
        'romancist_id': book.romancist_id,
    }


async def test_update_book_not_found(client, romancist):
    response = await client.put(
        '/books/1',
        json={
            'title': 'Memórias Póstumas',
            'year': 1881,
            'romancist_id': romancist.id,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}


async def test_update_book_romancist_not_found(client, book):
    response = await client.put(
        f'/books/{book.id}',
        json={
            'title': 'Memórias Póstumas',
            'year': 1881,
            'romancist_id': 999,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found'}


async def test_update_book_title_conflict(client, book, romancist):
    await client.post(
        '/books/',
        json={
            'title': 'Outro Livro',
            'year': 1900,
            'romancist_id': romancist.id,
        },
    )

    response = await client.put(
        f'/books/{book.id}',
        json={
            'title': 'Outro Livro',
            'year': 1900,
            'romancist_id': romancist.id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book title already exists'}


async def test_delete_book(client, book):
    response = await client.delete(f'/books/{book.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


async def test_delete_book_not_found(client):
    response = await client.delete('/books/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}
