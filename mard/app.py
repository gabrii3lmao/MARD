from http import HTTPStatus

from fastapi import FastAPI

from mard.routers import book, romancist, user

app = FastAPI()

app.include_router(user.router)
app.include_router(romancist.router)
app.include_router(book.router)


@app.get('/', status_code=HTTPStatus.OK)
async def read_root():
    return {'message': 'Olá mundo!'}
