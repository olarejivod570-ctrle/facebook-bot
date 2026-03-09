from flask import Flask, request
import requests
import os
import json
import re

app = Flask(__name__)

# ================ إعدادات فيسبوك ================
PAGE_ACCESS_TOKEN = "EAAmM9UaCLbYBQ8ZBLtBL1Rh5NKjZCG4QEQlcQIlU2bYUKZCgL0i1T591qkvMuJdU67Ka8Ac0MlUKSsQmOSgOCCbnwZC1q7NrXZCAFREWOPpwGfke7w0GDCebda4OzsuJLStGH9robCV2CcJZBtb76orMKGFZATtPz1B6KRLp7U60C4kvHZAP0ZCZBqocn0exIGBXZCtOaE1sKiVlQZDZD"
VERIFY_TOKEN = "mytoken123"

# ================ قاعدة بيانات الهواتف ================
PHONE_DB = {
    "itel": {
        "a70": {
            "name": "📱 Itel A70",
            "brand": "itel",
            "dpi": "280",
            "sensitivity": {
                "general": "185",
                "red_dot": "175",
                "2x_scope": "165",
                "4x_scope": "145",
                "sniper": "125",
                "free_look": "155",
                "3x_scope": "135",
                "aim_precision": "195"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "ولفراه", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🟢 سلسة + إطار عالي",
            "note": "💪 ممتاز للأداء المتوسط"
        }
    },
    "samsung": {
        "s21": {
            "name": "📱 Samsung Galaxy S21",
            "brand": "samsung",
            "dpi": "420",
            "sensitivity": {
                "general": "92",
                "red_dot": "82",
                "2x_scope": "72",
                "4x_scope": "55",
                "sniper": "38",
                "free_look": "85",
                "3x_scope": "65",
                "aim_precision": "90"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "كلا", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🔵 ناعم + إطار عالي جداً",
            "note": "👑 مناسب للمحترفين"
        }
    },
    "xiaomi": {
        "poco_x3": {
            "name": "📱 Poco X3 Pro",
            "brand": "xiaomi",
            "dpi": "440",
            "sensitivity": {
                "general": "95",
                "red_dot": "85",
                "2x_scope": "75",
                "4x_scope": "58",
                "sniper": "42",
                "free_look": "88",
                "3x_scope": "68",
                "aim_precision": "93"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "سكايلر", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كابيلا", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🔵 ناعم + إطار عالي جداً",
            "note": "⚡ معالج قوي 860"
        }
    },
    "iphone": {
        "iphone_11": {
            "name": "📱 iPhone 11",
            "brand": "iphone",
            "dpi": "460",
            "sensitivity": {
                "general": "88",
                "red_dot": "78",
                "2x_scope": "68",
                "4x_scope": "52",
                "sniper": "36",
                "free_look": "82",
                "3x_scope": "62",
                "aim_precision": "86"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "ووكونغ", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "اوليفيا"],
                "sniper": ["داشا", "لورا", "زاين", "انتونيو"]
            },
            "graphics": "🎮 HD + إطار عالي",
            "note": "🍎 ثبات رهيب"
        }
    },
    "infinix": {
        "hot_40": {
            "name": "📱 Infinix Hot 40",
            "brand": "infinix",
            "dpi": "320",
            "sensitivity": {
                "general": "175",
                "red_dot": "165",
                "2x_scope": "155",
                "4x_scope": "135",
                "sniper": "115",
                "free_look": "145",
                "3x_scope": "125",
                "aim_precision": "170"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "ولفراه", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🟢 سلسة + إطار عالي",
            "note": "🔥 أداء جيد"
        }
    },
    "tecno": {
        "spark_20": {
            "name": "📱 Tecno Spark 20",
            "brand": "tecno",
            "dpi": "300",
            "sensitivity": {
                "general": "180",
                "red_dot": "170",
                "2x_scope": "160",
                "4x_scope": "140",
                "sniper": "120",
                "free_look": "150",
                "3x_scope": "130",
                "aim_precision": "175"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "ولفراه", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🟢 سلسة + إطار عالي",
            "note": "✨ مناسب للعبة"
        }
    },
    "oppo": {
        "a57": {
            "name": "📱 Oppo A57",
            "brand": "oppo",
            "dpi": "320",
            "sensitivity": {
                "general": "172",
                "red_dot": "162",
                "2x_scope": "152",
                "4x_scope": "132",
                "sniper": "112",
                "free_look": "142",
                "3x_scope": "122",
                "aim_precision": "168"
            },
            "recommended_chars": {
                "aggressive": ["كرونو", "ولفراه", "جوتا", "هاياتو"],
                "support": ["الوك", "ديميتري", "كلو", "شاني"],
                "sniper": ["داشا", "لورا", "دي بي", "انتونيو"]
            },
            "graphics": "🟢 سلسة + إطار عالي",
            "note": "📱 جيد للمبتدئين"
        }
    }
}

# ================ تخزين مؤقت للمستخدمين ================
user_sessions = {}

# ================ دوال الإرسال ================
def send_message(psid, message_text):
    """إرسال رسالة نصية"""
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": psid},
        "message": {"text": message_text}
    }
    try:
        response = requests.post(url, params=params, headers=headers, json=data)
        print(f"📤 إرسال رسالة إلى {psid}: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return None

def send_quick_replies(psid, text, replies):
    """إرسال ردود سريعة (خانات)"""
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    quick_replies_list = []
    for reply_title, reply_payload in replies:
        quick_reply = {
            "content_type": "text",
            "title": reply_title,
            "payload": reply_payload
        }
        quick_replies_list.append(quick_reply)
    
    data = {
        "recipient": {"id": psid},
        "message": {
            "text": text,
            "quick_replies": quick_replies_list
        }
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=data)
        print(f"📤 إرسال خانات إلى {psid}: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ خطأ في إرسال الخانات: {e}")
        return None

def send_buttons(psid, text, buttons):
    """إرسال أزرار تفاعلية"""
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    button_list = []
    for btn_title, btn_payload in buttons:
        button_list.append({
            "type": "postback",
            "title": btn_title,
            "payload": btn_payload
        })
    
    data = {
        "recipient": {"id": psid},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": button_list
                }
            }
        }
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=data)
        print(f"📤 إرسال أزرار إلى {psid}: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ خطأ في إرسال الأزرار: {e}")
        return None

# ================ دوال المساعدة ================
def get_phone_by_brand_model(brand, model):
    """البحث عن هاتف في قاعدة البيانات"""
    if brand in PHONE_DB and model in PHONE_DB[brand]:
        return PHONE_DB[brand][model]
    return None

def search_phone(query):
    """البحث عن هاتف بالاسم"""
    results = []
    query = query.lower()
    
    for brand, models in PHONE_DB.items():
        for model, data in models.items():
            if query in data['name'].lower() or query in model.lower():
                results.append((brand, model, data))
    
    return results

def format_sensitivity(phone_data):
    """تنسيق رسالة الحساسية"""
    sens = phone_data['sensitivity']
    
    msg = f"""🔰 **{phone_data['name']}**

📊 **معلومات الجهاز:**
• DPI: `{phone_data['dpi']}`
• الجرافيكس: {phone_data['graphics']}

⚡ **إعدادات الحساسية:**
━━━━━━━━━━━━━━━━
🎮 عام: `{sens['general']}`
🎯 ريد دوت: `{sens['red_dot']}`
🔭 سكوب 2x: `{sens['2x_scope']}`
🔭 سكوب 3x: `{sens.get('3x_scope', '130')}`
🔭 سكوب 4x: `{sens['4x_scope']}`
🎯 قناص: `{sens['sniper']}`
👀 نظر حر: `{sens.get('free_look', '85')}`
🎯 دقة تصويب: `{sens.get('aim_precision', '90')}`
━━━━━━━━━━━━━━━━

✅ **طريقة التطبيق:**
1️⃣ اذهب للإعدادات ⚙️
2️⃣ اختر الحساسية 🎯
3️⃣ ضبط القيم يدوياً ✏️
4️⃣ حفظ التغييرات 💾
"""
    return msg

def format_chars(phone_data, style):
    """تنسيق رسالة الشخصيات"""
    chars = phone_data['recommended_chars'][style]
    
    style_names = {
        'aggressive': '⚔️ هجومي',
        'support': '🛡️ دعم',
        'sniper': '🎯 قناص'
    }
    
    msg = f"""🔰 **{phone_data['name']}**
🎮 أسلوب اللعب: {style_names[style]}

🌟 **الشخصيات المقترحة:**
━━━━━━━━━━━━━━━━
🎭 **المهارة النشطة:**
• {chars[0]}

🃏 **المهارات السلبية:**
• {chars[1]}
• {chars[2]}
• {chars[3]}
━━━━━━━━━━━━━━━━
"""
    return msg

# ================ قوائم الخانات ================
def show_main_menu(psid):
    """عرض القائمة الرئيسية بالخانات"""
    text = "🏠 **القائمة الرئيسية**\n\nاختر من الخيارات أدناه:"
    replies = [
        ("🔍 بحث", "SEARCH"),
        ("📱 هواتفي", "MY_PHONES"),
        ("🔥 الأكثر طلباً", "POPULAR"),
        ("❓ مساعدة", "HELP")
    ]
    send_quick_replies(psid, text, replies)

def show_phone_options(psid, brand, model, phone_name):
    """عرض خيارات الهاتف بالخانات"""
    text = f"📱 **{phone_name}**\n\nماذا تريد؟"
    replies = [
        ("🎯 الحساسية", f"SENS_{brand}_{model}"),
        ("👥 الشخصيات", f"CHARS_{brand}_{model}"),
        ("⚙️ إعدادات", f"SETTINGS_{brand}_{model}"),
        ("🔙 رجوع", "HOME")
    ]
    send_quick_replies(psid, text, replies)

def show_style_options(psid, brand, model):
    """عرض خيارات أسلوب اللعب بالخانات"""
    text = "👥 **اختر أسلوب لعبك:**"
    replies = [
        ("⚔️ هجومي", f"STYLE_aggressive_{brand}_{model}"),
        ("🛡️ دعم", f"STYLE_support_{brand}_{model}"),
        ("🎯 قناص", f"STYLE_sniper_{brand}_{model}"),
        ("🔙 رجوع", f"PHONE_{brand}_{model}")
    ]
    send_quick_replies(psid, text, replies)

# ================ معالجة الرسائل النصية ================
def handle_message(sender_id, message_text):
    """معالجة الرسائل النصية"""
    
    print(f"📩 رسالة من {sender_id}: {message_text}")
    
    # كلمات البداية
    if message_text in ["start", "ابدأ", "hi", "hello", "سلام", "السلام عليكم", "بداية", "main", "القائمة"]:
        welcome_msg = """👋 **مرحباً بك في بوت حساسيات فري فاير** 🔫

أنا هنا لمساعدتك في الحصول على أفضل إعدادات حساسية لهاتفك!

🔍 **للبحث عن هاتفك:** أرسل اسم الجهاز
مثال: `itel a70` أو `s21`"""
        
        send_message(sender_id, welcome_msg)
        show_main_menu(sender_id)
        return
    
    # كلمات المساعدة
    if message_text in ["مساعدة", "help", "المساعدة", "?"]:
        help_msg = """❓ **مساعدة البوت:**

📱 **للبحث عن هاتف:**
أرسل اسم الهاتف في المحادثة
مثال: "s21" أو "itel a70"

📱 **الهواتف المتوفرة:**
• Itel A70
• Samsung S21
• Poco X3
• iPhone 11
• Infinix Hot 40
• Tecno Spark 20
• Oppo A57"""
        
        replies = [("🏠 رئيسية", "HOME"), ("🔍 بحث", "SEARCH")]
        send_message(sender_id, help_msg)
        send_quick_replies(sender_id, "اختر:", replies)
        return
    
    # كلمات الماركات
    if message_text in ["ماركات", "brands", "الماركات"]:
        show_brands_menu(sender_id)
        return
    
    # كلمات الأكثر طلباً
    if message_text in ["الأكثر طلباً", "popular", "مشهورة", " hottest"]:
        show_popular_phones(sender_id)
        return
    
    # البحث عن هاتف
    results = search_phone(message_text)
    
    if results:
        if len(results) == 1:
            brand, model, phone_data = results[0]
            send_message(sender_id, f"✅ تم العثور على {phone_data['name']}")
            show_phone_options(sender_id, brand, model, phone_data['name'])
            # حفظ آخر هاتف
            user_sessions[sender_id] = {"last_brand": brand, "last_model": model}
        else:
            msg = f"🔍 **نتائج البحث عن '{message_text}':**\n\nاختر هاتفك:"
            replies = []
            for brand, model, phone_data in results[:8]:
                short_name = phone_data['name'].replace("📱 ", "")[:15]
                replies.append((short_name, f"PHONE_{brand}_{model}"))
            replies.append(("🔙 رجوع", "HOME"))
            send_quick_replies(sender_id, msg, replies)
    else:
        not_found_msg = f"""❌ لا توجد نتائج لـ '{message_text}'

💡 **جرب:**
• اسم الموديل فقط (a70)
• أشهر الهواتف من القائمة"""
        
        send_message(sender_id, not_found_msg)
        replies = [("🔥 الأكثر طلباً", "POPULAR"), ("📱 الماركات", "BRANDS"), ("🏠 رئيسية", "HOME")]
        send_quick_replies(sender_id, "اختر:", replies)

def show_brands_menu(psid):
    """عرض قائمة الماركات"""
    msg = "📱 **اختر الماركة:**"
    replies = [
        ("🇰🇷 Samsung", "BRAND_samsung"),
        ("🇨🇳 Xiaomi", "BRAND_xiaomi"),
        ("🇨🇳 Itel", "BRAND_itel"),
        ("🇨🇳 Infinix", "BRAND_infinix"),
        ("🇺🇸 iPhone", "BRAND_iphone"),
        ("🇨🇳 Tecno", "BRAND_tecno"),
        ("🇨🇳 Oppo", "BRAND_oppo"),
        ("🏠 رئيسية", "HOME")
    ]
    send_quick_replies(psid, msg, replies)

def show_popular_phones(psid):
    """عرض الهواتف الأكثر طلباً"""
    msg = "🔥 **الهواتف الأكثر طلباً:**"
    replies = [
        ("Itel A70", "PHONE_itel_a70"),
        ("Samsung S21", "PHONE_samsung_s21"),
        ("Poco X3", "PHONE_xiaomi_poco_x3"),
        ("iPhone 11", "PHONE_iphone_iphone_11"),
        ("Infinix Hot 40", "PHONE_infinix_hot_40"),
        ("🏠 رئيسية", "HOME")
    ]
    send_quick_replies(psid, msg, replies)

# ================ معالجة Postback ================
def handle_postback(sender_id, payload):
    """معالجة الضغط على الأزرار والخانات"""
    
    print(f"🔘 Postback من {sender_id}: {payload}")
    
    # ===== القائمة الرئيسية =====
    if payload == "HOME":
        show_main_menu(sender_id)
    
    elif payload == "SEARCH":
        msg = "🔍 **أرسل اسم الهاتف الذي تبحث عنه**\nمثال: itel a70 أو s21"
        replies = [("🏠 رئيسية", "HOME"), ("🔥 الأكثر طلباً", "POPULAR")]
        send_message(sender_id, msg)
        send_quick_replies(sender_id, "اختر:", replies)
    
    elif payload == "POPULAR":
        show_popular_phones(sender_id)
    
    elif payload == "BRANDS":
        show_brands_menu(sender_id)
    
    elif payload == "HELP":
        help_msg = """❓ **مساعدة سريعة:**

🔍 للبحث: أرسل اسم الهاتف
📱 للماركات: اختر "الماركات"
🔥 للأكثر طلباً: اختر "الأكثر طلباً"

💬 تواصل مع المطور: @Yacine"""
        send_message(sender_id, help_msg)
        replies = [("🏠 رئيسية", "HOME"), ("📱 ماركات", "BRANDS")]
        send_quick_replies(sender_id, "اختر:", replies)
    
    elif payload == "MY_PHONES":
        if sender_id in user_sessions and "last_brand" in user_sessions[sender_id]:
            brand = user_sessions[sender_id]["last_brand"]
            model = user_sessions[sender_id]["last_model"]
            phone_data = get_phone_by_brand_model(brand, model)
            if phone_data:
                show_phone_options(sender_id, brand, model, phone_data['name'])
            else:
                send_message(sender_id, "❌ لا يوجد هاتف سابق")
                replies = [("🔍 بحث جديد", "SEARCH"), ("🏠 رئيسية", "HOME")]
                send_quick_replies(sender_id, "اختر:", replies)
        else:
            send_message(sender_id, "📱 لم تبحث عن أي هاتف بعد")
            replies = [("🔍 بحث الآن", "SEARCH"), ("🏠 رئيسية", "HOME")]
            send_quick_replies(sender_id, "اختر:", replies)
    
    # ===== عرض ماركة معينة =====
    elif payload.startswith("BRAND_"):
        brand = payload.replace("BRAND_", "")
        if brand in PHONE_DB:
            brand_names = {
                "samsung": "🇰🇷 Samsung",
                "xiaomi": "🇨🇳 Xiaomi",
                "itel": "🇨🇳 Itel",
                "infinix": "🇨🇳 Infinix",
                "iphone": "🇺🇸 iPhone",
                "tecno": "🇨🇳 Tecno",
                "oppo": "🇨🇳 Oppo"
            }
            brand_name = brand_names.get(brand, brand.capitalize())
            msg = f"📱 **{brand_name} - الهواتف:**"
            replies = []
            for model, data in PHONE_DB[brand].items():
                short_name = data['name'].replace("📱 ", "")[:12]
                replies.append((short_name, f"PHONE_{brand}_{model}"))
            replies.append(("🔙 رجوع", "BRANDS"))
            send_quick_replies(sender_id, msg, replies[:10])
    
    # ===== عرض هاتف معين =====
    elif payload.startswith("PHONE_"):
        parts = payload.replace("PHONE_", "").split("_", 1)
        if len(parts) == 2:
            brand, model = parts
            phone_data = get_phone_by_brand_model(brand, model)
            if phone_data:
                user_sessions[sender_id] = {"last_brand": brand, "last_model": model}
                show_phone_options(sender_id, brand, model, phone_data['name'])
    
    # ===== عرض الحساسية =====
    elif payload.startswith("SENS_"):
        parts = payload.replace("SENS_", "").split("_", 1)
        if len(parts) == 2:
            brand, model = parts
            phone_data = get_phone_by_brand_model(brand, model)
            if phone_data:
                msg = format_sensitivity(phone_data)
                send_message(sender_id, msg)
                
                # عرض خيارات بعد الحساسية
                text = "✅ **تم عرض الحساسية**\n\nماذا تريد الآن؟"
                replies = [
                    ("👥 شخصيات", f"CHARS_{brand}_{model}"),
                    ("🔄 هاتف آخر", "SEARCH"),
                    ("🏠 رئيسية", "HOME")
                ]
                send_quick_replies(sender_id, text, replies)
    
    # ===== عرض خيارات الشخصيات =====
    elif payload.startswith("CHARS_"):
        parts = payload.replace("CHARS_", "").split("_", 1)
        if len(parts) == 2:
            brand, model = parts
            show_style_options(sender_id, brand, model)
    
    # ===== عرض أسلوب معين =====
    elif payload.startswith("STYLE_"):
        parts = payload.replace("STYLE_", "").split("_", 2)
        if len(parts) == 3:
            style, brand, model = parts
            phone_data = get_phone_by_brand_model(brand, model)
            if phone_data:
                msg = format_chars(phone_data, style)
                send_message(sender_id, msg)
                
                # عرض خيارات بعد الشخصيات
                text = "👥 **تم عرض الشخصيات**\n\nماذا تريد الآن؟"
                replies = [
                    ("🎯 الحساسية", f"SENS_{brand}_{model}"),
                    ("🔄 أسلوب آخر", f"CHARS_{brand}_{model}"),
                    ("🏠 رئيسية", "HOME")
                ]
                send_quick_replies(sender_id, text, replies)
    
    # ===== عرض الإعدادات =====
    elif payload.startswith("SETTINGS_"):
        parts = payload.replace("SETTINGS_", "").split("_", 1)
        if len(parts) == 2:
            brand, model = parts
            phone_data = get_phone_by_brand_model(brand, model)
            if phone_data:
                settings_msg = f"""🔰 **{phone_data['name']}** - إعدادات متقدمة

⚙️ **معلومات الجهاز:**
• DPI: `{phone_data['dpi']}`
• الجرافيكس: {phone_data['graphics']}

🎮 **إعدادات مقترحة:**
• جودة الرسوم: ناعم (Smooth)
• معدل الإطارات: عالي (High)
• الظل: مفعل ✅
• تأثيرات: متوسطة

💡 **نصائح لتحسين الأداء:**
1️⃣ أغلق التطبيقات الخلفية
2️⃣ فعل وضع الألعاب
3️⃣ خفض سطوع الشاشة"""
                
                send_message(sender_id, settings_msg)
                replies = [
                    ("🎯 الحساسية", f"SENS_{brand}_{model}"),
                    ("👥 شخصيات", f"CHARS_{brand}_{model}"),
                    ("🏠 رئيسية", "HOME")
                ]
                send_quick_replies(sender_id, "⚙️ **اختر:**", replies)

# ================ Routes ================
@app.route("/")
def home():
    return "✅ بوت حساسيات فري فاير شغال | المطور: Yacine"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully")
            return challenge
        print("❌ Webhook verification failed")
        return "❌ التحقق فشل"

    if request.method == "POST":
        data = request.json
        print(f"📨 Webhook received: {data}")
        
        if "entry" in data:
            for entry in data["entry"]:
                for messaging in entry.get("messaging", []):
                    sender_id = messaging["sender"]["id"]
                    
                    # معالجة الرسائل النصية
                    if "message" in messaging and "text" in messaging["message"]:
                        text = messaging["message"]["text"].strip().lower()
                        handle_message(sender_id, text)
                    
                    # معالجة postback (الأزرار)
                    elif "postback" in messaging:
                        payload = messaging["postback"]["payload"]
                        handle_postback(sender_id, payload)
                    
                    # معالجة quick reply
                    elif "message" in messaging and "quick_reply" in messaging["message"]:
                        payload = messaging["message"]["quick_reply"]["payload"]
                        handle_postback(sender_id, payload)
        
        return "OK", 200

# ================ تشغيل التطبيق ================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    print(f"🚀 Bot starting on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
