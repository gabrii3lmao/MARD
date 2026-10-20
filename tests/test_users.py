from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/', json={
            'username': 'teste',
            'email': 'teste@email.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@email.com',
        'id': 1
    }
