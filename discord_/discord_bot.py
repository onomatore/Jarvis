import discord
from config import DISCORD_BOT_TOKEN, DEBUG
from .discord_voice import voice_runtime

# =========================================
# INTENTS
# =========================================
intents = discord.Intents.default()
intents.message_content = True
from voice_.local_voice import voice
# =========================================
# CLIENT
# =========================================
class JarvisDiscordClient(discord.Client):
    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = agent

    async def on_ready(self):
        print(f"[DISCORD] Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not message.content:
            return

        user_text = message.content

        if DEBUG:
            print(f"\n[DISCORD USER]\n{user_text}")

        # Голосовые команды
        if user_text == "!join":
            await voice_runtime.join(message)
            return

        if user_text == "!leave":
            await voice_runtime.leave(message)
            return

        if user_text == "!testvoice":
            await voice_runtime.speak("Привет. Проверка голосового канала.")
            await message.channel.send("Голос отправлен.")
            return

        # Обработка сообщений
        try:
            async with message.channel.typing():
                if user_text.startswith("!memory"):
                    context = self.agent.memory.build_context() or "Memory empty."
                    await message.channel.send(context[:1900])
                    return

                if user_text.startswith("!clear"):
                    self.agent.memory.clear()
                    await message.channel.send("Memory cleared.")
                    return

                if user_text.startswith("!tasks"):
                    count = self.agent.task_count()
                    await message.channel.send(f"Tasks: {count}")
                    return

                if user_text.startswith("!task "):
                    self.agent.add_task(user_text[6:])
                    await message.channel.send(f"Task added:\n{user_text[6:]}")
                    return

                # Обработка агентом
                response = self.agent.handle_input(
                    user_input=user_text,
                    user_id=str(message.author.id),
                    username=message.author.name
                )

                if len(response) > 1900:
                    response = response[:1900]

                await message.channel.send(response)

                # Озвучка (если бот в канале)
                if voice_runtime.voice_client:
                    await voice_runtime.speak(response)

        except Exception as e:
            error_text = f"Discord error:\n{e}"
            print(error_text)
            await message.channel.send(error_text[:1900])

# =========================================
# START BOT
# =========================================
def start_discord_bot(agent):
    if not DISCORD_BOT_TOKEN:
        raise Exception("DISCORD_BOT_TOKEN missing")

    voice.start_thread(agent)

    client = JarvisDiscordClient(agent=agent, intents=intents)
    print("[DISCORD] Starting...")
    client.run(DISCORD_BOT_TOKEN)