import os
import discord
from discord import app_commands
import requests
import datetime

class RobloxBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = RobloxBot()

def get_csrf_token(raw_cookie, headers):
    """Extract CSRF token from Roblox cookie"""
    url = "https://auth.roblox.com/v2/logout"
    
    clean_cookie = raw_cookie.replace(".ROBLOSECURITY=", "").strip()
    
    if not clean_cookie:
        raise Exception("Cookie is empty! Paste the full .ROBLOSECURITY cookie.")
    
    cookies = {".ROBLOSECURITY": clean_cookie}
    response = requests.post(url, cookies=cookies, headers=headers, timeout=10)
    csrf_token = response.headers.get("x-csrf-token")
    
    if not csrf_token:
        raise Exception("Failed to fetch CSRF token. Check if your cookie is valid and active.")
        
    return csrf_token, cookies

def validate_birthday(month, day, year):
    """Validate birthday parameters"""
    if not 1 <= month <= 12:
        raise Exception("Invalid month! Must be 1-12.")
    
    if not 1 <= day <= 31:
        raise Exception("Invalid day! Must be 1-31.")
    
    if not 1900 <= year <= 2026:
        raise Exception("Invalid year! Must be 1900-2026.")
    
    try:
        datetime.date(year, month, day)
    except ValueError:
        raise Exception(f"Invalid date! {month}/{day}/{year} is not a real date.")
    
    return True

def method_1_direct_api(cookie, password, month, day, year):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://accountinformation.roblox.com/v1/birthdate"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {
        "birthMonth": month,
        "birthDay": day,
        "birthYear": year,
        "password": password
    }
    
    response = requests.post(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 1 (Direct API)"
    }

def method_2_settings_api(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://settings.roblox.com/v1/user-settings"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"birthMonth": month, "birthDay": day, "birthYear": year}
    response = requests.patch(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 2 (Settings API)"
    }

def method_3_account_preferences(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://accountpreferences.roblox.com/v1/preferences"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"preferences": {"birthdate": {"month": month, "day": day, "year": year}}, "password": password}
    response = requests.put(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 3 (Account Preferences)"
    }

def method_4_profile_update(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://profile.roblox.com/v1/update-profile"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"birthdate": f"{year}-{month:02d}-{day:02d}", "password": password}
    response = requests.post(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 4 (Profile Update)"
    }

def method_5_user_settings(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://users.roblox.com/v1/user-settings"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"birthDate": {"month": month, "day": day, "year": year}, "password": password}
    response = requests.put(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 5 (User Settings)"
    }

def method_6_mobile_ios(cookie, password, month, day, year):
    headers = {"User-Agent": "Roblox/1.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)", "X-Roblox-Device-Type": "iOS"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://mobile.roblox.com/v1/birthdate"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"birthMonth": month, "birthDay": day, "birthYear": year, "password": password}
    response = requests.post(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 6 (Mobile iOS)"
    }

def method_7_mobile_android(cookie, password, month, day, year):
    headers = {"User-Agent": "Roblox/1.0 (Linux; Android 11)", "X-Roblox-Device-Type": "Android"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://mobile.roblox.com/v1/birthdate"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {"birthMonth": month, "birthDay": day, "birthYear": year, "password": password}
    response = requests.post(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 7 (Mobile Android)"
    }

def method_8_form_data(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://accountinformation.roblox.com/v1/birthdate"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    
    data = {"birthMonth": str(month), "birthDay": str(day), "birthYear": str(year), "password": password}
    response = requests.post(url, cookies=cookies, headers=req_headers, data=data, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 8 (Form Data)"
    }

def method_9_multipart_form(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://accountinformation.roblox.com/v1/birthdate"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    
    files = {
        "birthMonth": (None, str(month)),
        "birthDay": (None, str(day)),
        "birthYear": (None, str(year)),
        "password": (None, password)
    }
    response = requests.post(url, cookies=cookies, headers=req_headers, files=files, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 9 (Multipart Form)"
    }

def method_10_graphql(cookie, password, month, day, year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    csrf_token, cookies = get_csrf_token(cookie, headers)
    url = "https://graphql.roblox.com/v1/graphql"
    
    req_headers = headers.copy()
    req_headers["X-CSRF-Token"] = csrf_token
    req_headers["Content-Type"] = "application/json"
    
    payload = {
        "query": "mutation UpdateBirthday($input: UpdateBirthdayInput!) { updateBirthday(input: $input) { success } }",
        "variables": {"input": {"birthMonth": month, "birthDay": day, "birthYear": year, "password": password}}
    }
    response = requests.post(url, cookies=cookies, headers=req_headers, json=payload, timeout=10)
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "method": "Method 10 (GraphQL)"
    }

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | Bot is online!")

@bot.tree.command(name="changebirthday", description="Change Roblox birthday using specific method (1-10)")
@app_commands.describe(
    cookie="Paste your .ROBLOSECURITY cookie",
    password="Your Roblox account password",
    month="Month (1-12)",
    day="Day (1-31)",
    year="Year (1900-2026)",
    method="Method number (1-10)"
)
async def changebirthday(
    interaction: discord.Interaction, 
    cookie: str, 
    password: str,
    month: int,
    day: int,
    year: int,
    method: int = 1
):
    await interaction.response.defer(ephemeral=True)

    try:
        validate_birthday(month, day, year)
        
        methods = {
            1: method_1_direct_api,
            2: method_2_settings_api,
            3: method_3_account_preferences,
            4: method_4_profile_update,
            5: method_5_user_settings,
            6: method_6_mobile_ios,
            7: method_7_mobile_android,
            8: method_8_form_data,
            9: method_9_multipart_form,
            10: method_10_graphql
        }
        
        if method not in methods:
            await interaction.followup.send("❌ Invalid method! Choose 1-10.")
            return
        
        result = methods[method](cookie, password, month, day, year)
        
        if result["success"]:
            msg = f"✅ **Success!**
Method: {result['method']}
Birthday changed to **{month}/{day}/{year}**."
            await interaction.followup.send(msg)
        else:
            error_msg = result["response"] if isinstance(result["response"], str) else str(result["response"])
            msg = f"❌ **Failed!**
Method: {result['method']}
Status: `{result['status_code']}`
Message: `{error_msg}`"
            await interaction.followup.send(msg)

    except Exception as e:
        await interaction.followup.send(f"⚠️ **Error:**
{str(e)}")

@bot.tree.command(name="tryall", description="Try all 10 methods automatically")
@app_commands.describe(
    cookie="Paste your .ROBLOSECURITY cookie",
    password="Your Roblox account password",
    month="Month (1-12)",
    day="Day (1-31)",
    year="Year (1900-2026)"
)
async def tryall(
    interaction: discord.Interaction, 
    cookie: str, 
    password: str,
    month: int,
    day: int,
    year: int
):
    await interaction.response.defer(ephemeral=True)

    try:
        validate_birthday(month, day, year)
        
        embed = discord.Embed(
            title="🔄 Trying All 10 Methods...",
            description=f"Attempting to change birthday to **{month}/{day}/{year}**",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        methods = [
            ("Method 1", method_1_direct_api),
            ("Method 2", method_2_settings_api),
            ("Method 3", method_3_account_preferences),
            ("Method 4", method_4_profile_update),
            ("Method 5", method_5_user_settings),
            ("Method 6", method_6_mobile_ios),
            ("Method 7", method_7_mobile_android),
            ("Method 8", method_8_form_data),
            ("Method 9", method_9_multipart_form),
            ("Method 10", method_10_graphql)
        ]
        
        successful = []
        failed = []
        
        for method_name, method_func in methods:
            result = method_func(cookie, password, month, day, year)
            
            if result["success"]:
                successful.append(result)
            else:
                failed.append(result)
        
        if successful:
            success_msg = "✅ **SUCCESS!**

"
            for i, result in enumerate(successful, 1):
                success_msg += f"**{i}. {result['method']}** ✓
"
            success_msg += f"
Birthday changed to **{month}/{day}/{year}**"
            await interaction.followup.send(success_msg)
        else:
            fail_msg = "❌ **All 10 Methods Failed!**

"
            for result in failed:
                fail_msg += f"❌ {result['method']}: `{result['status_code']}`
"
            fail_msg += "
Try getting a new cookie or check your password."
            await interaction.followup.send(fail_msg)

    except Exception as e:
        await interaction.followup.send(f"⚠️ **Error:**
{str(e)}")

if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if TOKEN:
        print("Bot is starting...")
        bot.run(TOKEN)
    else:
        print("Error: No DISCORD_BOT_TOKEN environment variable found!")
        print("Tip: Set environment variable:")
        print("  Windows: set DISCORD_BOT_TOKEN=your_token_here")
        print("  Mac/Linux: export DISCORD_BOT_TOKEN=your_token_here")
