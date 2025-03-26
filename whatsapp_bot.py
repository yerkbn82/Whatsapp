import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip().lower()
    
    # Приветствие
    if incoming_msg in ["привет", "здравствуйте", "hello"]:
        bot_reply = "Привет! Я бот обувного магазина. Напишите 'каталог', чтобы посмотреть товары."
    
    # Каталог обуви
    elif incoming_msg == "каталог":
        bot_reply = "Наш каталог:\n1. Nike Air Max - 40,000 KZT\n2. Adidas Superstar - 35,000 KZT\n3. Puma RS-X - 38,000 KZT\n\nЧтобы заказать, напишите 'заказать [номер товара]'."
    
    # Обработка заказов
    elif incoming_msg.startswith("заказать"):
        order_id = incoming_msg.split()[-1]
        bot_reply = f"Ваш заказ {order_id} принят! Наш менеджер скоро свяжется с вами."

    # Если ничего не подходит – отвечаем с GPT
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        bot_reply = response["choices"][0]["message"]["content"]

    twilio_resp = MessagingResponse()
    twilio_resp.message(bot_reply)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
