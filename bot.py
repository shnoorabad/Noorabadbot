import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# دریافت کلیدها از محیط
TELEGRAM_BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_KEY"]
openai.api_key = OPENAI_API_KEY

# کیبورد اولیه
reply_keyboard = [
    ["آدرس شهرداری", "ساعات کاری شهرداری"],
    ["ثبت شکایت", "شماره تماس"],
    ["نحوه دریافت مجوز ساخت", "خروج"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام، به ربات شهرداری نورآباد خوش آمدید.", reply_markup=markup)

# پاسخ به دکمه‌ها و سوالات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    predefined_responses = {
        "آدرس شهرداری": "نورآباد، میدان اصلی، ساختمان شهرداری.",
        "ساعات کاری شهرداری": "شنبه تا چهارشنبه از ۸ صبح تا ۲ بعدازظهر.",
        "ثبت شکایت": "لطفاً شکایت خود را تایپ و ارسال نمایید.",
        "شماره تماس": "۰۶۶۳۲۵۵۲۲۰۰",
        "نحوه دریافت مجوز ساخت": "برای دریافت مجوز ساخت به واحد شهرسازی مراجعه نمایید.",
        "خروج": "خدانگهدار!"
    }

    if user_message in predefined_responses:
        await update.message.reply_text(predefined_responses[user_message])
    else:
        # ارسال سؤال به OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            reply = response["choices"][0]["message"]["content"]
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("خطایی رخ داد. لطفاً بعداً تلاش کنید.")

# اجرای برنامه
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
