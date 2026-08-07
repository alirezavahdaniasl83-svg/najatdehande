import asyncio

from fastapi import FastAPI

from bot import create_bot
from database import initialize_database


app = FastAPI(
    title="NajatDehande",
    version="0.2.0"
)


@app.on_event("startup")
async def startup_event():
    initialize_database()

    bot = create_bot()

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()


@app.on_event("shutdown")
async def shutdown_event():
    # فعلاً Railway خودش پروسه را مدیریت می‌کند.
    pass


@app.get("/")
async def root():
    return {
        "project": "NajatDehande",
        "status": "online",
        "version": "0.2.0"
    }
