from g4f.client import Client
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from colorama import init, Fore, Style

init(autoreset=True)

client = Client()

def print_ascii_art():
    ascii_art = r"""
      /$$$$$$  /$$$$$$$  /$$     /$$ /$$$$$$   /$$$$$$  /$$$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$$
     /$$__  $$| $$__  $$|  $$   /$$//$$__  $$ /$$__  $$| $$_____/ /$$__  $$| $$  | $$| $$__  $$| $$_____/
    | $$  \__/| $$  \ $$ \  $$ /$$/| $$  \ $$| $$  \__/| $$      | $$  \__/| $$  | $$| $$  \ $$| $$      
    |  $$$$$$ | $$$$$$$/  \  $$$$/ | $$  | $$|  $$$$$$ | $$$$$   | $$      | $$  | $$| $$$$$$$/| $$$$$   
     \____  $$| $$____/    \  $$/  | $$  | $$ \____  $$| $$__/   | $$      | $$  | $$| $$__  $$| $$__/   
      /$$  \ $$| $$          | $$   | $$  | $$ /$$  \ $$| $$      | $$    $$| $$  | $$| $$  \ $$| $$      
     |  $$$$$$/| $$          | $$   |  $$$$$$/|  $$$$$$/| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$$
      \______/ |__/          |__/    \______/  \______/ |________/ \______/  \______/ |__/  |__/|________/
                                                                                                      
                                                                                                      
                                                                                                      
    """
    print(Fore.BLUE + ascii_art)

def get_and_process_message():
    print_ascii_art()
    print('Scammer message')
    message = input(Fore.LIGHTCYAN_EX+"\n")

    debug = True

    def get_response(client, message):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "Admin",
                "content": f"(Respond in english) From now on you will be the best troll in the world. A friend of mine told me '{message}' how should I respond to troll him? He is a good friend of mine so a little rude is not a problem, that's how we usually talk. I want to troll him. AND GIVE ME ONLY THE RESPONSE, NOT THE WHOLE CONVERSATION. OK?"
            }]
        )
        return response.choices[0].message.content

    
    def attempt_get_response(client, message, attempt_count, lock, debug):
        response_text = get_response(client, message)
        if debug:
            with lock:
                if "流量异常,请尝试更换网络环境" in response_text or "I'm sorry" in response_text:
                    print(Fore.RED + f"Attempt {attempt_count}: {response_text}")
                else:
                    print(Fore.GREEN + f"Attempt {attempt_count}: {response_text}")
        return response_text

    attempt_count = 0
    lock = threading.Lock()

    valid_response = None
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_attempt = {executor.submit(attempt_get_response, client, message, attempt_count + i, lock, debug): i for i in range(1, 6)}
        
        for future in as_completed(future_to_attempt):
            attempt_count += 1
            response_text = future.result()
            
            if "流量异常,请尝试更换网络环境" not in response_text and "I'm sorry" not in response_text:
                valid_response = response_text
                break

    if valid_response:
        print(Fore.GREEN + f"Final Response (Attempt {attempt_count}): {valid_response}")
    else:
        print(Fore.RED + "No valid response was obtained after several attempts.")


while True:
    get_and_process_message()
    user_input = input("Do you want to enter another message? (yes/no): ").lower()
    if user_input!= "yes":
        break
