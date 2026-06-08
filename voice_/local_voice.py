import time
import threading

import pygame
import speech_recognition as sr
from gtts import gTTS
from config import (
    ENABLE_VOICE,
    VOICE_LANGUAGE,
    VOICE_WAKE_WORD,
    DEBUG
)

# =========================================
# LOCAL VOICE
# =========================================

class VoiceController:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.running = False

        pygame.mixer.init()

    # =====================================
    # SPEAK LOCAL
    # =====================================

    def speak(self, text):

        try:

            if DEBUG:

                print(
                    f"\n[VOICE OUT]\n{text}"
                )

            filename = "voice_.mp3"

            tts = gTTS(
                text=text,
                lang=VOICE_LANGUAGE
            )

            tts.save(filename)

            pygame.mixer.music.load(
                filename
            )

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                time.sleep(0.1)

        except Exception as e:

            print(
                "[VOICE ERROR]",
                e
            )

    # =====================================
    # LISTEN LOCAL
    # =====================================

    def listen(self):

        try:

            with sr.Microphone() as source:

                if DEBUG:

                    print(
                        "\n[VOICE] Listening..."
                    )

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            text = self.recognizer.recognize_google(
                audio,
                language="ru-RU"
            )

            if DEBUG:

                print(
                    f"\n[VOICE IN]\n{text}"
                )

            return text

        except sr.UnknownValueError:

            return ""

        except Exception as e:

            print(
                "[VOICE LISTEN ERROR]",
                e
            )

            return ""

    # =====================================
    # WAKE WORD
    # =====================================

    def has_wake_word(
        self,
        text
    ):

        return (
            VOICE_WAKE_WORD
            in text.lower()
        )

    # =====================================
    # CLEAN COMMAND
    # =====================================

    def clean_command(
        self,
        text
    ):

        return (
            text.lower()
            .replace(
                VOICE_WAKE_WORD,
                ""
            )
            .strip()
        )

    # =====================================
    # LOOP
    # =====================================

    def start_loop(
        self,
        agent
    ):

        if self.running:
            return

        self.running = True

        print(
            "[VOICE] Loop started"
        )

        while self.running:

            try:

                text = self.listen()

                if not text:
                    continue

                if not self.has_wake_word(
                    text
                ):
                    continue

                command = self.clean_command(
                    text
                )

                if not command:
                    continue

                response = agent.handle_input(
                    command
                )

                self.speak(
                    response
                )

            except Exception as e:

                print(
                    "[VOICE LOOP ERROR]",
                    e
                )

                time.sleep(1)

    # =====================================
    # THREAD
    # =====================================

    def start_thread(
        self,
        agent
    ):

        if not ENABLE_VOICE:

            print(
                "[VOICE] Disabled"
            )

            return

        threading.Thread(
            target=self.start_loop,
            args=(agent,),
            daemon=True
        ).start()

    # =====================================
    # STOP
    # =====================================

    def stop(self):

        self.running = False


voice = VoiceController()



