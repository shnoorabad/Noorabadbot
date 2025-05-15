import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "توکن ربات تلگرام اینجا"
OPENAI_API_KEY = "توکن ChatGPT API اینجا"

openai.api_key = OPENAI_API_KEY

reply_keyboard = [
    ["ساعات کاری شهرداری", "آدرس شهرداری"],
    ["شماره تماس", "ثبت شکایت"],
    ["نحوه دریافت مجوز ساخت", "خروج"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'سلام! خوش آمدید به چت‌بات شهرداری نورآباد. لطفاً یک گزینه را انتخاب کنید:',
        reply_markup=markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message == "خروج":
        await update.message.reply_text("خدانگهدار! همیشه در خدمت شما هستم.")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "شما چت‌بات شهرداری نورآباد هستید. سوالات شهری پاسخ دهید."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply, reply_markup=markup)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()