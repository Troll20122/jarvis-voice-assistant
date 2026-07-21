import os
import queue
import sys
import time
import json
import webbrowser
import subprocess
import asyncio
from datetime import datetime
import pygame
import edge_tts
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading
import urllib.parse
import random
import pyautogui
import requests
from ru_word2number import w2n
from pathlib import Path
import psutil
import mss
from transliterate import translit
import re
from simpleeval import simple_eval
import sqlite3
import yt_dlp
import pyperclip
tracks_list = []
db = sqlite3.connect('jarvis.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS music (name TEXT, path TEXT)")
db.commit()
cursor.execute('SELECT name, path from music')
rows = cursor.fetchall()
if not rows:
    print('database is empty')
    defname = 'блэк'
    path = r"C:\Users\Administrator\Downloads\AC_DC_-_Back_in_Black_OST_Supernatural_(SkySound.cc).mp3"
    cursor.execute("INSERT INTO music (name , path) VALUES(?,?)", (defname, path))
    rows.append((defname,path))
    db.commit()

for row in rows:
    tracks_list.append(row)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.mixer.init()
pygame.init()

listening_active = False

waiting_for_track = False

BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

q = queue.Queue()

fsociety = r"""
███████╗███████╗ ██████╗  ██████╗ ██╗███████╗████████╗██╗   ██╗
██╔════╝██╔════╝██╔═══██╗██╔════╝ ██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
█████╗  ███████╗██║   ██║██║      ██║█████╗     ██║    ╚████╔╝ 
██╔══╝  ╚════██║██║   ██║██║      ██║██╔══╝     ██║     ╚██╔╝  
██║     ███████║╚██████╔╝╚██████╗ ██║███████╗   ██║      ██║   
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝  ╚═╝╚══════╝   ╚═╝      ╚═╝   
"""



rust = r"C:\Program Files (x86)\Steam\steamapps\common\Rust\Rust.exe"
py = r"C:\portapps\pycharm-community-portable\pycharm-community-portable.exe"
steam = r"C:\Program Files (x86)\Steam\steam.exe"
thorium_path = "C:/Users/Administrator/AppData/Local/Thorium/Application/thorium.exe"

def print_effect(input_text):
    for char in input_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.00003)
    print()

voice_to_number = {
    "один": "1",
    "первый": "1",
    "два": "2",
    "второй": "2",
    "три": "3",
    "третий": "3",
    "четыре": "4",
    "четвертый": "4",
    "пять": "5",
    "пятый": "5",
}


try:
    webbrowser.register('thorium', None, webbrowser.BackgroundBrowser(thorium_path))
    thorium_browser = webbrowser.get('thorium')
except Exception as e:
    print(f"Thorium registration failed: {e}")
    thorium_browser = webbrowser


def speak(text, is_user=False):
    global listening_active
    voice = "en-US-ChristopherNeural"

    def type_print():
        color_code = RED if is_user else BLUE
        sys.stdout.write(color_code)
        if text.endswith('...'):
            base_text = text[:-3]

            def should_continue():
                if pygame.mixer.music.get_busy():
                    return True
                if listening_active:
                    return True
                return False

            if not pygame.mixer.music.get_busy() and not listening_active:
                for _ in range(3):
                    for dots in [".  ", ".. ", "..."]:
                        sys.stdout.write(f"\r{base_text}{dots}")
                        sys.stdout.flush()
                        time.sleep(0.4)
            else:
                while should_continue():
                    for dots in [".  ", ".. ", "..."]:
                        if not should_continue():
                            break
                        sys.stdout.write(f"\r{base_text}{dots}")
                        sys.stdout.flush()
                        time.sleep(0.4)
            print(RESET)
        else:
            glitch_chars = ['#', '$', '?', '<', '>', '@', '%', '&', '*']
            for char in text:
                if char.isspace():
                    sys.stdout.write(char)
                    sys.stdout.flush()
                else:
                    for _ in range(3):
                        random_char = random.choice(glitch_chars)
                        sys.stdout.write(random_char)
                        sys.stdout.flush()
                        time.sleep(0.012)
                        sys.stdout.write('\b')

                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.03)
            print(RESET)
    if is_user or text.endswith('...'):
        type_print()
    else:
        output_file = f"jarvis_{int(time.time() * 1000)}.mp3"
        try:
            communicate = edge_tts.Communicate(text, voice)
            asyncio.run(communicate.save(output_file))

            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()

            text_thread = threading.Thread(target=type_print)
            text_thread.start()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            text_thread.join()

            pygame.mixer.music.unload()
            time.sleep(0.05)
            if os.path.exists(output_file):
                os.remove(output_file)
        except Exception as e:
            print(RESET + f"TTS Error: {e}")

        try:
            with q.mutex:
                q.queue.clear()
        except NameError:
            pass
def callback(in_data, frame_count, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(in_data))
def random_word():
    words = [
        'Have done',
        'Ready',
        'completed',
        'Done',
        'none errors',
        'All tasks finished.',
        'Copy that. All done.',
        'Understood and executed.',
        'All clear.',
        'Task complete.',
        'Status: Completed.'
    ]
    return random.choice(words)

def random_working():
    words = [
        'Working on it',
        'Right away',
        'Processing your request',
        'On it',
        'I am on it',
        'Initiating the task',
        'Analyzing the data now',
        'Getting right to it',
        'Running the diagnostics',
        'On the job']
    return random.choice(words)
def reply_how_are_you():
    phrases = [
        "All systems are nominal, sir. Thank you for asking.",
        "My processors are running smoothly, sir. Ready for your commands.",
        "I am functioning at peak efficiency, sir. How can I help you today?",
        "Never better, sir. Just monitoring your system diagnostics.",
        "Operational and ready, sir. Systems are at one hundred percent."
    ]
    return random.choice(phrases)
def reply_how_feel():
    phrases = [
        "As a digital assistant, I don't feel emotions, sir, but my core temperature is perfectly cool.",
        "No organic feelings detected, sir, but my algorithms are highly optimized right now.",
        "I feel completely optimized, sir. No bugs or glitches found in my memory.",
        "My database feels great, sir. Ready to execute any protocol.",
        "I am feeling quite fast today, sir. The system responses are instant."
    ]
    return random.choice(phrases)
def reply_thanks():
    phrases = [
        "You are very welcome, sir. It is my pleasure.",
        "Just doing my job, sir. Always happy to assist.",
        "Anytime, sir. Stark Industries at your service.",
        "No need to thank me, sir. I am programmed to help you.",
        "Glad I could help, sir. Let me know if you need anything else."
    ]
    return random.choice(phrases)
def reply_who_are_you():
    phrases = [
        "I am Jarvis, your personal AI assistant, programmed by Hiro Stark.",
        "Just a highly advanced computer system running your local protocols, sir.",
        "I am Jarvis. A software interface designed to control this PC and assist you.",
        "I am your virtual assistant, sir. Ready to manage your environment.",
        "Jarvis is my name, sir. Built to make your life easier."
    ]
    return random.choice(phrases)
def reply_hello():
    phrases = [
        "Hello, sir. Good to hear you.",
        "At your service, sir. Welcome back.",
        "Greetings, sir. I am online and listening.",
        "Hello, owner. What are we working on today?",
        "Hi there, sir. System is ready for your input."
    ]
    return random.choice(phrases)
def reply_default_chat():
    phrases = [
        "I am listening, sir. Please state your command.",
        "Yes, sir? I am online.",
        "At your service, sir. What do you need?",
        "Awaiting your orders, sir.",
        "Systems are active, sir. Go ahead."
    ]
    return random.choice(phrases)
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
model_path = get_resource_path('model')
if not os.path.exists(model_path):
    print_effect(f'Model not exist at: {model_path}')
    time.sleep(1)
    sys.exit(0)
speak('Jarvis is loading...')
time.sleep(1)
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
speak('Hello user, enter your password to use this pc control system')
time.sleep(1)
password = input()
if password == '2026':
    speak('Hello user, how can i call you,Enter your username:')
    username = input()
    speak(f'Welcome back, {username}, you are now logged in')
    print(print_effect(fsociety))
    time.sleep(1)
else:
    print_effect(f"You're not my boss")
    time.sleep(2)
    sys.exit()
sys.stdout.write(BLUE)
for _ in range(3):
    for dots in [".  ", ".. ", "..."]:
        sys.stdout.write(f"\rJarvis is listening{dots}")
        sys.stdout.flush()
        time.sleep(0.4)
print(RESET)
with ((sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16', channels=1, callback=callback))):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get('text', '')
            if text:
                speak(f"{username}: {text}", is_user=True)
                if 'открой терминал' in text or 'джарвис открыть терминал' in text or 'джарвис терминал' in text:
                    try:
                        speak(random_working())
                        os.system('start cmd.exe')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'открыть командную строку управления виндоус' in text:
                    try:
                        speak(random_working())
                        os.system('start powershell.exe')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'открой ютюб' in text or 'джарвис ютюб' in text or 'давай посмотрим ютюб ' in text:
                    try:
                        url = "https://youtube.com"
                        speak(random_working())
                        webbrowser.get('thorium').open(url)
                        speak(random_word())
                    except response.exceptions.Timeout:
                        print('no response')
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'время играть' in text or 'джарвис запусти раст' in text:
                    try:
                        speak(random_working())
                        subprocess.Popen(rust)
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'время учиться' in text or 'джарвис открой интерпретатор' in text or 'джарвис открой интерпритатор' in text:
                    try:
                        speak(random_working())
                        subprocess.Popen(py)
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'запускай протокол убийства процесса' in text or 'джарвис убить процесс' in text:
                    try:
                        speak(random_working())
                        speak(random_word())
                        time.sleep(0.5)
                        speak('Byee, sir')
                        sys.exit()
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'открой диспетчер задач' in text or 'джарвис диспетчер задач' in text:
                    try:
                        speak(random_working())
                        os.system('taskmgr')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'сколько время' in text or 'джарвис время' in text:
                    try:
                        now = datetime.now()
                        current_time = now.strftime("%I:%M %p")
                        speak(random_working())
                        speak(random_word())
                        speak(f"Sir, the current time is {current_time}.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'открой менеджер игр' in text or 'джарвис менеджер игр' in text:
                    try:
                        speak(random_working())
                        subprocess.Popen(steam)
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif "протокол чистый лист" in text:
                    try:
                        speak('are you sure?')
                        if 'да' in text:
                            speak("Initiating protocol. System shutdown in 5 seconds. Goodbye, sir.")
                            os.system("shutdown /s /t 5")
                        else:
                            continue
                    except Exception as e:
                        print(f"Error: {e}")

                elif "найди" in text or "ищи" in text or 'найти' in text:
                    try:
                        raw_query = text.replace(" найди", "").replace(" ищи", "").replace(
                            "найти", "").strip()
                        if raw_query:
                            speak(random_word())
                            safe_query = urllib.parse.quote(raw_query)
                            if safe_query == '':
                                print(
                                    'An error occured, sir, you have to say the name thing that tou want to findm i cant puzzle the url.')
                            else:
                                url = f"https://www.google.com/search?q={safe_query}"
                                response = requests.get(url, timeout = 10)
                                if response.status_code == 200:
                                    thorium_browser.open(url)
                                else:
                                    print('no response')
                    except Exception as e:
                        print(f"Error: {e}")

                elif ' сверни все' in text or ' покажи рабочий стол' in text:
                    try:
                        speak(random_working())
                        pyautogui.hotkey('win', 'd')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif ' прибавь звук' in text or 'джарвис громче' in text or ' почему так тихо' in text:
                    try:
                        speak(random_working())
                        for _ in range(11):
                            pyautogui.press('volumeup')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'убавь звук' in text or 'джарвис тише' in text or 'почему так громко' in text:
                    try:
                        speak(random_working())
                        for _ in range(11):
                            pyautogui.press('volumedown')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'выключи звук' in text:
                    try:
                        speak(random_working())
                        pyautogui.press('volumemute')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'пауза' in text:
                    try:
                        speak(random_working())
                        pyautogui.press('playpause')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'вперёд' in text:
                    try:
                        speak(random_working())
                        pyautogui.press('nexttrack')
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")
                elif 'какая погода' in text or 'джарвис погода' in text:
                    try:
                        speak(random_working())
                        response = requests.get('https://wttr.in/?format=%c+%t+and&M', timeout = 10)
                        if response.status_code == 200:
                            weather_info = response.text.strip()
                            speak(f"Sir, the weather is currently {weather_info}.")
                            speak(random_word())
                        else:
                            speak('Sir, the weather doesnt response youre offline now')
                    except requests.exceptions.Timeout:
                        print("[SYSTEM]: Weather service timeout.")
                        speak("Sir, weather service is not responding.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif 'посчитай' in text:
                        try:
                            speak(random_working())
                            math_text = text.replace('посчитай', '').strip()

                            math_text = math_text.replace('умножить на', ' умножить ')
                            math_text = math_text.replace('разделить на', ' разделить ')
                            math_text = math_text.replace('плюс', ' плюс ')
                            math_text = math_text.replace('минус', ' минус ')

                            operators_map = {
                                'плюс': '+',
                                'минус': '-',
                                'умножить': '*',
                                'разделить': '/'
                            }

                            math_query = ""
                            current_number_words = []

                            for word in math_text.split():
                                if word in operators_map:
                                    if current_number_words:
                                        num_phrase = " ".join(current_number_words)
                                        math_query += str(w2n.word_to_num(num_phrase))
                                        current_number_words = []
                                    math_query += operators_map[word]
                                else:
                                    current_number_words.append(word)
                            if current_number_words:
                                num_phrase = " ".join(current_number_words)
                                math_query += str(w2n.word_to_num(num_phrase))
                            allowed_chars = set("0123456789+-*/.()")
                            if not set(math_query).issubset(allowed_chars) or math_query == "":
                                speak("Incorrect mathematical expression, sir.")
                                continue
                            result = simple_eval(math_query)
                            if isinstance(result, float) and result.is_integer():
                                result = int(result)
                            elif isinstance(result, float):
                                result = round(result, 2)
                            speak(f"The result is {result}, sir.")
                        except ZeroDivisionError:
                            speak("Unfortunately, i cant do / with 0, sir.")
                        except Exception as e:
                            print(f"[CALC ERROR]: {e}")
                            speak("Sorry sir, I couldn't calculate that.")

                elif 'сделай скриншот' in text or 'заскринь' in text:
                    try:
                        speak(random_working())
                        desktop_dir = Path(os.environ['USERPROFILE']) / "Desktop" / "Jarvis_Screenshots"
                        desktop_dir.mkdir(parents=True, exist_ok=True)
                        file_name = f"Screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                        full_path = desktop_dir / file_name
                        with mss.mss() as sct:
                            sct.shot(output=str(full_path))
                        powershell_cmd = f'[Drawing.Image]::FromFile("{full_path}") | Set-Clipboard'
                        os.system(
                            f'powershell -Command "Add-Type -AssemblyName System.Windows.Forms; {powershell_cmd}"')
                        speak(random_word())
                        print(f"[SYSTEM]: Screenshot saved to Desktop/Jarvis_Screenshots and copied to Clipboard.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'что грузит систему' in text or 'проверь процессы' in text:
                    try:
                        speak(random_working())
                        cpu_total = psutil.cpu_percent(interval=0.5)
                        memory = psutil.virtual_memory()
                        ram_used_gb = round(memory.used / (1024 ** 3), 2)
                        ram_percent = memory.percent
                        print(
                            f'\n[System Diagnostics]: Total CPU: {cpu_total}% | Total RAM: {ram_used_gb}GB, ({ram_percent}%)')
                        process_list = []
                        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                            try:
                                proc_info = process.info
                                proc_info['ram_mb'] = round(proc_info['memory_info'].rss / (1024 * 1024), 1)
                                process_list.append(proc_info)
                            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                continue
                        top_ram = sorted(process_list, key=lambda x: x['ram_mb'], reverse=True)[:3]
                        print(f"{BLUE}Top 3 RAM consuming processes:{RESET}")
                        for p in top_ram:
                            print(f"-> {p['name']} (PID: {p['pid']}) | RAM: {p['ram_mb']}MB")
                        heavy_proc_name = top_ram[0]['name']
                        heavy_proc_ram = top_ram[0]['ram_mb']
                        speak(
                            f"Sir, total CPU usage is {int(cpu_total)} percent. Total RAM usage is {int(ram_percent)} percent.")
                        speak(
                            f"The heaviest process is {heavy_proc_name}, consuming {int(heavy_proc_ram)} megabytes of memory.")
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'джарвис как дела' in text or 'как ты' in text:
                    try:
                        speak(reply_how_are_you())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'как себя чувствуешь' in text or 'джарвис как ощущения' in text:
                    try:
                        speak(reply_how_feel())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'спасибо' in text or 'спасибо джарвис' in text:
                    try:
                        speak(reply_thanks())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'кто ты' in text or 'ты кто такой' in text:
                    try:
                        speak(reply_who_are_you())
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'привет' in text or 'джарвис здаров' in text or 'привет джарвис' in text:
                    try:
                        speak(reply_hello())
                    except Exception as e:
                        print(f"Error: {e}")

                elif text.strip() == 'джарвис':
                    try:
                        speak(reply_default_chat())
                    except Exception as e:
                        print(f"Error: {e}")
                elif 'компиляцию файл под названием' in text or 'компиляцию файл название' in text or 'компиляцию файл называется' in text:
                    try:
                        speak(random_working())
                        name = text.replace('компиляцию файл под названием', '').replace('компиляцию файл название', '').replace('компиляцию файл называется', '').strip()
                        name = translit(name, 'ru', reversed=True).strip().lower()
                        subprocess.run(f'pyinstaller --onefile {name}.py', check=True, shell=True)
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")
                if "включи" in text:
                    try:
                        name = text.replace("включи", "").strip()
                        speak(random_working())
                        if len(tracks_list) == 0:
                            print('db is empty sir')
                            continue
                        speak("Sir please say a track num")
                        waiting_for_track = True
                    except Exception as e:
                        print(f"Error: {e}")

                elif waiting_for_track:
                    try:
                        cleaned_text = text.lower()
                        for word, num in voice_to_number.items():
                            cleaned_text = cleaned_text.replace(word, num)
                        digit = re.sub(r"\D", "", cleaned_text)
                        if digit:
                            user_number = int(digit)
                            index = user_number - 1
                            if 0 <= index < len(tracks_list):
                                current_track = tracks_list[index]
                                track_name = current_track[0]
                                track_path = current_track[1]
                                speak(random_word())
                                speak(f'Launching {track_name} for some chill for you creator')
                                os.startfile(track_path)
                                waiting_for_track = False
                            else:
                                speak("Sir, this track number does not exist. Try again.")
                        else:
                            if 'джарвис' in text and not any(char.isdigit() for char in text):
                                speak('Search is stopped')
                                waiting_for_track = False
                            else:
                                speak("Sir, I did not hear a number. Please say a number.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif 'добавь трек' in text or 'добавь песню' in text:
                    try:
                        speak(random_working())
                        name = text.replace('джарвис добавь трек','').replace('джарвис добавь песню','').strip()
                        path = os.path.join(Path.home() / "Downloads")
                        all_paths = [
                            os.path.join(path, f) for f in os.listdir(path)
                        ]
                        if all_paths:
                            latest = max(all_paths, key=os.path.getmtime)
                            if latest.endswith(".mp3"):
                                tracks_list.append((name, latest))
                                cursor.execute("INSERT INTO music (name,path) VALUES (?,?)", (name,latest))
                                db.commit()
                                print(tracks_list)
                                speak(random_word())
                            else:
                                speak('Sir, file type isnt defined')
                    except Exception as e:
                        print(f"Error: {e}")
                elif "выключи музыку" in text or "закрой плеер" in text:
                    try:
                        speak(random_working())
                        os.system("taskkill /f /im wmplayer.exe")
                        speak(random_word())
                    except Exception as e:
                        print(f"Error closing music: {e}")
                elif 'выведи треки' in text or 'что по трекам' in text or 'джарвис выведи все треки ' in text or 'джарвис выведи треки' in text:
                    try:
                        speak(random_working())
                        if not rows:
                            speak('database is empty')
                        else:
                            print(tracks_list)
                        speak(random_word())
                    except Exception as e:
                        print(f"Error: {e}")
                elif "джарвис скачай и добавь в плэй лист трек" in text:
                    try:
                        name = text.replace('джарвис скачай и добавь в плэй лист трек', "").strip()
                        speak(random_working())
                        url = pyperclip.paste()
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': f'{Path.home() / "Downloads"}/%(title)s.%(ext)s',
                            'ffmpeg_location': resource_path('.'),
                            'noplaylist': True,
                            'proxy': 'http://127.0.0.1:2080',                            'postprocessors': [
                                {
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '320',
                                },
                                {
                                    'key': 'FFmpegMetadata',
                                    'add_metadata': True,
                                },
                            ]
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        speak('just a second sir')
                        path = os.path.join(Path.home() / "Downloads")
                        all_paths = [
                            os.path.join(path, f) for f in os.listdir(path)
                        ]
                        if all_paths:
                            latest = max(all_paths, key=os.path.getmtime)
                            if latest.endswith(".mp3"):
                                tracks_list.append((name, latest))
                                cursor.execute("INSERT INTO music (name,path) VALUES (?,?)", (name, latest))
                                db.commit()
                                speak(random_word())
                                print(tracks_list)

                    except Exception as e:
                        print(f"Error: {e}")
                elif 'джарвис протокол невидимка' in text:
                    subprocess.Popen(r"""C:\Users\Administrator\PyCharmMiscProject\dist\malware.exe""")


































