from __future__ import annotations

import os
import json
import shutil
import pickle

from datetime import datetime, timedelta, timezone
from typing import TypeVar, Optional, Any
from collections import OrderedDict
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram import Client
from pyrogram.raw.types import InputUser, InputUserFromMessage
from pyrogram.types import Message, Chat, User
from pyrogram.raw.functions.help import GetUserInfo
from telethon.tl.functions.users import GetFullUserRequest
from pyrogram.raw.functions.users import GetFullUser


def full_backup ():
    ...


def check_missing ():
    ...


async def progress (current, total):
    print(f"{current * 100 / total:.1f}%")


def update_known_groups (client, chat, known_groups):
    chat_id = chat.id
    if chat_id not in known_groups:
        i = 1
        
        known_groups[chat_id] = {
            'title': chat.title,
            # 'username': chat.username
        }
    
    return known_groups


def update_known_chats (client, chat, known_chats):
    chat_id = chat.id
    if chat_id not in known_chats:
        i = 1
        
        known_chats[chat_id] = {
            'title': chat.title,
            'username': chat.username
        }
    
    return known_chats


async def get_full_user_info (client: Client, user: User) -> Any:
    i = 1
    user_id = user.id
    user_info = await client.get_users(user_id)
    
    i = 1
    return user_info


async def deserialize_message (client: Client, message: Message) -> OrderedDict:
    
    message_dict = OrderedDict()
    message_dict['id'] = message.id
    message_dict['date'] = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else None
    message_dict['text'] = message.text
    from_user_info = message.from_user
    reply_to_info = message.reply_to_message
    chat_info = message.chat

    # from_user_info = await get_full_user_info(client, message.from_user)
    if from_user_info:
        # TODO: check for sender type, if not user then get the chat info
        message_dict['from_user_info'] = from_user_info
        message_dict['from_id'] = from_user_info.id
        message_dict['from_username'] = from_user_info.username
    else:
        message_dict['from_user_info'] = None
        message_dict['from_id'] = ''
        message_dict['from_username'] = ''
        
    if reply_to_info:
        message_dict['reply_to_info'] = reply_to_info
        message_dict['reply_to_id'] = reply_to_info.id
        message_dict['reply_to_username'] = reply_to_info.from_user.username
        # TODO: add From user and user_id to the message_dict Or channel if so
    else:
        message_dict['reply_to_info'] = None
        message_dict['reply_to_id'] = None
        message_dict['reply_to_username'] = ''
    
    if chat_info:
        message_dict['chat_info'] = chat_info
        message_dict['chat_id'] = chat_info.id
        message_dict['chat_title'] = chat_info.title
    else:
        message_dict['chat_info'] = None
        message_dict['chat_id'] = ''
        message_dict['chat_title'] = ''
    
    message_dict['media'] = str(message.media) if message.media else None
    
    w = 1
    
    return message_dict


async def format_message (client: Client, message: Message, message_type: str = 'new') -> str:
    
    message_dict = await deserialize_message(client, message)
    test = _format_message(message_dict, message_type)
    if test:
        return test
    
    if message_dict['from_user_info']:
        sender_username = message_dict['from_user_info'].username
        sender_id = message_dict['from_user_info'].id
    else:
        sender_username = 'Unknown'
        sender_id = message_dict['from_user_info'].id if message_dict['from_user_info'] else 'Unknown'
    
    if message_dict['reply_to_info']:
        to_username = message_dict['reply_to_info'].username
        to_id = message_dict['reply_to_info'].id
    else:
        to_username = 'Unknown'
        to_id = message_dict['reply_to_info'].id if message_dict['reply_to_info'] else None
    
    if message_dict['reply_to_info']:
        reply_to = f" (reply to {message_dict['reply_to_info']['id']})"
    else:
        reply_to = ''
        
    if message_type == 'new':
        ...
    elif message_type == 'edited':
        ...
    elif message_type == 'deleted':
        ...
    else:
        ...

    out = f"[{message_dict['timestamp']}] {sender_username}: {message_dict['text']} {reply_to}\n"
    i = 1
    
    return out


def _format_message (message_dict, message_type: str = 'new') -> str:
    if message_dict['from_user_info']:
        sender_username = message_dict['from_user_info'].username
        sender_id = message_dict['from_user_info'].id
    else:
        sender_username = 'Unknown'
        sender_id = message_dict['from_user_info'].id if message_dict['from_user_info'] else 'Unknown'
    
    if message_dict['reply_to_info']:
        to_username = message_dict['reply_to_info'].username
        to_id = message_dict['reply_to_info'].id
    else:
        to_username = 'Unknown'
        to_id = message_dict['reply_to_info'].id if message_dict['reply_to_info'] else None
    
    if message_dict['reply_to_info']:
        reply_to = f" (reply to {message_dict['reply_to_info']['id']})"
    else:
        reply_to = ''
    
    if message_type == 'new':
        ...
    elif message_type == 'edited':
        ...
    elif message_type == 'deleted':
        ...
    else:
        ...
    
    out = f"[{message_dict['date']}] {sender_username}: {message_dict['text']} {reply_to}\n"
    i = 1
    
    return out


def format_edited_message (client: Client, message: Message):
    message_dict = deserialize_message(message)
    timestamp = message.date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    sender = message_dict['from_id']
    content = message.message or 'Media'
    
    reply_to = f" (reply to {message.reply_to.reply_to_msg_id})" if message.reply_to else ''
    
    out = f"[{timestamp}] {sender}: {content}{reply_to}\n"
    i = 1
    
    return out


def format_deleted_message (client: Client, message: Message):
    message_dict = deserialize_message(message)
    timestamp = message.date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    sender = message_dict['from_id']
    content = message.message or 'Media'
    
    reply_to = f" (reply to {message.reply_to.reply_to_msg_id})" if message.reply_to else ''
    
    out = f"[{timestamp}] {sender}: {content}{reply_to}\n"
    i = 1
    
    return out


def load_pickle_file (file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}


def save_pickle_file (data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def get_current_date_as_str ():
    return datetime.now().strftime('%Y-%m-%d')


def get_current_time_as_str ():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_chat_folder (chat_name: str):
    base_folder = 'telegram_messages'
    chat_folder = os.path.join(base_folder, chat_name)
    if not os.path.exists(chat_folder):
        os.makedirs(chat_folder)
    return chat_folder


def get_chat_file (chat_name: str):
    chat_folder = get_chat_folder(chat_name)
    chat_file = os.path.join(chat_folder, f'{chat_name}_{get_current_date_as_str()}_chat.txt')
    
    return chat_file


def write_message_to_file (msg: str, chat_name: str):
    chat_file = get_chat_file(chat_name)
    print(msg)
    with open(chat_file, 'a') as f:
        f.write(msg)


def schedule_backup (hours=0, minutes=1, time_zone='UTC'):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        backup_previous_day_folder,
        trigger='cron',
        hour=hours,
        minute=minutes,
        timezone=time_zone
        )
    
    scheduler.start()


def create_archives (base_folder_path='../telegram_messages', backup_folder_path='../telegram_backup'):
    for folder in os.listdir(base_folder_path):
        source_folder = os.path.join(base_folder_path, folder)
        destination_folder = os.path.join(backup_folder_path, folder)
        if os.path.exists(source_folder):
            shutil.copytree(source_folder, destination_folder)
            print(f"Backup completed for {folder}")
            shutil.rmtree(source_folder, ignore_errors=True)
            os.mkdir(source_folder)
        else:
            i = 1


def backup_previous_day_folder (base_folder_path='../telegram_messages', backup_folder_path='../telegram_backup'):
    # Get the previous date in GMT
    previous_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')
    backup_to_folder = os.path.join(backup_folder_path, previous_date)
    archive_file = os.path.join(backup_folder_path, f'{previous_date}_archive')
    
    print(f"source folder: {base_folder_path}")
    print(f"base backup folder: {backup_folder_path}")
    print(f"destination folder: {backup_to_folder}")
    
    try:
        blah = shutil.make_archive(
            archive_file,
            format='tar',
            root_dir=base_folder_path,
            base_dir=previous_date
            )
    except FileNotFoundError:
        i = 1
    
    try:
        blah = shutil.move(base_folder_path, backup_to_folder, copy_function=shutil.copytree)
    except FileExistsError:
        i = 1
    except FileNotFoundError:
        i = 1
    
    if os.path.exists(base_folder_path):
        shutil.copytree(base_folder_path, backup_to_folder, dirs_exist_ok=True)
        print(f"Backup completed copied {backup_to_folder} to {backup_to_folder}")
    else:
        i = 1


def main ():
    backup_previous_day_folder()


if __name__ == '__main__':
    main()
