import os
import json
import subprocess

import pyautogui
import keyboard
import psutil

from PIL import Image

import mss
from events import event_bus

from config import (
    ENABLE_DESKTOP_CONTROL,
    ENABLE_BROWSER,
    SCREENSHOT_DIR,
    SAFE_MODE,
    WORKSPACE_DIR
)

from browser import browser

from vision import vision

# =========================================
# TOOL REGISTRY
# =========================================

TOOLS = {}

# =========================================
# REGISTER TOOL
# =========================================

def register_tool(
    name,
    description,
    func
):
    TOOLS[name] = {

        "description": description,

        "func": func
    }

#TOOL_BROWSER
def tool_browser_open(args):

    url = args.get("url")

    if not url:

        return "Missing url."

    return browser.open(url)

register_tool(
    "browser_open",
    "Open browser page",
    tool_browser_open
)

#GOOGLE_search
def tool_google(args):

    query = args.get("query")

    if not query:

        return "Missing query."

    return browser.google(query)

register_tool(
    "google_search",
    "Search Google",
    tool_google
)

#click
def tool_browser_click(args):

    selector = args.get("selector")

    if not selector:

        return "Missing selector."

    return browser.click(selector)

register_tool(
    "browser_click",
    "Click page element",
    tool_browser_click
)

#type
def tool_browser_type(args):

    selector = args.get("selector")

    text = args.get("text")

    if not selector:

        return "Missing selector."

    return browser.type(
        selector,
        text
    )

register_tool(
    "browser_type",
    "Type into browser field",
    tool_browser_type
)

#html
def tool_browser_html(args):

    return browser.html()

register_tool(
    "browser_html",
    "Get page html",
    tool_browser_html
)

#title
def tool_browser_title(args):

    return browser.title()

register_tool(
    "browser_title",
    "Get page title",
    tool_browser_title
)

#screenshot
def tool_browser_screenshot(args):

    return browser.screenshot()

register_tool(
    "browser_screenshot",
    "Take browser screenshot",
    tool_browser_screenshot
)

#close
def tool_browser_close(args):

    return browser.close()

register_tool(
    "browser_close",
    "Close browser",
    tool_browser_close
)

#screen_ocr
def tool_read_screen(args):

    return vision.read_screen()

register_tool(
    "read_screen",
    "Read text from screen",
    tool_read_screen
)

#active_window
def tool_active_window(args):

    return vision.active_window()

register_tool(
    "active_window",
    "Get active window",
    tool_active_window
)

#analyze_screen
def tool_analyze_screen(args):

    return vision.analyze_screen()

register_tool(
    "analyze_screen",
    "Analyze current screen",
    tool_analyze_screen
)

#ocr_image
def tool_ocr_image(args):

    path = args.get("path")

    if not path:

        return "Missing path."

    return vision.read_text(path)

register_tool(
    "ocr_image",
    "Read text from image",
    tool_ocr_image
)
# =========================================
# EXECUTE TOOL
# =========================================

def execute_tool(
    tool_name,
    args

):
    event_bus.emit(

        "tool_start",

        {
            "tool": tool_name,
            "args": args
        }
    )

    if tool_name not in TOOLS:

        return (
            f"Tool '{tool_name}' "
            f"not found."
        )

    try:

        result = (
            TOOLS[tool_name]
            ["func"](args)
        )

    except Exception as e:

        result = (
            f"Tool error: {e}"
        )

    event_bus.emit(

        "tool_finish",

        {
            "tool": tool_name,
            "result": str(result)
        }
    )

    return result

#safe
def safe_path(path):

    full = os.path.abspath(path)

    workspace = os.path.abspath(
        WORKSPACE_DIR
    )

    if not full.startswith(
        workspace
    ):
        raise Exception(
            "Path outside workspace."
        )

    return full


# =========================================
# LIST TOOLS
# =========================================

def list_tools():

    result = []

    for name, tool in TOOLS.items():

        result.append({

            "name": name,

            "description":
                tool["description"]
        })

    return result

# =====================================================
# TOOL: OPEN URL
# =====================================================

def tool_open_url(args):

    if not ENABLE_BROWSER:

        return "Browser disabled."

    url = args.get("url")

    if not url:

        return "Missing url."

    os.system(f'start {url}')

    return f"Opened {url}"

register_tool(
    "open_url",
    "Open website in browser",
    tool_open_url
)

# =====================================================
# TOOL: TYPE TEXT
# =====================================================

def tool_type_text(args):

    if not ENABLE_DESKTOP_CONTROL:

        return (
            "Desktop control disabled."
        )

    text = args.get("text", "")

    pyautogui.write(
        text,
        interval=0.02
    )

    return "Text typed."

register_tool(
    "type_text",
    "Type text on keyboard",
    tool_type_text
)

# =====================================================
# TOOL: PRESS KEY
# =====================================================

def tool_press_key(args):

    if not ENABLE_DESKTOP_CONTROL:

        return (
            "Desktop control disabled."
        )

    key = args.get("key")

    if not key:

        return "Missing key."

    keyboard.press_and_release(
        key
    )

    return f"Pressed {key}"

register_tool(
    "press_key",
    "Press keyboard key",
    tool_press_key
)

# =====================================================
# TOOL: HOTKEY
# =====================================================

def tool_hotkey(args):

    if not ENABLE_DESKTOP_CONTROL:

        return (
            "Desktop control disabled."
        )

    keys = args.get("keys")

    if not keys:

        return "Missing keys."

    pyautogui.hotkey(*keys)

    return (
        f"Pressed hotkey: "
        f"{keys}"
    )

register_tool(
    "hotkey",
    "Press keyboard hotkey",
    tool_hotkey
)

# =====================================================
# TOOL: OPEN APP
# =====================================================

def tool_open_app(args):

    app = args.get("app")

    if not app:

        return "Missing app."

    subprocess.Popen(app)

    return f"Opened app: {app}"

register_tool(
    "open_app",
    "Open application",
    tool_open_app
)

# =====================================================
# TOOL: SCREENSHOT
# =====================================================

def tool_screenshot(args):

    path = os.path.join(
        SCREENSHOT_DIR,
        "screen.png"
    )

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(
            monitor
        )

        image = Image.frombytes(

            "RGB",

            screenshot.size,

            screenshot.rgb
        )

        image.save(path)

    return path

register_tool(
    "screenshot",
    "Take screenshot",
    tool_screenshot
)

# =====================================================
# TOOL: SYSTEM INFO
# =====================================================

def tool_system_info(args):

    return {

        "cpu_percent":
            psutil.cpu_percent(),

        "ram_percent":
            psutil.virtual_memory().percent,

        "disk_percent":
            psutil.disk_usage("/").percent
    }

register_tool(
    "system_info",
    "Get system information",
    tool_system_info
)

# =====================================================
# TOOL: READ FILE
# =====================================================

def tool_read_file(args):

    path = args.get("path")

    if not path:

        return "Missing path."

    if not os.path.exists(path):

        return "File not found."

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

register_tool(
    "read_file",
    "Read text file",
    tool_read_file
)

# =====================================================
# TOOL: WRITE FILE
# =====================================================

def tool_write_file(args):

    path = args.get("path")

    content = args.get(
        "content",
        ""
    )

    if not path:

        return "Missing path."

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    return f"Written to {path}"

register_tool(
    "write_file",
    "Write text file",
    tool_write_file
)

# =====================================================
# TOOL: LIST FILES
# =====================================================

def tool_list_files(args):

    path = args.get("path", ".")

    if not os.path.exists(path):

        return "Path not found."

    return os.listdir(path)

register_tool(
    "list_files",
    "List directory files",
    tool_list_files
)

# =====================================================
# TOOL: MOUSE CLICK
# =====================================================

def tool_mouse_click(args):

    if SAFE_MODE:

        return (
            "Mouse disabled in safe mode."
        )

    x = args.get("x")

    y = args.get("y")

    if x is None or y is None:

        return "Missing coordinates."

    pyautogui.click(x, y)

    return (
        f"Clicked at {x}, {y}"
    )

register_tool(
    "mouse_click",
    "Click mouse",
    tool_mouse_click
)

# =====================================================
# TOOL: MOVE MOUSE
# =====================================================

def tool_move_mouse(args):

    if SAFE_MODE:

        return (
            "Mouse disabled in safe mode."
        )

    x = args.get("x")

    y = args.get("y")

    if x is None or y is None:

        return "Missing coordinates."

    pyautogui.moveTo(x, y)

    return (
        f"Moved mouse to {x}, {y}"
    )

register_tool(
    "move_mouse",
    "Move mouse",
    tool_move_mouse
)