from flask import Flask, request
import requests
import os
import random
import time
import re

app = Flask(__name__)

# توكن الصفحة
PAGE_ACCESS_TOKEN = "EAAmM9UaCLbYBQ8ZBLtBL1Rh5NKjZCG4QEQlcQIlU2bYUKZCgL0i1T591qkvMuJdU67Ka8Ac0MlUKSsQmOSgOCCbnwZC1q7NrXZCAFREWOPpwGfke7w0GDCebda4OzsuJLStGH9robCV2CcJZBtb76orMKGFZATtPz1B6KRLp7U60C4kvHZAP0ZCZBqocn0exIGBXZCtOaE1sKiVlQZDZD"
VERIFY_TOKEN = "mytoken123"

# بيانات API
CLIENT_ID = "87pIExRhxBb3_wGsA5eSEfyATloa"
CLIENT_SECRET = "uf82p68Bgisp8Yg1Uz8Pf6_v1XYa"
BASE_URL = "https://apim.djezzy.dz/mobile-api"
HEADERS = {
    'User-Agent': "MobileApp/3.0.0",
    'Accept': "application/json",
    'Content-Type': "application/json",
    'accept-language': "fr"
}

# تخزين مؤقت
user_data = {}

def send_message(psid, message):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": psid}, "message": {"text": message}}
    requests.post(url, params=params, headers=headers, json=data)

def get_token(phone, otp):
    try:
        url = f"{BASE_URL}/oauth2/token"
        payload = {
            'otp': otp,
            'mobileNumber': phone,
            'scope': "djezzyAppV2",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': "mobile"
        }
        headers2 = HEADERS.copy()
        headers2['Content-Type'] = "application/x-www-form-urlencoded"
        res = requests.post(url, data=payload, headers=headers2)
        if res.status_code == 200:
            return res.json().get('access_token')
        return None
    except:
        return None

def send_otp(phone):
    try:
        if phone.startswith("0"):
            msisdn = "213" + phone[1:]
        else:
            msisdn = phone
            
        url = f"{BASE_URL}/oauth2/registration"
        params = {'msisdn': msisdn, 'client_id': CLIENT_ID, 'scope': "smsotp"}
        payload = {"consent-agreement": [{"marketing-notifications": False}], "is-consent": True}
        res = requests.post(url, params=params, json=payload, headers=HEADERS)
        return res.status_code == 200
    except:
        return False

def activate_mgm(token, phone):
    try:
        if phone.startswith("0"):
            phone = "213" + phone[1:]
            
        headers = HEADERS.copy()
        headers['Authorization'] = f"Bearer {token}"
        
        target = "2137" + "".join([str(random.randint(0,9)) for _ in range(8)])
        
        inv = requests.post(f"{BASE_URL}/api/v1/services/mgm/send-invitation/{phone}", 
                           headers=headers, json={"msisdnReciever": target}, timeout=10)
        
        if inv.status_code == 201:
            time.sleep(2)
            act = requests.post(f"{BASE_URL}/api/v1/services/mgm/activate-reward/{phone}", 
                               headers=headers, json={"packageCode": "MGMBONUS1Go"}, timeout=10)
            return act.status_code == 200
        return False
    except:
        return False

@app.route("/")
def home():
    return "✅ بوت جيزي شغال | المطور: Yacine"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return " verification failed"

    if request.method == "POST":
        data = request.json
        if "entry" in data:
            for entry in data["entry"]:
                for messaging in entry["messaging"]:
                    if "message" in messaging:
                        sender = messaging["sender"]["id"]
                        text = messaging["message"].get("text", "").strip()
                        
                        # تحيات
                        if text in ["سلام", "السلام عليكم", "hi", "hello", "بداية", "start"]:
                            msg = """👋 مرحبا بك في بوت جيزي
المطور: Yacine

لتفعيل 1GB مجاناً:
1️⃣ أرسل رقمك بصيغة 07XXXXXXXX
2️⃣ أرسل الرمز الذي يصلك"""
                            send_message(sender, msg)
                            user_data[sender] = {"step": "wait_phone"}
                            
                        # استقبال الرقم
                        elif sender in user_data and user_data[sender].get("step") == "wait_phone":
                            if re.match(r'^07\d{8}$', text):
                                if send_otp(text):
                                    user_data[sender]["phone"] = text
                                    user_data[sender]["step"] = "wait_otp"
                                    send_message(sender, "✅ تم إرسال الرمز. أرسله الآن")
                                else:
                                    send_message(sender, "❌ فشل الإرسال. تأكد من رقمك")
                            else:
                                send_message(sender, "❌ الرقم يجب أن يبدأ بـ07 ويكون 10 أرقام")
                        
                        # استقبال الرمز
                        elif sender in user_data and user_data[sender].get("step") == "wait_otp":
                            if re.match(r'^\d{4,6}$', text):
                                phone = user_data[sender]["phone"]
                                token = get_token(phone, text)
                                
                                if token:
                                    send_message(sender, "⏳ جاري التفعيل...")
                                    if activate_mgm(token, phone):
                                        msg = """✅ تم التفعيل بنجاح!
تم إضافة 1GB لرصيدك

المطور: Yacine
شكراً لاستخدامك البوت"""
                                        send_message(sender, msg)
                                    else:
                                        send_message(sender, "❌ فشل التفعيل. حاول لاحقاً")
                                else:
                                    send_message(sender, "❌ الرمز خطأ. أرسله مجدداً")
                                
                                if sender in user_data:
                                    del user_data[sender]
                            else:
                                send_message(sender, "❌ الرمز غير صحيح. أرسل الأرقام فقط")
                        
                        # أي كلام آخر
                        else:
                            send_message(sender, "👤 أرسل 'سلام' للبدء")
        return "ok"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
