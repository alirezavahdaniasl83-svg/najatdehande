from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_CHAT_ID:
        return

    await update.message.reply_text(
        "🛟 نجات‌دهنده من آنلاین شد 😎"
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
