from telegram.ext import Application, CommandHandler
import asyncio
from datetime import datetime
import requests
import os # <--- NEW: Import the OS library to access environment variables

# --- CONFIGURATION (Fetching from Render's Environment Variables) ---
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
ALERT_CHAT_ID = os.environ.get('ALERT_CHAT_ID') 

# --- NĀRAD'S WORK (Now with Live API Calls) ---

def get_latest_verified_news():
    """Placeholder for News Scanner & Truth Verification (/naradnews)."""
    return (
        f"🗞️ *Latest Verified News Scan* (Time: {datetime.now().strftime('%H:%M:%S IST')})\n"
        f"Status: Scanners Active. No major Dharmic news detected."
    )

def get_instant_solana_update():
    """Fetches live SOL Price and Solana Network TPS/Health (/solalert)."""
    # 1. Fetch Live SOL Price from CoinGecko
    try:
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true"
        price_response = requests.get(price_url).json()
        sol_data = price_response.get('solana', {})
        price = sol_data.get('usd')
        change_24h = sol_data.get('usd_24h_change')

        if price and change_24h is not None:
            price_line = f"💰 *Price:* ${price:.2f} (24h: {change_24h:.2f}%)"
        else:
            price_line = "💰 *Price:* Data Unavailable"
    except Exception:
        price_line = "💰 *Price:* API Connection Error"

    # 2. Fetch Live TPS from Solana Network RPC
    try:
        rpc_url = "https://api.mainnet-beta.solana.com"
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getRecentPerformanceSamples", "params": [1]}
        tps_response = requests.post(rpc_url, json=payload).json()

        if tps_response.get('result') and tps_response['result'][0]['numTransactions'] > 0:
            tps_data = tps_response['result'][0]
            tps = tps_data['numTransactions'] / tps_data['samplePeriodSecs']
            tps_line = f"⚡ *TPS:* {tps:.0f} (Avg.)"
        else:
            tps_line = "⚡ *TPS:* Data Unavailable (RPC Error)"
    except Exception:
        tps_line = "⚡ *TPS:* API Connection Error"

    return (
        f"🔱 *NĀRAD SOLANA REPORT* 🔱\n"
        f"{price_line}\n"
        f"{tps_line}\n"
        f"*Congestion:* NONE (Basic Status OK)"
    )

# --- COMMAND HANDLERS ---
async def naradnews_command(update, context):
    """/naradnews → latest verified news"""
    response = get_latest_verified_news()
    await update.message.reply_text(response, parse_mode='Markdown')

async def solalert_command(update, context):
    """/solalert → instant Solana update (Uses Live Data)"""
    response = get_instant_solana_update()
    await update.message.reply_text(response, parse_mode='Markdown')

async def whalemove_command(update, context):
    """/whalemove → large wallet movement"""
    await update.message.reply_text("🐋 *Whale Movement Scan*:\nStatus: Placeholder - No significant movements (>$5M) detected.", parse_mode='Markdown')

async def risk_command(update, context):
    """/risk → tells if market is safe or dangerous"""
    await update.message.reply_text("🚨 *Market Risk Assessment:\nRISK LEVEL: **MODERATE*. Sentiment is positive, but caution is advised.", parse_mode='Markdown')

# --- MAIN BOT SETUP ---
def main():
    print("NARAD Bot: Initializing (Polling Mode)...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("naradnews", naradnews_command))
    application.add_handler(CommandHandler("solalert", solalert_command))
    application.add_handler(CommandHandler("whalemove", whalemove_command))
    application.add_handler(CommandHandler("risk", risk_command))

    print("NARAD Bot: Starting Polling Loop...")
    application.run_polling()

if __name__ == "__main__":
    main()
        
