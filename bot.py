import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv
from strategies import fetch_price, get_signal

# Load local .env variables (optional for local test)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower().startswith("signal"):
        try:
            symbol = text.split(" ")[1].upper().replace("/","") if len(text.split(" "))>1 else "BTCUSDT"
            price_data = fetch_price(symbol)
            signal = get_signal(price_data)
            # বাংলা reply
            if signal == "BUY":
                reply = f"{symbol} এর জন্য সংকেত: ক্রয় (BUY)"
            elif signal == "SELL":
                reply = f"{symbol} এর জন্য সংকেত: বিক্রয় (SELL)"
            else:
                reply = f"{symbol} এর জন্য সংকেত: অপেক্ষা করুন (HOLD)"
        except Exception as e:
            reply = f"ত্রুটি: {e}"
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": text + " অনুগ্রহ করে বাংলায় উত্তর দাও"}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"ত্রুটি: {e}"

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("বাংলা-enabled Trading AI Bot চালু হলো...")
app.run_polling()            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"ত্রুটি: {e}"

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("বাংলা-enabled Trading AI Bot চালু হলো...")
app.run_polling()
