import requests
import random
import string
import time
import os


url = "https://n-production-serial-code.sekai-en.com/api/serial-code"
user_id = "677869293366751238"  # replace with your actual user ID if needed

headers = {
    "Host": "n-production-serial-code.sekai-en.com",
    "sec-ch-ua-platform": "\"Android\"",
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; AI2501 Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.111 Mobile Safari/537.36",
    "Accept": "application/json",
    "sec-ch-ua": "\"Android WebView\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "Origin": "https://n-production-serial-code.sekai-en.com",
    "x-requested-with": "prosekai.browser",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "Referer": "https://n-production-serial-code.sekai-en.com/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

def generate_serial_code(length=17):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Set output file path
output_path = "/storage/emulated/0/Download/alive_codes.txt"


dead_count = 0
alive_count = 0
used_count = 0

# Make sure Download directory exists (it always should, but just in case)
if not os.path.exists("/storage/emulated/0/Download/"):
    os.makedirs("/storage/emulated/0/Download/")

while True:
    serial_code = generate_serial_code()
    payload = {
        "userId": user_id,
        "serialCode": serial_code
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        status = response.status_code

        if status == 200:
            alive_count += 1
            
            with open(output_path, "a") as f:
                f.write(f"{serial_code}\n")

        elif status == 400:
            dead_count += 1

        elif status == 409:
            used_count += 1

        print(f"Sent serialCode: {serial_code} | Status: {status} | Success: {alive_count} | Failed: {dead_count} | Failed (used already): {used_count} | Response: {response.text}")

    except Exception as e:
        print(f"Error sending request: {e}")

    time.sleep(1)  
