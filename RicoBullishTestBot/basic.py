import os
import shutil

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone


from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.handlers import MessageHandler, DeletedMessagesHandler, EditedMessageHandler


# from utils.media_downloader import _get_media_meta, _can_download, _is_exist, manage_duplicate_file, get_next_name
from utils.load_dotenv import load_dotenv


env_vars = load_dotenv("BullishTechOps.env")
session_string = env_vars['session_string']

app = Client(name='BullishTechOps',
             session_string=session_string,
             )


@app.on_edited_message()
async def log_edit(client, message):
    i = 1
    # client.send_message(message.chat.id, "I'm here")
    # print(message)


@app.on_deleted_messages()
async def log_delete(client, messages):
    i = 1
    # print(messages)


@app.on_message(filters=filters.private)
async def log_direct_message(client, message):
    i = 1

    if message.media:
        print(f"message from {message.chat.username} contains a {message.media.value} file")
        folder_location = os.path.join('telegram_messages', datetime.now().strftime('%Y-%m-%d_%S/'))
        
        blah = await app.download_media(message=message,
                                        file_name=folder_location,
                                        progress=progress)

        i = 1
        
    else:
        i = 1
        
    i = 1
    
@app.on_message(filters=filters.group)
async def group_handler(client, message):
    i = 1
    
    if message.media:
        print(f"message from {message.chat.username} contains a {message.media.value} file")
        folder_location = os.path.join('telegram_messages', datetime.now().strftime('%Y-%m-%d_%S/'))
        
        blah = await app.download_media(
            message=message,
            file_name=folder_location,
            progress=progress
            )
        
        i = 1
    
    else:
        i = 1
    
    i = 1


@app.on_user_status()
async def user_status(client, user):
    i = 1


async def main():
    async with app:
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)
            chat = dialog.chat
            chat_type = chat.type.value
            print(f"chat ID: {chat.id}, chat type: {chat_type}")
            # TODO: Download all media from the chat

    i = 1


def backup_previous_day_folder ():
    base_folder_path = 'telegram_messages'
    backup_folder_path = 'telegram_backup'
    # Get the previous date in GMT
    # For Testing
    previous_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d_%H/')
    # Real
    # previous_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d/')
    source_folder = os.path.join(base_folder_path)
    print (f"source folder: {source_folder}")
    destination_folder = os.path.join(backup_folder_path, previous_date)
    print(f"destination folder: {destination_folder}")
    if os.path.exists(source_folder):
        
        print(f"Backing up {previous_date}")

        shutil.copytree(source_folder, destination_folder)
        print(f"Backup completed for {previous_date}")
        shutil.rmtree(source_folder, ignore_errors=True)
        os.mkdir(source_folder)


def schedule_backup ():
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_previous_day_folder, 'cron', hour='*', minute=1, timezone='UTC')
    scheduler.start()


# async def download_files(client, folder_location, message):
#     media_types = ['audio', 'photo', 'video', 'document', 'voice', 'video_note']
#     file_formats = {
#         'audio': ['all'],
#         'document': ['all'],
#         'video': ['all']
#     }
#
#     for _type in media_types:
#         _media = getattr(message, _type, None)
#         if _media is None:
#             continue
#
#         file_name, file_format = await _get_media_meta(_media, _type, folder_location)
#
#         if _can_download(_type, file_formats, file_format):
#             if os.path.exists(file_name):
#                 file_name = get_next_name(file_name)
#                 download_path = await client.download_media(
#                     message, file_name=file_name
#                 )
#                 # pylint: disable = C0301
#                 download_path = manage_duplicate_file(download_path)
#             if _is_exist(file_name):
#                 file_name = get_next_name(file_name)
#                 download_path = await client.download_media(
#                     message, file_name=file_name
#                 )
#                 # pylint: disable = C0301
#                 download_path = manage_duplicate_file(download_path)  # type: ignore
#             else:
#                 download_path = await client.download_media(
#                     message, file_name=file_name
#                 )
#             if download_path:
#                 print(f"Media downloaded - {download_path}")


async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


if __name__ == '__main__':
    # Start the backup scheduler
    schedule_backup()
    # backup_previous_day_folder()
    
    # Run the main function to fetch messages
    # asyncio.run(main())
    
    app.run()
    
    i = 1
    # app.stop()
    # app.run()
    # app.stop()
