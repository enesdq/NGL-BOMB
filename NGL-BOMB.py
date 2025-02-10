import subprocess
import platform
import random
import time
import json
import os

color_yellow = "\033[93m"
color_green = "\033[92m"
color_red = "\033[91m"
color_reset = "\033[0m"

def clean():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")

clean()
print("This script is still only in development.")
print()
input("Press Enter to continue...")
clean()

print("""

 _     _____ _         ______ ________  ________ 
| \ | |  __ \ |        | ___ \  _  |  \/  | ___ \
|  \| | |  \/ |  ______| |_/ / | | | .  . | |_/ /
| . ` | | __| | |______| ___ \ | | | |\/| | ___ \
| |\  | |_\ \ |____    | |_/ | \_/ / |  | | |_/ /
\_| \_/\____|_____/    \____/ \___/\_|  |_|____/ 


""")

username = input("Enter username: ")

while True:
    msgcount = input("Amount of messages: ")
    if not msgcount.isdigit():
        print("Only numbers are allowed. Please try again.")
    else:
        msgcount = int(msgcount)
        if msgcount <= 0:
            print("Please enter a positive number.")
        else:
            break

message_option = input("Use custom messages? (y/n): ").lower()

messages = []

if message_option == 'y':
    print("Enter your custom messages (one per line). Press enter on an empty line to finish.")
    while True:
        message = input("> ")
        if not message:
            break
        messages.append(message)
else:
    with open("messages.txt", "r", encoding="utf-8") as file:
        messages = [line.strip() for line in file if line.strip()]

if not messages:
    print("No messages found.")
    exit()

all_messages = messages + [random.choice(messages).strip() for _ in range(msgcount - len(messages))]
random.shuffle(all_messages)

curl_command = [
    'curl',
    "-s",
    '-X', 'POST',
    '-H', 'Content-Type: application/json',
    '-H', 'Accept: application/json',
    '-d', '{{"username": "{}", "question": "{{message}}", "deviceId": "error"}}'.format(username, ''),
    'https://ngl.link/api/submit'
]

counter = 1

try:
    for message in all_messages[:msgcount]:
        encoded_message = json.dumps(message)
        encoded_message = encoded_message[1:-1]

        current_curl_command = list(curl_command)
        current_curl_command[9] = '{{"username": "{}", "question": "{}", "deviceId": "bro is paying for nothing"}}'.format(username, encoded_message)

        t = time.localtime()
        current_time = time.strftime("[INFO: \"""%H:%M:%S""\"]", t)

        try:
            output = subprocess.check_output(current_curl_command, stderr=subprocess.STDOUT)
            response = json.loads(output.decode('utf-8'))

            if "questionId" in response:
                print(f"{counter}." + color_yellow + current_time + color_reset + color_green + " Message sent successfully: " + color_reset + message)
            else:
                print(f"{counter}." + color_yellow + current_time + color_reset + color_red + " Something went wrong. " + color_reset + message)
            counter += 1

        except subprocess.CalledProcessError as e:
            print(f"Error executing cURL command: {e}")
        except json.JSONDecodeError:
            print(f"{counter}." + color_yellow + current_time + color_reset + color_red + " Too many messages! Ngl.Link cannot take it anymore." + color_reset)
            counter += 1

except Exception as ex:
    print(f"An error occurred: {ex}")
