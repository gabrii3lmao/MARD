from http import HTTPStatus


async def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = await client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}
