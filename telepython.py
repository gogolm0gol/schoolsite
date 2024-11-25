import logging
import sqlite3
import telebot

TOKEN = '7750393495:AAF9Jp3-XiKnJfO79l9URK7MRAGwmWuyHAA'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1011100974

logging.basicConfig(level=logging.INFO)


def create_db():
    try:
        conn = sqlite3.connect('messages.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            message TEXT)''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error during DB initialization: {e}")


create_db()


def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text

    logging.info(f"Ви отримали повідомлення: {user_message} від {user_id}")

    try:
        with sqlite3.connect('messages.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            logging.info(f"Saving message from {user_id} to database.")
            cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, user_message))
            conn.commit()

            message_id = cursor.lastrowid
            logging.info(f"Message from {user_id} saved successfully with ID {message_id}.")

            bot.send_message(ADMIN_ID,
                             f"Нове повідомлення від User ID: {user_id}\nID Повідомлення: {message_id}\nТекст повідомлення: {user_message}")

    except sqlite3.Error as e:
        logging.error(f"SQLite error while saving message: {e}")
        bot.send_message(message.chat.id, "Сталася помилка під час обробки вашого повідомлення.")

    bot.send_message(message.chat.id, "Повідомлення відправлено. Чекайте на відповідь🫶🏻")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добрий вечір. Якщо у вас є запитання, ви можете задати його тут❤️")
    logging.info(f"User {message.from_user.id} почав переписку.")


@bot.message_handler(commands=['view_messages'])
def view_messages(message):
    if message.from_user.id == ADMIN_ID:
        try:
            with sqlite3.connect('messages.db', check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM messages')
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        bot.send_message(ADMIN_ID, f"ID повідомлення: {row[0]} | User ID: {row[1]} | Повідомлення: {row[2]}")
                else:
                    bot.send_message(ADMIN_ID, "Повідомлень не знайдено.")
                logging.info("Admin viewed messages.")
        except sqlite3.Error as e:
            logging.error(f"SQLite error while retrieving messages: {e}")
            bot.send_message(ADMIN_ID, "Сталася помилка під час отримання повідомлень.")
    else:
        bot.send_message(message.chat.id, "Ви не маєте доступу до цієї функції❌")


@bot.message_handler(commands=['reply'])
def reply_to_message(message):
    if message.from_user.id == ADMIN_ID:
        parts = message.text.split(' ', 2)
        if len(parts) > 2:
            msg_id = parts[1]
            reply_text = parts[2]

            try:
                with sqlite3.connect('messages.db', check_same_thread=False) as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM messages WHERE id = ?', (msg_id,))
                    msg = cursor.fetchone()

                    if msg:
                        user_id = msg[1]
                        bot.send_message(user_id, f"{reply_text}")
                        bot.send_message(ADMIN_ID, f"Відповідь на ID {msg_id}: {reply_text}")
                    else:
                        bot.send_message(ADMIN_ID, "Повідомлення не знайдено.")
                    logging.info(f"Відповідь на ID {msg_id}.")
            except sqlite3.Error as e:
                logging.error(f"SQLite error while replying to message: {e}")
                bot.send_message(ADMIN_ID, "Сталася помилка під час відповіді.")
        else:
            bot.send_message(ADMIN_ID, "Використання: /reply <message_id> <ваша відповідь>")
    else:
        bot.send_message(message.chat.id, "Ви не маєте доступу до цієї функції❌")


@bot.message_handler(func=lambda message: True)
def user_message(message):
    handle_message(message)


def start_telegram_bot():
    logging.info("Bot is starting...")
    bot.polling(none_stop=True)
