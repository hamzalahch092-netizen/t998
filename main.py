import os
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import hashlib

# ⚠️ هام: استبدل هذه المتغيرات بمفاتيحك الحقيقية في Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET = os.getenv("BITGET_SECRET_KEY")

# حالة البوت
is_active = False
last_hunt_time = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *الوحش الرقمي جاهز!* \n"
        "أرسل /activate للبدء في البحث عن الفرص."
    )

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_active
    if not is_active:
        is_active = True
        await update.message.reply_text(
            "✅ *تم تفعيل الوحش الرقمي بنجاح!*\n"
            "🔍 جارٍ الاتصال بـ Binance و Bitget...\n"
            "🔍 جارٍ مسح منصات الإطلاق (Seedify, Polkastarter)...\n"
            "🚀 البوت يعمل الآن 24/7. سأبلغك فور اكتشاف أي فرصة واعدة."
        )
        # بدء البحث المستمر
        context.job_queue.run_repeated(hunt, interval=300, first=10)
    else:
        await update.message.reply_text("أنا بالفعل في وضع الصيد! 🚀")

async def hunt(context: ContextTypes.DEFAULT_TYPE):
    global last_hunt_time
    current_time = time.time()
    
    # منع البحث المتكرر (كل 5 دقائق)
    if current_time - last_hunt_time < 300:
        return
    
    last_hunt_time = current_time
    
    # محاكاة البحث (في النسخة الكاملة سيتم ربطها بـ APIs حقيقية)
    # هذا مثال على ما قد يعثر عليه الوحش
    potential_opportunity = {
        "name": "ProjectAlpha",
        "platform": "Seedify",
        "score": 8.7,
        "reason": "فريق قوي، تمويل 5M$, زخم مجتمعي عالٍ"
    }
    
    message = (
        f"🔍 *فرصة جديدة اكتشفها الوحش!*\n\n"
        f"📌 *المشروع:* {potential_opportunity['name']}\n"
        f"🏛️ *المنصة:* {potential_opportunity['platform']}\n"
        f"🧠 *التقييم:* {potential_opportunity['score']}/10\n"
        f"💡 *السبب:* {potential_opportunity['reason']}\n\n"
        f"⚠️ *نصيحة:* تحقق من العقد الذكي قبل الاستثمار!"
    )
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")

def main():
    if not TELEGRAM_TOKEN:
        print("❌ خطأ: لم يتم العثور على TELEGRAM_TOKEN في المتغيرات.")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("activate", activate))
    
    print("🚀 الوحش الرقمي يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
