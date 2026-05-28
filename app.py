import os
import discord
from discord import app_commands
import requests

class RobloxBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # I-sync ang slash commands sa Discord server mo
        await self.tree.sync()

bot = RobloxBot()

def get_csrf_token(raw_cookie, headers):
    url = "https://auth.roblox.com/v2/logout"
    
    # Linisin ang cookie para sigurado (tatanggapin kahit may ".ROBLOSECURITY=" o wala)
    clean_cookie = raw_cookie.replace(".ROBLOSECURITY=", "").strip()
    cookies = {".ROBLOSECURITY": clean_cookie}
    
    response = requests.post(url, cookies=cookies, headers=headers)
    csrf_token = response.headers.get("x-csrf-token")
    
    if not csrf_token:
        raise Exception("Failed to fetch CSRF token. Suriin kung tama/buhay ang cookie mo.")
        
    return csrf_token, cookies

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | Bot is online!")

# Slash command na may dalawang parameters (cookie at password)
@bot.tree.command(name="change", description="Baguhin ang Roblox birthday sa June 5, 2010")
@app_commands.describe(
    cookie="I-paste dito ang iyong .ROBLOSECURITY cookie",
    password="Ang password ng iyong Roblox account"
)
async def change(interaction: discord.Interaction, cookie: str, password: str):
    # 'ephemeral=True' para ikaw lang ang makakita ng response sa chat, iwas silip sa iba
    await interaction.response.defer(ephemeral=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Kunin ang CSRF token gamit ang cookie na binigay mo sa command
        csrf_token, cookies = get_csrf_token(cookie, headers)
        
        url = "https://accountinformation.roblox.com/v1/birthdate"
        
        req_headers = headers.copy()
        req_headers["X-CSRF-Token"] = csrf_token
        req_headers["Content-Type"] = "application/json"
        
        # Hardcoded details base sa hiling mo (June 5, 2010)
        payload = {
            "birthMonth": 6,   # June
            "birthDay": 5,     # 5
            "birthYear": 2010, # 2010
            "password": password
        }
        
        response = requests.post(url, cookies=cookies, headers=req_headers, json=payload)
        
        if response.status_code == 200:
            await interaction.followup.send("✅ **Success!** Nabago na ang iyong Roblox birthday sa June 5, 2010.")
        else:
            try:
                err_msg = response.json().get("errors", [{}])[0].get("message", "Unknown error")
            except:
                err_msg = response.text
            await interaction.followup.send(f"❌ **Failed!** Status Code: {response.status_code}\nResponse: `{err_msg}`")

    except Exception as e:
        await interaction.followup.send(f"⚠️ **Error:** {str(e)}")

if __name__ == "__main__":
    # Ang DISCORD_BOT_TOKEN lang ang itatago sa Environment Variables para mag-run ang bot
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: Walang DISCORD_BOT_TOKEN environment variable na nahanap!")
