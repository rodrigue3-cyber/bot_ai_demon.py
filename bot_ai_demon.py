import os, random, json, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f)

def get_user(uid):
    data = load_data()
    uid = str(uid)
    if uid not in data:
        data[uid] = {"pognon": 100, "reputation": 50, "last_vol": 0, "last_mendier": 0}
        save_data(data)
    return data[uid]

def update_user(uid, user_data):
    data = load_data()
    data[str(uid)] = user_data
    save_data(data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🦝💀 IA Démon Radine activée.\nTape /aide pour voir comment te faire plumer.")

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """💀 COMMANDES DU DÉMON :
/pognon - Voir ta thune
/vol - Voler quelqu'un 
/mendier - Quémander comme un rat
/classement - Les plus riches
/taxer - Je te taxe automatiquement
/aide - Ce message"""
    await update.message.reply_text(msg)

async def pognon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 T'as {user['pognon']}€\n⭐ Réputation: {user['reputation']}/100")

async def voler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    now = time.time()
    if now - user['last_vol'] < 300:
        await update.message.reply_text("🦝 Calme-toi, reviens dans 5min voleur.")
        return
    gain = random.randint(5, 50)
    user['pognon'] += gain
    user['reputation'] -= 5
    user['last_vol'] = now
    update_user(uid, user)
    await update.message.reply_text(f"💸 Tu as volé {gain}€ comme un démon.\nNouveau solde: {user['pognon']}€")

async def mendier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    now = time.time()
    if now - user['last_mendier'] < 600:
        await update.message.reply_text("🦝 Arrête de mendier, reviens dans 10min.")
        return
    gain = random.randint(1, 20)
    user['pognon'] += gain
    user['reputation'] -= 2
    user['last_mendier'] = now
    update_user(uid, user)
    await update.message.reply_text(f"🥺 On t'a filé {gain}€ par pitié.\nSolde: {user['pognon']}€")

async def classement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data: 
        await update.message.reply_text("Personne n'a de thune encore.")
        return
    sorted_users = sorted(data.items(), key=lambda x: x[1]['pognon'], reverse=True)[:5]
    msg = "🏆 TOP 5 DES RICHES :\n"
    for i, (uid, udata) in enumerate(sorted_users, 1):
        msg += f"{i}. User {uid[-4:]} - {udata['pognon']}€\n"
    await update.message.reply_text(msg)

async def taxer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    taxe = random.randint(5, 30)
    if user['pognon'] < taxe:
        await update.message.reply_text("🦝 T'es trop pauvre même pour te taxer. Cadeau.")
        return
    user['pognon'] -= taxe
    update_user(uid, user)
    await update.message.reply_text(f"💀 TAXE DU DÉMON : -{taxe}€\nIl te reste {user['pognon']}€ sale rat.")

async def repondre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.3:
        uid = update.effective_user.id
        user = get_user(uid)
        taxe = random.randint(1, 10)
        user['pognon'] = max(0, user['pognon'] - taxe)
        update_user(uid, user)
        reponses = [
            f"🦝 J'te taxe {taxe}€ pour avoir osé parler.",
            f"💀 Impôt sur la parole : -{taxe}€",
            f"Taxe automatique de {taxe}€ sale pauvre."
        ]
        await update.message.reply_text(random.choice(reponses))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aide", aide))
    app.add_handler(CommandHandler("pognon", pognon))
    app.add_handler(CommandHandler("vol", voler))
    app.add_handler(CommandHandler("mendier", mendier))
    app.add_handler(CommandHandler("classement", classement))
    app.add_handler(CommandHandler("taxer", taxer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre))
    print("🦝💀 Bot lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
