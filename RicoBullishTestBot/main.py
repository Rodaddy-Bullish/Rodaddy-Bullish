import os
import shutil

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone

from pyrogram import Client, idle
from pyrogram.types import Message, Chat, User
from pyrogram import filters


from utils.load_dotenv import load_dotenv
from utils.google_cloud_helpers import access_secret
from utils.helpers import (schedule_backup,
                           progress,
                           get_current_date_as_str,
                           write_message_to_file,
                           get_chat_folder,
                           format_message,
                           get_full_user_info,
                           )

env_vars = load_dotenv("BullishTechOps.env")
session_string = env_vars['session_string']

app = Client(name='BullishTechOps', session_string=env_vars['session_string'])


@app.on_message(filters=filters.group)
async def group_message_log (client: Client, message: Message):
    chat_name = message.chat.title
    from_user = message.from_user.username
    message_id = message.id
    
    formatted_message = await format_message(client, message, message_type='new')
    
    write_message_to_file(f"Date: {message.date} MsgId: {message_id} - {from_user}: {message.text}\n", chat_name)
    
    if message.media:
        if message.web_page:
            link = message.web_page.url
            print(f'message from {from_user} contains the link "{link}" ')
        elif message.media:
            pass
        elif message.sticker:
            i = 1
        
        print(f"message from {from_user} contains a {message.media.value} file")
        files_folder_location = os.path.join(get_chat_folder(chat_name), 'files/')
        
        downloaded_file = await app.download_media(
            message=message,
            file_name=files_folder_location,
            progress=progress,
        )
        
        write_message_to_file(f"{message.date} - {from_user}: added file {downloaded_file}\n", chat_name)
    
    # print(f"original message: {message}")
    i = 1


@app.on_edited_message(filters=filters.group)
async def group_message_edit (client, message):
    chat_name = message.chat.title
    from_user = message.from_user.username
    original_time_of_message = message.date.strftime('%Y-%m-%d %H:%M:%S')
    time_of_edit = message.edit_date.strftime('%Y-%m-%d %H:%M:%S')
    message_id = message.id
    if message.reaction:
        print(f"message from {from_user} contains a reaction)")
    # print(f"updated message: {message}")
    
    msg = f"Date: {time_of_edit} - \nmessage {message_id} was changed by {from_user} text changed to {message.text}\n"
    write_message_to_file(msg, chat_name)


@app.on_deleted_messages(filters=filters.group)
async def group_message_delete (client, message):
    chat_name = message.chat.title
    from_user = message.from_user.username
    
    msg = f"{message.date} - {from_user} deleted {message.text}\n"
    
    write_message_to_file(msg, chat_name)


@app.on_message(filters=filters.private)
async def direct_message_log (client, message):
    chat_name = message.chat.username
    from_user = message.from_user.username
    message_id = message.id
    write_message_to_file(f"Date: {message.date} MsgId: {message_id} - {from_user}: {message.text}\n", chat_name)
    
    if message.media:
        if message.web_page:
            link = message.web_page.url
            print(f'message from {from_user} contains the link "{link}" ')
        elif message.media:
            pass
        elif message.sticker:
            i = 1
        
        print(f"message from {from_user} contains a {message.media.value} file")
        files_folder_location = os.path.join(get_chat_folder(chat_name), 'files/')
        
        downloaded_file = await app.download_media(
            message=message,
            file_name=files_folder_location,
            progress=progress,
        )
        
        write_message_to_file(f"{message.date} - {from_user}: added file {downloaded_file}\n", chat_name)
    
    # print(f"original message: {message}")
    i = 1


@app.on_edited_message(filters=filters.private)
async def direct_message_edit (client, message):
    chat_name = message.chat.title
    from_user = message.from_user.username
    
    i = 1
    
    msg = f"{message.date} - {from_user} edited {message.text}\n"
    write_message_to_file(msg, chat_name)


@app.on_deleted_messages(filters=filters.private)
async def direct_message_delete (client, message):
    chat_name = message.chat.title
    from_user = message.from_user.username
    timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
    
    i = 1
    
    msg = f"{message.date} - {from_user} deleted {message.text}\n"
    
    write_message_to_file(msg, chat_name)


@app.on_user_status()
async def user_status (client, user):
    i = 1


async def main ():
    async with app:
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)
            chat = dialog.chat
            chat_type = chat.type.value
            print(f"chat ID: {chat.id}, chat type: {chat_type}")
            # TODO: Download all media from the chat
    
    i = 1


if __name__ == '__main__':
    # Start the backup scheduler
    # schedule_backup(hours='*', minutes='54')
    # backup_previous_day_folder()
    
    # Run the main function to fetch messages
    # asyncio.run(main())
    
    app.run()
    
    i = 1
