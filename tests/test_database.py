from sqlalchemy import text


async def test_conexao_com_postgres(session):
    result = await session.execute(text('SELECT 1'))

    assert result.scalar_one() == 1
