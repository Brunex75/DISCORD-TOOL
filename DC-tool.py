import ctypes
import string
import os
import time
import requests
import numpy
import platform
import json
import random
from pystyle import Colorate, Colors
from os import system
from discord_webhook import DiscordWebhook
from colorama import Fore, Style, init

# Ustawienia
USE_WEBHOOK = True
MAIN_COLOR = "\033[36m"

# Logo
logo = f"""{MAIN_COLOR}    
    ____  _                          __   __              __
   / __ \\(_)_____________  _________/ /  / /_____  ____  / /
  / / / / / ___/ ___/ __ \\/ ___/ __  /  / __/ __ \\/ __ \\/ / 
 / /_/ / (__  ) /__/ /_/ / /  / /_/ /  / /_/ /_/ / /_/ / /  
/_____/_/____/\\___/\\____/_/   \\____/   \\__/\\____/\\____/_/

             By Brunexz
"""

# Menu
menu = f"""{MAIN_COLOR}                  
[1] WEBHOOK SENDER
[2] WEBHOOK SPAM
[3] NITRO GEN
"""

# Klasa generatora Nitro
class NitroGen:
    def __init__(self):
        self.fileName = "Nitro_Codes.txt"
        self.valid = []
        self.invalid = 0

    def main(self):
        num = input(f"{MAIN_COLOR}Enter the number of codes to generate and check: ")
        try:
            num = int(num)
        except ValueError:
            input(f"{MAIN_COLOR}Invalid input. Please enter a number.\nPress Enter to exit")
            return

        webhook = None
        if USE_WEBHOOK:
            url = input(f"{MAIN_COLOR}Enter Discord webhook URL (or leave blank to skip): ")
            if url.strip():
                webhook = url
                DiscordWebhook(url=webhook, content="Started checking codes...").execute()

        chars = string.ascii_letters + string.digits
        c = numpy.random.choice(list(chars), size=[num, 16])

        for s in c:
            code = ''.join(s)
            url = f"https://discord.gift/{code}"
            result = self.quickChecker(url, webhook)
            if result:
                self.valid.append(url)
            else:
                self.invalid += 1

            if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Nitro Generator - {len(self.valid)} Valid | {self.invalid} Invalid"
                )

        print(f"{MAIN_COLOR}\nResults:\n Valid: {len(self.valid)}\n Invalid: {self.invalid}")
        if self.valid:
            print(f"Valid Codes: {', '.join(self.valid)}")

        input(f"{MAIN_COLOR}Press Enter to return...")

    def quickChecker(self, nitro: str, notify=None):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{MAIN_COLOR}Valid | {nitro}")
                with open(self.fileName, "a") as file:  
                    file.write(nitro + "\n")
                if notify:
                    DiscordWebhook(url=notify, content=f"Valid Nitro Code found! {nitro}").execute()
                return True
            else:
                print(f"{MAIN_COLOR}Invalid | {nitro}")
                return False
        except requests.exceptions.RequestException:
            print(f"{MAIN_COLOR}Error connecting to Discord API.")
            return False

# Czyszczenie ekranu
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Interfejs użytkownika
def main():
    while True:
        clear_screen()
        os.system("title DiscordTool")
        print(logo)
        print(menu)
        print()
        username = os.getlogin()
        q = input(f"{MAIN_COLOR}{username}> ")

        if q == "1":
            clear_screen()
            url = input(f"{MAIN_COLOR}Webhook URL: ")
            message = input(f"{MAIN_COLOR}Message: ")
            name = input(f"{MAIN_COLOR}Webhook name: ")

            data = {
                "content": message,
                "username": name
            }
            try:
                r = requests.post(url, json=data)
                if r.status_code == 204:
                    print(f"{MAIN_COLOR}Webhook successfully sent!")
                else:
                    print(f"{MAIN_COLOR}Error sending webhook: {r.status_code}")
            except requests.exceptions.RequestException:
                print(f"{MAIN_COLOR}Error sending webhook")

            input(f"{MAIN_COLOR}Press enter to return...")

        elif q == "2":
            clear_screen()
            message = input("Message: ")
            webhookurl = input("Webhook URL: ")
            delay = input("Delay (in seconds): ")

            try:
                delay = int(delay)
            except ValueError:
                print("Invalid delay. Using default (1 second).")
                delay = 1

            webhook = DiscordWebhook(url=webhookurl, content=message)

            print("Press CTRL + C to stop spam!")

            try:
                while True:
                    webhook.execute()
                    print(f"Sent: {message}")
                    time.sleep(delay)
            except KeyboardInterrupt:
                print("\nSpam stopped.")
                input(f"{MAIN_COLOR}Press Enter to return...")  
                main()  # Po zatrzymaniu wraca do menu zamiast zamykać program

        elif q == "3":  
            clear_screen()
            NitroGen().main()

        else:
            print("Invalid option. Try again.")

# Uruchomienie programu
if __name__ == "__main__":
    main()
