from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import config


MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["📱 دستگاه‌ها"],
        ["⚙️ تنظیمات", "ℹ️ اطلاعات"],
    ],
    resize_keyboard=True
)


def is_admin(update: Update) -> bool:
    return (
        update.effective_chat is not None
        and update.effective_chat.id == config.ADMIN_CHAT_ID
    )


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_admin(update):
        return

    await update.message.reply_text(
        "🛟 نجات‌دهنده من\n\n"
        "سیستم آماده است 😎\n"
        "از منوی زیر انتخاب کن:",
        reply_markup=MAIN_MENU
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_admin(update):
        return

    await update.message.reply_text(
        "ℹ️ راهنما\n\n"
        "/start - نمایش منوی اصلی\n"
        "/help - نمایش راهنما"
    )


async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not is_admin(update):
        return

    text = update.message.text

    if text == "📱 دستگاه‌ها":
        await update.message.reply_text(
            "📱 دستگاه‌های ثبت‌شده\n\n"
            "فعلاً هیچ دستگاهی ثبت نشده است."
        )

    elif text == "⚙️ تنظیمات":
        await update.message.reply_text(
            "⚙️ تنظیمات\n\n"
            "این بخش در نسخه‌های بعدی فعال می‌شود."
        )

    elif text == "ℹ️ اطلاعات":
        await update.message.reply_text(
            f"🛟 NajatDehande\n"
            f"نسخه: {config.API_VERSION}\n"
            f"وضعیت: 🟢 آنلاین"
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

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_handler
        )
    )

    return application
