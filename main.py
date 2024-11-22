import os
import time
import asyncio

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import cloudscraper
from aiogram import Bot


load_dotenv()

interval_str = os.getenv('INTERVAL')
if interval_str is None:
    raise ValueError("interval is invalid")

interval = int(interval_str)
chat = os.getenv('CHAT')
message = os.getenv('MESSAGE')
token = os.getenv('TOKEN')
link = os.getenv("LINK")

if token is None:
    raise ValueError("token is invalid")

bot = Bot(token=token)
scrapper = cloudscraper.create_scraper()

past_link = None

async def main():
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

            print(new_link)

            for i in new_link:
                message_to_send = f'{message} https://www.hltv.org{i}'
                await bot.send_message(chat_id=chat, text=message_to_send)
            
        except Exception as e:
            print(e)
        finally:
            time.sleep(interval)


if __name__ == '__main__':
    asyncio.run(main())
    
