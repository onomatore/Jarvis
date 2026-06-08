import time
import threading
import queue
import uuid
import discord_
import os

from gtts import gTTS

# =========================================
# DISCORD TTS QUEUE
# =========================================

class VoiceQueue:

    def __init__(self):

        self.voice_client = None

        self.queue = queue.Queue()

        self.running = True

        self.worker = threading.Thread(
            target=self.worker_loop,
            daemon=True
        )

        self.worker.start()

    # =====================================
    # SET CLIENT
    # =====================================

    def set_voice_client(
        self,
        voice_client
    ):

        self.voice_client = voice_client

    # =====================================
    # ADD TEXT
    # =====================================

    def add(self, text):

        print("[QUEUE] add:", text)

        if text:
            self.queue.put(text)

    # =====================================
    # WORKER
    # =====================================

    def worker_loop(self):

        while self.running:

            try:

                text = self.queue.get()

                print("[QUEUE] got:", text)

                self.play_text(text)

            except Exception as e:

                print("[VOICE QUEUE ERROR]", e)

    # =====================================
    # PLAY
    # =====================================

    def play_text(
        self,
        text
    ):
        print(
            "[TTS START]",
            text
        )
        if not self.voice_client:

            print(
                "[VOICE] No voice_ client"
            )

            return

        filename = (
            f"tts_"
            f"{uuid.uuid4().hex}"
            f".mp3"
        )

        try:

            print(
                "[TTS] Generating..."
            )

            tts = gTTS(
                text=text,
                lang="ru"
            )

            tts.save(
                filename
            )

            print(
                "[TTS] Generated:",
                filename
            )

            while self.voice_client.is_playing():

                time.sleep(0.5)

            source = discord_.FFmpegPCMAudio(
                filename
            )

            def cleanup(error):

                try:

                    if os.path.exists(
                        filename
                    ):

                        os.remove(
                            filename
                        )

                except Exception:

                    pass

            print(
                "[TTS] Playing..."
            )

            self.voice_client.play(
                source,
                #after=cleanup
            )

            while self.voice_client.is_playing():

                time.sleep(0.5)

            print(
                "[TTS] Done"
            )

        except Exception as e:

            print(
                "[VOICE PLAY ERROR]",
                e
            )

    # =====================================
    # STOP
    # =====================================

    def stop(self):

        self.running = False


voice_queue = VoiceQueue()