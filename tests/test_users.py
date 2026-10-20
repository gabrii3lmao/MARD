from http import HTTPStatus


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
