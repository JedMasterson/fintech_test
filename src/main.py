from fastapi import FastAPI
from src.db import database
from src import records
import uvicorn

app = FastAPI()


async def lifespan(app: app):
    database.connect()
    yield
    database.dispose()


@app.get('/passport_check/')
async def passport_check(series: int | None = None, number: int | None = None):
    pass_status = await records.passport_check(series, number)
    return pass_status


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8075)
