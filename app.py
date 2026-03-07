from flask import Flask, request
import requests
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAmM9UaCLbYBQ8ZBLtBL1Rh5NKjZCG4QEQlcQIlU2bYUKZCgL0i1T591qkvMuJdU67Ka8Ac0MlUKSsQmOSgOCCbnwZC1q7NrXZCAFREWOPpwGfke7w0GDCebda4OzsuJLStGH9robCV2CcJZBtb76orMKGFZATtPz1B6KRLp7U60C4kvHZAP0ZCZBqocn0exIGBXZCtOaE1sKiVlQZDZD"
VERIFY_TOKEN = "mytoken123"

def send_message(psid, message):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": psid}, "message": {"text": message}}
    requests.post(url, params=params, headers=headers, json=data)

@app.route("/")
def home():
    return "Facebook☑️🧡"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "FacebookBotFidel"

    if request.method == "POST":
        data = request.json
        if "entry" in data:
            for entry in data["entry"]:
                for messaging in entry["messaging"]:
                    if "message" in messaging:
                        sender_id = messaging["sender"]["id"]
                        text = messaging["message"].get("text","")
                        if "سلام" in text:
                            send_message(sender_id, "سلام خويا 👋 مرحبا بك")
                        else:
                            send_message(sender_id, "أنا بوت 🤖 قل سلام فقط")
        return "ok"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
