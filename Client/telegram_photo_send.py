import asyncio
import os
from time import sleep
from telebot.async_telebot import AsyncTeleBot
import aiohttp
import datetime
import cv2
import numpy as np
import time
import inspect
import socket
from dotenv import load_dotenv

load_dotenv()

bot = AsyncTeleBot(os.getenv("TOKEN"))
chatId1, chatId2 = os.getenv("ID1"), os.getenv("ID2")

async def start_message():
    time = datetime.datetime.now()
    await bot.send_message(chat_id=chatId1, text=f'''
Пк запущен: {time}, 
Имя пк: {socket.gethostname()}
''')
    await bot.send_message(chat_id=chatId2, text=f'''
Пк запущен: {time}, 
Имя пк: {socket.gethostname()}
''')

@bot.message_handler(commands=['photo'])
async def photo(message):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('cam.png', frame)
    cap.release()

    with open('cam.png', 'rb') as photo_file:
        await bot.send_photo(chat_id=chatId1, photo=photo_file)
    with open('cam.png', 'rb') as photo_file:
        await bot.send_photo(chat_id=chatId2, photo=photo_file)


@bot.message_handler(commands=['video'])
async def video(message):
    def get_duration(text):
        try:
            return int(text.split()[1])
        except (IndexError, ValueError):
            return None
    duration = get_duration(message.text)
    if duration is not None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await bot.send_message(message.chat.id, "Failed to open webcam.")
            return
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
        start_time = time.time()
        while int(time.time() - start_time) < duration:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 0)
                out.write(frame)
                cv2.imshow('frame', frame)
                await asyncio.sleep(0.1)
            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        video_out = open('output.mp4', 'rb')
        await bot.send_video(chat_id=chatId2, video=video_out)
    else:
        await bot.send_message(message.chat.id, "Invalid arguments.")


async def main():
    await start_message()
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())
