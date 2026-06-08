from telegram import Update

from telegram.ext import (

    ApplicationBuilder,

    ContextTypes,

    MessageHandler,

    CommandHandler,

    filters
)

from config import (

    TELEGRAM_BOT_TOKEN,

    DEBUG
)

# =========================================
# START COMMAND
# =========================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (

        "Jarvis online.\n\n"

        "Commands:\n"
        "/help\n"
        "/memory\n"
        "/tasks\n"
        "/clear"
    )

    await update.message.reply_text(
        text
    )

# =========================================
# HELP COMMAND
# =========================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (

        "Jarvis AI Agent\n\n"

        "Just send message.\n"

        "Examples:\n"
        "- open youtube\n"
        "- take screenshot\n"
        "- write hello world to file\n"
    )

    await update.message.reply_text(
        text
    )

# =========================================
# MEMORY COMMAND
# =========================================

async def memory_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    agent = context.bot_data["agent"]

    memory_context = (
        agent.memory.build_context()
    )

    if not memory_context:

        memory_context = "Memory empty."

    await update.message.reply_text(
        memory_context[:4000]
    )

# =========================================
# TASKS COMMAND
# =========================================

async def tasks_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    agent = context.bot_data["agent"]

    count = agent.task_count()

    await update.message.reply_text(

        f"Tasks in queue: {count}"
    )

# =========================================
# CLEAR MEMORY
# =========================================

async def clear_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    agent = context.bot_data["agent"]

    agent.memory.clear()

    await update.message.reply_text(
        "Memory cleared."
    )

# =========================================
# MAIN MESSAGE HANDLER
# =========================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    agent = context.bot_data["agent"]

    user_text = update.message.text

    if DEBUG:

        print(
            f"\n[TELEGRAM USER]\n"
            f"{user_text}"
        )

    try:

        # TYPING STATUS

        await context.bot.send_chat_action(

            chat_id=update.effective_chat.id,

            action="typing"
        )

        # AGENT RESPONSE

        response = agent.handle_input(
            user_text
        )

        # LIMIT TELEGRAM LENGTH

        if len(response) > 4000:

            response = response[:4000]

        await update.message.reply_text(
            response
        )

    except Exception as e:

        error_text = (
            f"Telegram error:\n{e}"
        )

        print(error_text)

        await update.message.reply_text(
            error_text
        )

# =========================================
# START BOT
# =========================================

def start_telegram_bot(agent):

    if not TELEGRAM_BOT_TOKEN:

        raise Exception(
            "TELEGRAM_BOT_TOKEN missing"
        )

    # CREATE APPLICATION

    app = (

        ApplicationBuilder()

        .token(
            TELEGRAM_BOT_TOKEN
        )

        .build()
    )

    # STORE AGENT

    app.bot_data["agent"] = agent

    # =====================================
    # COMMANDS
    # =====================================

    app.add_handler(

        CommandHandler(
            "start",
            start_command
        )
    )

    app.add_handler(

        CommandHandler(
            "help",
            help_command
        )
    )

    app.add_handler(

        CommandHandler(
            "memory",
            memory_command
        )
    )

    app.add_handler(

        CommandHandler(
            "tasks",
            tasks_command
        )
    )

    app.add_handler(

        CommandHandler(
            "clear",
            clear_command
        )
    )

    # =====================================
    # TEXT HANDLER
    # =====================================

    app.add_handler(

        MessageHandler(
            filters.TEXT
            &
            ~filters.COMMAND,

            message_handler
        )
    )

    print(
        "[TELEGRAM] Bot started"
    )

    # =====================================
    # RUN
    # =====================================

    app.run_polling(
        drop_pending_updates=True
    )