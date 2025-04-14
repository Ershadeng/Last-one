from flask import Flask
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

TOKEN = '7816665394:AAFar_7V0dCmaz1xjeGlAy0YO-nhhwzqob0'
bot = telebot.TeleBot(TOKEN)
user_roles = {}
user_sessions = {}
user_counter = set()

@bot.message_handler(commands=['start'])
def send_start(message):
    print(f"/start من: {message.chat.id}")
    user_id = message.chat.id
    if user_id not in user_counter:
        user_counter.add(user_id)
    if user_id in user_sessions:
        bot.send_message(user_id, "رجعنا لك! تبي تكمل من وين وقفت؟")
    else:
        user_sessions[user_id] = True
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("طالب", callback_data="role_male"),
        InlineKeyboardButton("طالبة", callback_data="role_female")
    )
    bot.send_message(
        message.chat.id,
        "ارحب 🫡\n\nاختَر إذا كنت طالب أو طالبة:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(f"زر تم الضغط عليه: {call.data} من {call.message.chat.id}")
    user_id = call.message.chat.id

    if call.data == "role_male":
        user_roles[user_id] = "طالب"
        bot.send_message(user_id, "منور يا أقوى مهندس 🛠️")
        show_main_menu_direct(user_id)

    elif call.data == "role_female":
        user_roles[user_id] = "طالبة"
        bot.send_message(user_id, "منورة يا أروع مهندسة ✨")
        show_main_menu_direct(user_id)

    elif call.data == "main_menu":
        show_main_menu(call)

    elif call.data == "academic":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("التخصصات", callback_data="majors"),
            InlineKeyboardButton("المواد المشتركة", callback_data="common_courses"),
            InlineKeyboardButton("الرجوع", callback_data="main_menu")
        )
        try:
            bot.edit_message_text("القسم الأكاديمي:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data == "non_academic":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("اللجان", callback_data="committees"),
            InlineKeyboardButton("بعض الأندية الأخرى التابعة للعمادة", callback_data="extra_clubs"),
            InlineKeyboardButton("الرجوع", callback_data="main_menu")
        )
        try:
            bot.edit_message_text("القسم غير الأكاديمي:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data == "majors":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("⚡ الكهرباء", callback_data="ee"),
            InlineKeyboardButton("⚙️ الميكانيكا", callback_data="me"),
            InlineKeyboardButton("🏗️ المدنية", callback_data="ce"),
            InlineKeyboardButton("🧪 الكيميائية", callback_data="che"),
            InlineKeyboardButton("🏭 الصناعية", callback_data="ie"),
            InlineKeyboardButton("⛏️ التعدين", callback_data="mining"),
            InlineKeyboardButton("☢️ النووية", callback_data="nuclear"),
            InlineKeyboardButton("✈️ الطيران", callback_data="aero"),
            InlineKeyboardButton("الرجوع", callback_data="academic")
        )
        try:
            bot.edit_message_text("اختر التخصص:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data == "ce":
        bot.send_message(user_id, "الهندسة المدنية تهتم بالمباني، الطرق، الجسور، والسدود. تعتبر من أوسع التخصصات الهندسية ميدانياً.")
        bot.send_message(user_id, "إذا عندك أي استفسار عن الهندسة المدنية، تواصل مع: @s98_l")

    elif call.data in ["ee", "me", "che", "ie", "mining", "nuclear", "aero"]:
        messages = {
            "ee": "⚡ تخصص الكهرباء مستقبل مشرق بالطاقة!",
            "me": "⚙️ الهندسة الميكانيكية، قلب الصناعة!",
            "che": "🧪 الكيميائية: تفاعل إبداعي لا يتوقف!",
            "ie": "🏭 نظم صناعية وتنظيم عالي!",
            "mining": "⛏️ تنقيبك عن المستقبل يبدأ من هنا.",
            "nuclear": "☢️ جاهز تشعّ علم؟",
            "aero": "✈️ انطلق بأول رحلة دراسية!"
        }
        bot.send_message(user_id, messages[call.data])
        bot.send_message(user_id, f"اخترت: {call.data.upper()}.
(المحتوى قيد الإضافة)")

    elif call.data == "common_courses":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("ARAB201", callback_data="arab201"),
            InlineKeyboardButton("ISLS201", callback_data="isls201"),
            InlineKeyboardButton("ISLS301", callback_data="isls301"),
            InlineKeyboardButton("ISLS401", callback_data="isls401"),
            InlineKeyboardButton("IE202", callback_data="ie202"),
            InlineKeyboardButton("Math 204", callback_data="math204"),
            InlineKeyboardButton("مواد حرة", callback_data="free_course"),
            InlineKeyboardButton("الرجوع", callback_data="academic")
        )
        try:
            bot.edit_message_text("المواد المشتركة:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data in ["arab201", "isls201", "isls301", "isls401", "ie202", "math204", "free_course"]:
        bot.send_message(user_id, f"اخترت: {call.data.upper()} (روابط المحتوى قيد الإضافة)")

    elif call.data == "committees":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("الرياضية", callback_data="sport_committee"),
            InlineKeyboardButton("الثقافية", callback_data="culture_committee"),
            InlineKeyboardButton("الإسلامية", callback_data="islamic_committee"),
            InlineKeyboardButton("الاجتماعية", callback_data="social_committee"),
            InlineKeyboardButton("الرجوع", callback_data="non_academic")
        )
        try:
            bot.edit_message_text("اللجان:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data in ["sport_committee", "culture_committee", "islamic_committee", "social_committee"]:
        names = {
            "sport_committee": "الرياضية",
            "culture_committee": "الثقافية",
            "islamic_committee": "الإسلامية",
            "social_committee": "الاجتماعية"
        }
        bot.send_message(user_id, f"اللجنة: {names[call.data]} (المحتوى قيد الإضافة)")

    elif call.data == "extra_clubs":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("DRAG", callback_data="drag"),
            InlineKeyboardButton("Microsoft", callback_data="microsoft"),
            InlineKeyboardButton("Google", callback_data="google"),
            InlineKeyboardButton("نادي ريادة الأعمال", callback_data="entrepreneur"),
            InlineKeyboardButton("الرجوع", callback_data="non_academic")
        )
        try:
            bot.edit_message_text("بعض الأندية التابعة للعمادة:", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data == "entrepreneur":
        try:
            file = InputFile("attached_assets/entrepreneur.pdf")
            bot.send_document(user_id, file, caption="معلومات نادي ريادة الأعمال")
        except:
            bot.send_message(user_id, "الملف غير موجود حالياً.")

    elif call.data in ["drag", "microsoft", "google"]:
        bot.send_message(user_id, f"النادي: {call.data.upper()} (المحتوى قيد الإضافة)")

    elif call.data == "rate_experience":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("ممتاز", callback_data="rate_excellent"),
            InlineKeyboardButton("جيد", callback_data="rate_good"),
            InlineKeyboardButton("أحتاج تحسين", callback_data="rate_needs_improve"),
            InlineKeyboardButton("عندي ملاحظات", callback_data="rate_feedback"),
            InlineKeyboardButton("الرجوع", callback_data="main_menu")
        )
        try:
            bot.edit_message_text("كيف كانت تجربتك مع البوت؟", user_id, call.message.message_id, reply_markup=markup)
        except:
            pass

    elif call.data in ["rate_excellent", "rate_good", "rate_needs_improve"]:
        ratings = {
            "rate_excellent": "سعيدين إنها كانت ممتازة! شكراً لك!",
            "rate_good": "رائع! نطمح نوصل للممتاز!",
            "rate_needs_improve": "شكراً! راح نشتغل على تحسينه بإذن الله."
        }
        bot.send_message(user_id, ratings[call.data])

    elif call.data == "rate_feedback":
        bot.send_message(user_id, "ارسل ملاحظاتك هنا، راح نوصلها للمطورين مباشرة!")
        user_sessions[user_id] = "awaiting_feedback"

def show_main_menu(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("أكاديمي", callback_data="academic"),
        InlineKeyboardButton("غير أكاديمي", callback_data="non_academic"),
        InlineKeyboardButton("قيّم تجربتك", callback_data="rate_experience"),
        InlineKeyboardButton("الرجوع للبداية", callback_data="main_menu")
    )
    bot.edit_message_text(
        text="اختَر القسم:",
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

app = Flask('')

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run_bot():
    print("تشغيل البوت...")
    bot.polling()

def run_flask():
    print("تشغيل Flask...")
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()

def show_main_menu_direct(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("أكاديمي", callback_data="academic"),
        InlineKeyboardButton("غير أكاديمي", callback_data="non_academic"),
        InlineKeyboardButton("قيّم تجربتك", callback_data="rate_experience"),
        InlineKeyboardButton("الرجوع للبداية", callback_data="main_menu")
    )
    bot.send_message(user_id, "اختَر القسم:", reply_markup=markup)

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id) != "awaiting_question" and user_sessions.get(message.chat.id) != "awaiting_feedback")
def return_to_start(message):
    print(f"رجوع تلقائي للبداية من المستخدم: {message.chat.id}")
    send_start(message)