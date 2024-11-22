import os
import time

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import cloudscraper
import telegram

load_dotenv()


interval_str = os.getenv('INTERVAL')
if interval_str is None:
    raise ValueError("interval is invalid")

interval = int(interval_str)
chat_id = os.getenv('CHAT_ID')
message = os.getenv('MESSAGE')
token = os.getenv('TG_BOT')
link = os.getenv("LINK")

scrapper = cloudscraper.create_scraper()
if token is None:
    raise ValueError("token is invalid")

bot = telegram.Bot(token=token)

past_link = None

def main():
    global past_link
    while True:
        try:
            response = scrapper.get(link).text
            parser = BeautifulSoup(response , 'lxml')
            links = parser.find_all('a', class_='newsline article', href=True)
            result = map(lambda x: x['href'], links)
            if past_link is None:
                past_link = set(result)
                continue

            sended_link = set(result)
            new_link = sended_link - past_link
            past_link = sended_link

            for i in new_link:
                message_to_send = f'{message} https://www.hltv.org{i}'
                bot.send_message(chat_id=chat_id, message=message_to_send)
            
        except Exception as e:
            print(e)
        finally:
            time.sleep(interval)


if __name__ == '__main__':
    main()
