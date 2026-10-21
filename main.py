import telebot
from telebot import types
import threading
import http.server
import socketserver

# --- بخش وب‌سرور برای روشن نگه داشتن ربات (مخصوص Render) ---
PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is active and running 24/7!")

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# اجرای سرور در یک نخ (Thread) جداگانه تا جلوی ربات تلگرام را نگیرد
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# --- بخش اصلی ربات تلگرام ---
TOKEN = "توکن_ربات_خودت_را_اینجا_بگذار"
bot = telebot.TeleBot(TOKEN)

# دیتابیس ساده برای ذخیره اطلاعات بازی کاربران
users_data = {}

def get_user(chat_id):
    if chat_id not in users_data:
        users_data[chat_id] = {
            "gold": 1000,
            "diamonds": 10,
            "factories": {"kashan": 0, "qainat": 0, "lahijan": 0, "khuzestan": 0, "rafsanjan": 0},
            "house_level": 1
        }
    return users_data[chat_id]

@bot.message_handler(commands=['start'])
def send_welcome(chat_id):
    # اگر از طریق کالبک یا پیام مستقیم باشد
    pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text
    user = get_user(chat_id)

    # دستورات اونر (برای شما و دوستتون)
    if text in ["من اونرم", "اونر شو"] and chat_id in [7409520835, 1792505230]:
        user["gold"] = 5000000000
        user["diamonds"] = 100000
        user["house_level"] = 10
        user["factories"]["kashan"] = 50
        user["factories"]["qainat"] = 50
        user["factories"]["lahijan"] = 50
        user["factories"]["khuzestan"] = 50
        user["factories"]["rafsanjan"] = 50
        bot.reply_to(message, "👑 مقام اونری فعال شد! ۵ میلیارد طلا، ۱۰۰ هزار الماس و تمامی کارخانه‌ها و خانه‌ها مکس شدند.")
        return

    if text == "شروع" or text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💰 دارایی من", "🏭 کارخانه‌ها")
        markup.add("🏠 خانه", "👑 من اونرم")
        bot.reply_to(message, "به بازی **تاج و تیغ (ایران تایکون)** خوش آمدید! امپراتوری خود را بسازید.", reply_markup=markup)
    
    elif text == "💰 دارایی من":
        bot.reply_to(message, f"💰 طلا: {user['gold']}\n💎 الماس: {user['diamonds']}\n🏠 سطح خانه: {user['house_level']}")
    
    elif text == "🏭 کارخانه‌ها":
        f = user["factories"]
        msg = f"🏭 وضعیت کارخانه‌های شما:\n🧶 فرش کاشان: {f['kashan']}\n🌾 زعفران قائنات: {f['qainat']}\n🍵 چای لاهیجان: {f['lahijan']}\n🛢️ نفت خوزستان: {f['khuzestan']}\n🥜 پسته رفسنجان: {f['rafsanjan']}"
        bot.reply_to(message, msg)
    
    elif text == "🏠 خانه":
        bot.reply_to(message, f"🏠 خانه‌ی شما در سطح {user['house_level']} قرار دارد.")

# شروع به کار ربات
bot.infinity_polling()
