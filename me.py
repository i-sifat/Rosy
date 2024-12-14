
import logging
import os
from datetime import datetime
from telegram.bot import Bot, MessageHandler, Filters

# Set your Telegram Bot Token here
TOKEN = '6316599602:AAFU8HdpJADz0ogKtvNav7-_yWK3kC_UPrs'

# Initialize the bot
bot = Bot(token=TOKEN)
dispatcher = bot.dispatcher

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define a command handler for when you call the bot "ME"
def start(update: Update, context: CallbackContext):
    greeting = get_greeting()
    update.message.reply_text(greeting)

# Define a message handler for all other messages
def respond(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    message_text = update.message.text
    sender_name = update.message.from_user.first_name

    # Check if the message starts with "Me, mone raikho kintu"
    if message_text == "Me, mone raikho kintu":
        save_message(user_id, sender_name, message_text)
        update.message.reply_text('Message saved.')

    # Check if the message starts with the specific command
    elif message_text.startswith("ME, tomar Friend ke bolo:"):
        friend_name = message_text.split("ME, tomar Friend ke bolo:")[1]
        response = f"{friend_name}, shono, {sender_name} bolche: {message_text}"
        update.message.reply_text(response)
    
    else:
        update.message.reply_text('Bolen')

# Register the command handler
dispatcher.add_handler(CommandHandler('ME', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

def save_message(user_id, sender_name, message_text):
    # Create a directory for each user if it doesn't exist
    user_directory = f"user_messages/{user_id}"
    os.makedirs(user_directory, exist_ok=True)

    # Save the message to a text file named after the sender
    with open(os.path.join(user_directory, f"{sender_name}.txt"), "a") as file:
        file.write(message_text + "\n")

def get_greeting():
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "Good morning shobaike"
    elif 12 <= hour < 17:
        return "Good noon shobaike. Shokale ghumaite besto chilam tai late holo"
    elif 17 <= hour < 22:
        return "Good night shobaike. Late kooro nah ghumaia jaio..."
    else:
        return "It's late! Better go to bed..."

def main():
    # Start the bot
    bot.polling()

if __name__ == '__main__':
    main()
