from concurrent.futures import ProcessPoolExecutor
from app import start_app
from tg_bot import start_polling

if __name__ == "__main__":
    with ProcessPoolExecutor(10) as executor:
        app = executor.submit(start_app)
        bot = executor.submit(start_polling)
        