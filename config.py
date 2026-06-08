import os

from dotenv import load_dotenv

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# APP
# =========================================

APP_NAME = "Jarvis"

DEBUG = True

# =========================================
# MODEL
# =========================================

MODELS_NAME = (
    "openai/gpt-oss-120b:free",

    "openrouter/owl-alpha",

    "meta-llama/llama-3.3-70b-instruct:free",

    "mistralai/mistral-small-3.2-24b-instruct:free",

    "deepseek/deepseek-r1-0528:free"
)

WORKSPACE_DIR = "workspace"

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    ""
)

USER_MEMORY_FILE = (
    "user_memory.json"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

# =========================================
# TELEGRAM
# =========================================

ENABLE_TELEGRAM = True

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""
)

# =========================================
# DISCORD
# =========================================

ENABLE_DISCORD = True
ENABLE_DISCORD_VOICE = True
DISCORD_BOT_TOKEN = os.getenv(
    "DISCORD_BOT_TOKEN",
    ""
)

# =========================================
# MEMORY
# =========================================

MEMORY_FILE = "memory.json"

MEMORY_LIMIT = 200

MEMORY_SUMMARY_LIMIT = 20

# =========================================
# AUTONOMOUS MODE
# =========================================

ENABLE_AUTONOMOUS = True

AUTO_LOOP_DELAY = 2

MAX_TASK_RETRIES = 3

# =========================================
# VOICE
# =========================================

ENABLE_VOICE = False

VOICE_LANGUAGE = "ru"

VOICE_WAKE_WORD = "джарвис"

# =========================================
# BROWSER
# =========================================

ENABLE_BROWSER = True

BROWSER_HEADLESS = False

# =========================================
# DESKTOP CONTROL
# =========================================

ENABLE_DESKTOP_CONTROL = True

SAFE_MODE = True

# =========================================
# SCREENSHOT
# =========================================

SCREENSHOT_DIR = "screenshots"

# =========================================
# LOGGING
# =========================================

LOG_LEVEL = "INFO"

LOG_FILE = "jarvis.log"

# =========================================
# TOOLS
# =========================================

ENABLE_FILE_TOOLS = True

ENABLE_SYSTEM_TOOLS = True

ENABLE_WEB_TOOLS = True

# =========================================
# AGENT
# =========================================

SYSTEM_PROMPT = """
You are Jarvis.

You are:
- helpful
- autonomous
- concise
- intelligent

You can:
- answer questions
- use tools
- automate tasks
- help user

If tool required:
respond ONLY in JSON.

Example:

{
  "tool": "open_url",
  "args": {
    "url": "https://youtube.com"
  }
}

Otherwise respond normally.
"""

# =========================================
# DIRECTORIES
# =========================================

DATA_DIR = "data"

TEMP_DIR = "temp"

LOGS_DIR = "logs"

# =========================================
# CREATE DIRS
# =========================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(
    TEMP_DIR,
    exist_ok=True
)

os.makedirs(
    LOGS_DIR,
    exist_ok=True
)

os.makedirs(
    SCREENSHOT_DIR,
    exist_ok=True
)

os.makedirs(
    WORKSPACE_DIR,
    exist_ok=True
)



