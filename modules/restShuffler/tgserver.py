import logging
import yaml

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from rest_shuffle import User
from rest_shuffle import get_shuffled_event, add_events_from_file

from pathlib import Path

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    #user = update.effective_user
    print(update.effective_user.id)
    user = User(update.effective_user.id)

    if not user.is_exists:
        print("Unknown user. Adding into DB")
        user.add(update.effective_user.first_name, update.effective_user.id)
        add_events_from_file(Path(__file__).parent / "../../data/restEvents.txt", user.user_id, 'REST_EVENT')
        add_events_from_file(Path(__file__).parent / "../../data/workEvents.txt", user.user_id, 'WORK_EVENT')

    reply_keyboard = [["Rest", "Work"]]

    await update.message.reply_text(
        rf"Hi {user.name}!"
        "Send /cancel to stop talking to me.\n\n"
        "What do you wanna do right now?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Work or Rest?"
        ),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def event_shuffle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    event_type = update.message.text
    if event_type == "Rest":
        type = 'REST_EVENT'
    else:
        type = 'WORK_EVENT'
    print(f"Received event: {event_type}")
    reply_keyboard = [["Rest", "Work"]]
    
    user = User(update.effective_user.id)
    print(f"User id: {user.user_id}")

    await update.message.reply_text(get_shuffled_event(user.user_id, type),
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Work or Rest?"
        ),
    )


def main() -> None:
    """Start the bot."""
    with open(Path(__file__).parent / '../../config/config.yml', 'r') as file:
        text = yaml.safe_load(file)
        print (text)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(text['bot_token']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex("^(Rest|Work)$"), event_shuffle))
 #   application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()