import sys
import signal
import asyncio
import threading

from dotenv import load_dotenv

from discord_.discord_voice import set_agent


from agent import Agent

from telegram_bot import (
    start_telegram_bot
)

from discord_.discord_bot import (
    start_discord_bot
)

from config import (
    ENABLE_TELEGRAM,
    ENABLE_DISCORD,
    ENABLE_AUTONOMOUS
)

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# ======================================!===
# GLOBALS
# =========================================

running = True


# =========================================
# SIGNAL HANDLER
# =========================================

def shutdown_handler(
        sig,
        frame
):
    global running

    print("\n[SHUTDOWN] stopping...")

    running = False

    sys.exit(0)


# =========================================
# REGISTER SIGNALS
# =========================================

signal.signal(
    signal.SIGINT,
    shutdown_handler
)

signal.signal(
    signal.SIGTERM,
    shutdown_handler
)


# =========================================
# AUTONOMOUS LOOP
# =========================================

def autonomous_loop(agent):
    print("[AUTO] loop started")

    while running:

        try:

            agent.tick()

        except Exception as e:

            print(
                "[AUTO ERROR]",
                e
            )

        asyncio.run(
            asyncio.sleep(2)
        )


# =========================================
# START TELEGRAM
# =========================================

def start_telegram(agent):
    try:

        start_telegram_bot(agent)

    except Exception as e:

        print(
            "[TELEGRAM ERROR]",
            e
        )


# =========================================
# START DISCORD
# =========================================

def start_discord(agent):
    try:

        start_discord_bot(agent)

    except Exception as e:

        print(
            "[DISCORD ERROR]",
            e
        )


# =========================================
# MAIN
# =========================================

def main():

    global running

    print("=" * 50)
    print("JARVIS RUNTIME STARTING")
    print("=" * 50)

    # =====================================
    # CREATE AGENT
    # =====================================

    agent = Agent()
    set_agent(agent)
    print("[OK] Agent initialized")

    # =====================================
    # AUTONOMOUS THREAD
    # =====================================

    if ENABLE_AUTONOMOUS:
        threading.Thread(
            target=autonomous_loop,
            args=(agent,),
            daemon=True
        ).start()

        print("[OK] Autonomous loop")

    # =====================================
    # TELEGRAM THREAD
    # =====================================

    if ENABLE_TELEGRAM:
        threading.Thread(
            target=start_telegram,
            args=(agent,),
            daemon=True
        ).start()

        print("[OK] Telegram")

    # =====================================
    # DISCORD THREAD
    # =====================================

    if ENABLE_DISCORD:
        threading.Thread(
            target=start_discord,
            args=(agent,),
            daemon=True
        ).start()

        print("[OK] Discord")

    # =====================================
    # CONSOLE LOOP
    # =====================================


    print("[OK] Voice")

    print("\n[READY]\n")

    while running:

        try:

            user_input = input(">>> ")

            if not user_input:
                continue

            if user_input.lower() == "exit":
                shutdown_handler(
                    None,
                    None
                )

            result = agent.handle_input(
                user_input
            )

            print(
                f"\n[JARVIS]\n{result}\n"
            )

        except KeyboardInterrupt:

            shutdown_handler(
                None,
                None
            )

        except Exception as e:

            print(
                "[MAIN ERROR]",
                e
            )


# =========================================
# ENTRYPOINT
# =========================================

if __name__ == "__main__":
    main()