import os
from datetime import datetime

import pytesseract

from PIL import Image

import mss

import pygetwindow as gw

from config import (

    SCREENSHOT_DIR,

    DEBUG
)

# =========================================
# TESSERACT PATH (WINDOWS)
# =========================================

pytesseract.pytesseract.tesseract_cmd = (

    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =========================================
# VISION CLASS
# =========================================

class Vision:

    def __init__(self):

        pass

    # =====================================
    # SCREENSHOT
    # =====================================

    def screenshot(self):

        filename = (

            f"screen_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            f".png"
        )

        path = os.path.join(

            SCREENSHOT_DIR,

            filename
        )

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            shot = sct.grab(
                monitor
            )

            image = Image.frombytes(

                "RGB",

                shot.size,

                shot.rgb
            )

            image.save(path)

        if DEBUG:

            print(
                f"[VISION] Screenshot: {path}"
            )

        return path

    # =====================================
    # OCR
    # =====================================

    def read_text(
        self,
        image_path
    ):

        try:

            image = Image.open(
                image_path
            )

            text = (
                pytesseract.image_to_string(
                    image,
                    lang="rus+eng"
                )
            )

            return text

        except Exception as e:

            return (
                f"OCR error: {e}"
            )

    # =====================================
    # SCREEN OCR
    # =====================================

    def read_screen(self):

        path = self.screenshot()

        return self.read_text(path)

    # =====================================
    # ACTIVE WINDOW
    # =====================================

    def active_window(self):

        try:

            window = (
                gw.getActiveWindow()
            )

            if not window:

                return "No active window."

            return {

                "title":
                    window.title,

                "width":
                    window.width,

                "height":
                    window.height,

                "x":
                    window.left,

                "y":
                    window.top
            }

        except Exception as e:

            return (
                f"Window error: {e}"
            )

    # =====================================
    # ANALYZE SCREEN
    # =====================================

    def analyze_screen(self):

        window = (
            self.active_window()
        )

        text = (
            self.read_screen()
        )

        result = {

            "window":
                window,

            "text":
                text[:3000]
        }

        return result

# =========================================
# GLOBAL INSTANCE
# =========================================

vision = Vision()