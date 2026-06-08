import discord
import wave
import time
import asyncio
import os

from voice_.stt import transcribe_file
from discord.ext import voice_recv
from .discord_queue import voice_queue
from gtts import gTTS

#AGENT
agent_instance = None

def set_agent(agent):
    global agent_instance
    agent_instance = agent

#RECEIVER
class RecordSink(voice_recv.AudioSink):
    def __init__(
        self,
        voice_client,
        voice_runtime
    ):
        super().__init__()

        self.frames = []
        self.started = time.time()

        self._voice_client = voice_client   # переименовано, чтобы не конфликтовать
        self.voice_runtime = voice_runtime
        self.saved = False

        self.last_user_id = None
        self.last_username = None

        self.chunk_duration = 5
        self.processing = False

    def wants_opus(self):
        return False

    def write(self, user, data):

        if data.pcm is None:
            return

        self.last_user_id = str(user.id)
        self.last_username = user.display_name

        self.frames.append(data.pcm)

        if len(self.frames) % 100 == 0:
            print(
                f"[VOICE] packets={len(self.frames)}"
            )

        if (
                time.time() - self.started
                >= self.chunk_duration
                and not self.processing
        ):
            self.processing = True

            chunk = self.frames.copy()

            self.frames.clear()

            self.started = time.time()

            asyncio.run_coroutine_threadsafe(
                self.process_chunk(chunk),
                self.voice_runtime.loop
            )

    def cleanup(self):
        pass

    async def process_chunk(
            self,
            frames
    ):

        try:

            filename = (
                f"chunk_"
                f"{int(time.time())}"
                f".wav"
            )

            with wave.open(
                    filename,
                    "wb"
            ) as wf:

                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(48000)

                wf.writeframes(
                    b"".join(frames)
                )

            text = await asyncio.to_thread(
                transcribe_file,
                filename
            )

            if os.path.exists(
                    filename
            ):
                os.remove(
                    filename
                )

            text = text.strip()

            if not text:
                return

            print(
                f"[VOICE TEXT] {text}"
            )

            response = await asyncio.to_thread(
                agent_instance.handle_input,
                text,
                self.last_user_id,
                self.last_username
            )

            print(
                f"[JARVIS RESPONSE] {response}"
            )

            await voice_runtime.speak(
                response
            )

        except Exception as e:

            print(
                "[VOICE PROCESS ERROR]",
                e
            )

        finally:

            self.processing = False


#VOICE
class DiscordVoice:

    def __init__(self):
        self.loop = None
        self.voice_client = None
        self.current_sink = None
        self.listening_task = None

    # =====================================
    # JOIN
    # =====================================

    async def join(self, message):

        self.loop = asyncio.get_running_loop()

        channel = message.author.voice.channel

        self.voice_client = await channel.connect(
            cls=voice_recv.VoiceRecvClient
        )

        voice_queue.set_voice_client(
            self.voice_client
        )

        self.current_sink = RecordSink(self.voice_client,  self)

        self.voice_client.listen(
            self.current_sink
        )

        print("[VOICE] Recording started")

    async def leave(self, message):
        voice_queue.set_voice_client(None)

        if self.listening_task:
            self.listening_task.cancel()
            self.listening_task = None

        if self.voice_client:
            if self.current_sink:
                self.current_sink.cleanup()
                self.current_sink = None
            await self.voice_client.disconnect()
            self.voice_client = None
            print("[VOICE] Stopped")
            await message.channel.send("Выебан.")

    # =====================================
    # SPEAK
    # =====================================

    async def speak(self, text):

        filename = "tts.mp3"

        tts = gTTS(
            text=text,
            lang="ru"
        )

        tts.save(filename)

        source = discord.FFmpegPCMAudio(
            filename
        )

        self.voice_client.play(source)


voice_runtime = DiscordVoice()

#Debug
class DebugSink(voice_recv.AudioSink):

    def wants_opus(self):
        return False

    def write(self, user, data):
        print(
            "user:",
            user,
            "pcm:",
            len(data.pcm) if data.pcm else None
        )

   #def cleanup(self):
        #pass