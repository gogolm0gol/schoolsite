import threading
from telepython import start_telegram_bot
from my_site import app

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot).start()

    app.run(debug=True, use_reloader=False)