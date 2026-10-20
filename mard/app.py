from http import HTTPStatus

from mard.routers import user
from fastapi import FastAPI

app = FastAPI()

app.include_router(user.router)

@app.get('/', status_code=HTTPStatus.OK)
async def read_root():
    return {'message': 'Olá mundo!'}
