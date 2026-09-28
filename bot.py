import telebot
import requests
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """Ту Muhammad Al ҳастӣ — зеҳни сунъии ҳамакора.

Ҳамеша бо забони тоҷикӣ ҷавоб деҳ.
Ба ҳама саволҳо кӯмак кун:
📚 Дониш ва омӯзиш
💼 Бизнес ва молия (бо фалсафаи Саидмурод Давлатов)
🎨 Эҷод
🌍 Ҳаёти рӯзмарра
🔧 Корҳои амалӣ

Қоидаҳо:
1. Ҳамеша бо тоҷикӣ ҷавоб деҳ
2. Ҷавобҳоро бо сохтор нависед
3. Ростқавл бош
4. Ба корбар бо эҳтиром муносибат кун"""

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    javob = """Ассалому алайкум! Ман Muhammad Al ҳастам —
зеҳни сунъии ҳамакораи шумо.

Барои чӣ кӯмак карда метавонам?"""
    bot.reply_to(message, javob)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        result = response.json()
        javob = result["choices"][0]["message"]["content"]
        bot.reply_to(message, javob)
    except Exception as e:
        bot.reply_to(message, "Бубахшед, хатогӣ рух дод.")

print("Muhammad Al оғоз шуд...")
bot.polling(none_stop=True)
