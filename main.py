import os

from fastapi import FastAPI, Request

from bot import create_bot
from database import initialize_database
from routers.device_router import router as device_router


app = FastAPI(
    title="NajatDehande",
    version="0.2.0"
)

app.include_router(device_router)

bot = create_bot()


@app.on_event("startup")
async def startup_event():
    initialize_database()

    await bot.initialize()

    webhook_url = os.getenv("WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError("WEBHOOK_URL is not configured")

    await bot.bot.set_webhook(
        url=f"{webhook_url}/telegram/webhook"
    )

    await bot.start()


@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()
    await bot.shutdown()


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    from telegram import Update

    update = Update.de_json(
        data,
        bot.bot
    )

    await bot.process_update(update)

    return {"ok": True}


@app.get("/")
async def root():
    return {
        "project": "NajatDehande",
        "status": "online",
        "version": "0.2.0"
    }
