# Importing Required Libraries, Imported os Module For Security 
import os
import telebot

# Getting Bot Token From Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Creating Telebot Object
bot = telebot.TeleBot('')

# Whenever Starting Bot
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
  # Inline Button
  markup = telebot.types.InlineKeyboardMarkup()
  markup.add(telebot.types.InlineKeyboardButton("VardanBot", url="https://t.me/VardanBot"))

  # Reply Keyboard Button
  # markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
  # markup.add(telebot.types.KeyboardButton("Reply Keyboard Button"))
  
  markdown = f"""Hey *{message.chat.first_name}* Welcome To *Vardan Bot*."""
  
  bot.reply_to(message, markdown, parse_mode="Markdown", reply_markup=markup)
  print(f"Welcome Message Sent To {message.chat.first_name} for {message}\n")

# Handle Documents
@bot.message_handler(func=lambda m: True, content_types=['document','photo'])
def handle_docs_photo(message):
  if message.document:
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Save the file or process it as needed
    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "File received!")

  elif message.photo:
    # Get the highest resolution photo
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info)
    # Save the file or process it as needed
    with open(file_info.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Photo received!")
  
  else:
    bot.reply_to(message, "Unsupported file format.") 
  #bot.reply_to(message, f"Sorry {message.chat.first_name}, Documents Not Supported At This Time")
  #print(f"Message Replied To {message.chat.first_name}\n")

# Reply To All Messages
#@bot.message_handler(func=lambda msg: True)
#def all(message):
#  bot.reply_to(message, f"Sorry {message.chat.first_name}, This Bot Is In Development Mode")
#  print(f"Message Replied To {message.chat.first_name} with message {message}\n")

@bot.message_handler()
def all(msg):
  bot.reply_to(msg, f"Sorry {msg.chat.first_name}, This Bot Is In Development Mode")
  print(f"Message Replied To {msg.chat.first_name} with message {msg}\n")


print("Bot Started And Waiting For New Messages\n")
  
# Waiting For New Messages
bot.infinity_polling()
