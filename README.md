# PC Jarvis 🤖

An advanced, offline voice-controlled AI assistant built in Python for total Windows automation, system monitoring, and media control.

---

## 🛠️ Complete Voice Commands List

### 🔒 Security & System Protocols
* **"джарвис" (On Startup)** — Requests the security password. Enter or speak **`2026`** to unlock Jarvis.
* **"протокол невидимка"** — Lock Protocol. Immediately locks the Windows screen for security when the user steps away.
* **"протокол чистый лист"** — Wipe Protocol. Initiates a forced Windows shutdown after a 5-second countdown.
* **"запускай протокол убийства процесса"** — Self-Destruct. Safely terminates the Jarvis process and closes the application.

### 🌐 Automation & File Compilation
* **"включи компиляцию файл под названием [имя]"** — Automated File Creator. Uses `transliterate` to automatically convert Russian spoken file names into clean English characters (latin letters) and generates the file.
* **"открыть командную строку управления виндоус" / "открой терминал"** — Launches the Windows Command Prompt (CMD).

### 🎵 Media & YouTube Integration
* **"джарвис скачай и добавь в плэй лист трек [название]"** — Downloads any audio from YouTube via `yt-dlp` and automatically registers it into the local SQLite database.
* **"выведи треки"** — Lists all available songs stored in the Jarvis music library.
* **"включи компиляцию"** — Starts playing a custom-compiled music mix.
* **"выключи музыку" / "пауза"** — Stops or pauses current audio playback.
* **"прибавь звук" / "убавь звук" / "выключи звук"** — Controls Master OS Volume levels.

### 🖥️ Windows & Apps Management
* **"открой ютюб"** — Opens YouTube in your default browser.
* **"покажи рабочий стол"** — Minimizes all active windows to reveal the Desktop.
* **"открой диспетчер задач"** — Launches Windows Task Manager.
* **"открой менеджер игр"** — Launches Steam or your configured gaming platform.
* **"время играть"** — Launches Rust (Steam).
* **"время учиться"** — Launches PyCharm IDE.

### 🧠 Utilities & Social Chitchat
* **"что грузит систему"** — Uses `psutil` to analyze CPU/RAM loads and reports what is slowing down the PC.
* **"сделай скриншот"** — Captures a high-performance screenshot instantly via `mss`.
* **"какая погода" / "джарвис погода"** — Fetches live weather conditions in real-time via `wttr.in` without requiring any API keys.
* **"посчитай [выражение]"** — Safely parses and evaluates mathematical formulas out loud using `simpleeval`.
* **"сколько время"** — Speaks the current local time.
* **"привет" / "кто ты" / "как дела" / "как себя чувствуешь" / "спасибо"** — Friendly conversation commands with simulated AI system logic.

---

## 🚀 Installation & Setup

### 1. Prerequisites
* **Python** 3.10 or newer.

### 2. Install Dependencies
Install all required libraries at once with this command:
```bash
pip install Pillow pygame edge-tts sounddevice vosk pyautogui requests ru-word2number psutil mss yt-dlp transliterate simpleeval pyperclip
```

### 3. Voice Model Configuration
1. Download the offline Russian speech recognition model from the official Vosk website (e.g., `vosk-model-small-ru-0.22`).
2. Extract the archive into the project root directory.
3. Rename the folder to exactly `model`.

### 4. Database Setup
On the first run, Jarvis creates an SQLite database `jarvis.db` automatically. It looks for a default track to seed the database. Make sure to download a starting track (e.g., *AC/DC - Back in Black*) and place it in your target path or change this line inside `pcjarvis.py` to a relative path:
```python
path = r"C:\Users\Administrator\Downloads\AC_DC_-_Back_in_Black_OST_Supernatural_(SkySound.cc).mp3"
```

