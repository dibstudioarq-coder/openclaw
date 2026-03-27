import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from anthropic import Anthropic

load_dotenv(dotenv_path='./.env')

ALLOWED_USERS = [5405164096]  # Só você pode usar o bot

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ERRO: ANTHROPIC_API_KEY não encontrada!")
    exit()

client = Anthropic(api_key=api_key)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        print(f"⛔ Acesso negado: {update.effective_user.id}")
        await update.message.reply_text("Acesso negado.")
        return
    
    texto_usuario = update.message.text
    print(f"📩 Recebi: {texto_usuario}")
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": f"Você é o assistente do Dib Studio. Responda de forma curta: {texto_usuario}"}]
        )
        await update.message.reply_text(message.content[0].text)
    except Exception as e:
        print(f"❌ Erro no Claude: {e}")
        await update.message.reply_text("Erro temporário. Tente novamente!")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN não encontrado!")
        exit()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    print("🚀 Assistente Dib Studio Online!")
    app.run_polling()
