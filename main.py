import uvicorn
from fastapi import FastAPI

from core import LOGGING
from modules import routers
from modules.bot import setup_bot

app = FastAPI(title='ZenMoney Telegram Bot')
for router in routers:
    app.include_router(router)


@app.on_event('startup')
async def startup():
    await setup_bot()


@app.on_event('shutdown')
async def shutdown():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=LOGGING)
