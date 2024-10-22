import logging
import asyncio

from telethon import TelegramClient, sync, events

@client.on(events.NewMessage)
async def watcher(client):
    async for message in client.iter_messages('me'):
        print(message.text)
