from http import HTTPStatus

from sqlalchemy import select

from mard.models import User
from mard.security import verify_password


async def test_create_user(client):
    response = await client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@email.com',
        'id': 1,
    }


async def test_create_user_hashes_password(client, session):
    await client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste@email.com',
            'password': '123456',
        },
    )

    db_user = await session.scalar(
        select(User).where(User.username == 'teste')
    )

    assert db_user.password != '123456'
    assert verify_password('123456', db_user.password)


async def test_users_conflict_error_email(client, user):
    response = await client.post(
        '/users/',
        json={
            'username': 'testt',
            'email': user.email,
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


async def test_users_conflict_error_username(client, user):
    response = await client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'test@test.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


async def test_read_users(client, user):
    response = await client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': user.id, 'username': user.username, 'email': user.email}
        ]
    }


async def test_find_user(client, user):
    response = await client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


async def test_find_user_not_found(client):
    response = await client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


async def test_update_user(client, user):
    response = await client.put(
        f'/users/{user.id}',
        json={
            'username': 'lucas_novo',
            'email': 'lucas_novo@email.com',
            'password': '654321',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'lucas_novo',
        'email': 'lucas_novo@email.com',
    }
    assert verify_password('654321', user.password)


async def test_update_user_not_found(client):
    response = await client.put(
        '/users/1',
        json={
            'username': 'lucas_novo',
            'email': 'lucas_novo@email.com',
            'password': '654321',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


async def test_update_user_conflict_email(client, user):
    await client.post(
        '/users/',
        json={
            'username': 'outro',
            'email': 'outro@email.com',
            'password': '123456',
        },
    )

    response = await client.put(
        f'/users/{user.id}',
        json={
            'username': 'lucas_novo',
            'email': 'outro@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


async def test_update_user_conflict_username(client, user):
    await client.post(
        '/users/',
        json={
            'username': 'outro',
            'email': 'outro@email.com',
            'password': '123456',
        },
    )

    response = await client.put(
        f'/users/{user.id}',
        json={
            'username': 'outro',
            'email': 'lucas_novo@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


async def test_delete_user(client, user):
    response = await client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


async def test_delete_user_not_found(client):
    response = await client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
