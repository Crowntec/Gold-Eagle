import requests
import json
import time
import random
import logging
#from colorama 
import Fore, Back, Style

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read authentication tokens from data.txt
with open("data.txt", "r") as file:
    auth_tokens = [line.strip() for line in file if line.strip()]

# API URLs
tap_url = "https://gold-eagle-api.fly.dev/tap"
claim_url = "https://gold-eagle-api.fly.dev/wallet/claim"

# Headers template (common for all requests except Authorization)
headers_template = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://telegram.geagle.online",
    "priority": "u=1, i",
    "referer": "https://telegram.geagle.online/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
}

def send_tap_request(auth_token):
    """Send tap request using a specific authorization token."""
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    data = {
        "available_taps": 1000,
        "count": random.randint(998, 1000),  # Number of taps as random number
        "timestamp": int(time.time()),  # Generate current timestamp
        "salt": "[ID]"
    }

    try:
        response = requests.post(tap_url, headers=headers, data=json.dumps(data))
        logging.info(f"{Fore.GREEN}TAP Response {response.text} - {response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}TAP Request failed for {e}{Style.RESET_ALL}")

def send_claim_request(auth_token):
    """Send claim request using a specific authorization token."""
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"
    headers["content-length"] = "0"

    try:
        response = requests.post(claim_url, headers=headers)
        logging.info(f"{Fore.GREEN}CLAIM Response {response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}CLAIM Request failed for {e}{Style.RESET_ALL}")

cycle_count = 0  # Track cycles

# Print the ASCII art banner
banner = '''
░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗
██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║
██║░░╚═╝██████╔╝██║░░██║░╚██╗████╗██╔╝██╔██╗██║
██║░░██╗██╔══██╗██║░░██║░░████╔═████║░██║╚████║
╚█████╔╝██║░░██║╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║
░╚════╝░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝

█████████████████████████████████████
█▄─▄▄─█▄─▄▄▀█▄─▄█▄─▀█▄─▄█─▄▄▄─█▄─▄▄─█
██─▄▄▄██─▄─▄██─███─█▄▀─██─███▀██─▄█▀█
▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
channel: https://t.me/crown_prince_hacks
Buy me coffee usdt: 0x4ee70e0f1bb829389b5b7f81af9fcafea2986885bde8b238b4b96e6df0628acc

'''

while True:
    cycle_count += 1
    print("\033c", end="")  # Clear the screen before starting a new cycle
    print(banner)
    logging.info(f"{Fore.BLUE}Starting Cycle {cycle_count}{Style.RESET_ALL}...")

    for token in auth_tokens:
        send_tap_request(token)
        time.sleep(2)  # Small delay between requests to avoid rate limits

    if cycle_count % 10 == 0:  # Every 10 cycles, send claim requests
        logging.info(f"{Fore.CYAN}Sending CLAIM requests for all accounts...{Style.RESET_ALL}")
        for token in auth_tokens:
            send_claim_request(token)
            time.sleep(1)  # Small delay between requests

    logging.info(f"{Fore.YELLOW}Waiting 15 minutes before the next cycle...{Style.RESET_ALL}")
    total_seconds = 1003  #  in seconds
    for i in range(total_seconds, 0, -1):
        minutes, seconds = divmod(i, 60)
        progress_bar = "█" * int(i / total_seconds * 20) + "-" * (20 - int(i / total_seconds * 20))
        print(f"\r{Fore.MAGENTA}{minutes:02d}:{seconds:02d} [{progress_bar}]{Style.RESET_ALL}", end="")
        time.sleep(1)
    print("\n")  # New line after the countdown

