from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import config


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_chat is None:
        return

    if update.effective_chat.id != config.ADMIN_CHAT_ID:
        return

    await update.message.reply_text(
        "🛟 نجات‌دهنده من\n\n"
        "ربات با موفقیت آنلاین شد! 😎\n\n"
        "نسخه: " + config.API_VERSION
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_chat is None:
        return

    if update.effective_chat.id != config.ADMIN_CHAT_ID:
        return

    await update.message.reply_text(
        "ℹ️ راهنما\n\n"
        "/start - شروع ربات\n"
        "/help - نمایش راهنما"
    )


def create_bot() -> Application:
    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    if config.ADMIN_CHAT_ID == 0:
        raise RuntimeError("ADMIN_CHAT_ID is not configured")

    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    return application
