  import os
    import sqlite3
    import openai
    from datetime import datetime, timedelta
    from telegram import Update, ReplyKeyboardMarkup
    from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

    TELEGRAM_BOT_TOKEN = os.environ["BOT_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_KEY"]
    openai.api_key = OPENAI_API_KEY

    # اتصال به دیتابیس
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_limits (
        user_id INTEGER PRIMARY KEY,
        count INTEGER,
        reset_time TEXT
    )
    """)
    conn.commit()

    # محدودیت روزانه
    def is_user_allowed(user_id):
        now = datetime.now()
        cursor.execute("SELECT count, reset_time FROM user_limits WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("INSERT INTO user_limits VALUES (?, ?, ?)", (user_id, 1, (now + timedelta(days=1)).isoformat()))
            conn.commit()
            return True
        else:
            count, reset_time = row
            reset_time_dt = datetime.fromisoformat(reset_time)
            if now > reset_time_dt:
                cursor.execute("UPDATE user_limits SET count = ?, reset_time = ? WHERE user_id = ?", (1, (now + timedelta(days=1)).isoformat(), user_id))
                conn.commit()
                return True
            elif count < 10:
                cursor.execute("UPDATE user_limits SET count = ? WHERE user_id = ?", (count + 1, user_id))
                conn.commit()
                return True
            else:
                return False

    # کیبورد
    keyboard = [
        ["شهردار", "ساعات کاری"],
        ["آدرس شهرداری", "شماره تماس"],
        ["درباره ما", "ثبت شکایت"],
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("سلام! به ربات رسمی شهرداری نورآباد دلفان خوش آمدید.", reply_markup=markup)

    # مدیریت پیام‌ها
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text

        if not is_user_allowed(user_id):
            await update.message.reply_text("شما امروز به حداکثر ۱۰ سؤال رسیدید. لطفاً فردا دوباره امتحان کنید.")
            return

        # پاسخ‌های ثابت
        if text == "شهردار":
            await update.message.reply_text("شهردار نورآباد: آقای مرادپور")
        elif text == "ساعات کاری":
            await update.message.reply_text("ساعات کاری شهرداری: شنبه تا چهارشنبه، از ساعت ۶ صبح تا ۱۳.")
        elif text == "آدرس شهرداری":
            await update.message.reply_text("خیابان کشاورز، ساختمان شهرداری
[مشاهده در نقشه گوگل](https://maps.google.com)", parse_mode="Markdown")
        elif text == "شماره تماس":
            await update.message.reply_text("۰۶۶۳۲۷۲۴۰۵۷-۸")
        elif text == "درباره ما":
            await update.message.reply_text("طراحی و تدوین: علی معصومی‌پور")
        elif text == "ثبت شکایت":
            await update.message.reply_text("لطفاً شکایت خود را تایپ و ارسال کنید.")
        else:
            try:
                chat = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "شما ربات پاسخگوی شهرداری نورآباد دلفان هستید. پاسخ‌ها باید محترمانه و دقیق باشد."},
                        {"role": "user", "content": text}
                    ]
                )
                reply = chat.choices[0].message.content
                await update.message.reply_text(reply)
            except Exception as e:
                await update.message.reply_text("خطایی در ارتباط با هوش مصنوعی رخ داد.")

    if __name__ == "__main__":
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
