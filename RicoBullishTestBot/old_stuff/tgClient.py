import os
import json
import shutil
import pickle
import asyncio
from datetime import datetime, timedelta, timezone
from collections import OrderedDict

from tqdm import tqdm
import telethon
from PIL import Image
from telethon import TelegramClient, errors, sync
import telethon.tl.types
from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from apscheduler.schedulers.background import BackgroundScheduler
from telethon.tl.types import DocumentAttributeFilename, InputFileLocation

from load_dotenv import load_dotenv

dot_file = "BullishTechOps.env"
env_vars = load_dotenv(".env2")


# BACKUP_TRACKER_FILE = 'backup_tracker.json'


async def tlg_connect (api_id=None, api_hash=None, phone_number=None, session_string=None):
    """Connect and Log-in/Sign-in to Telegram API. Request Sign-in code for first execution"""
    
    if session_string:
        client = TelegramClient(StringSession(session_string), api_id, api_hash)
    else:
        env_vars = load_dotenv(dot_file)
        print('No session string provided. Trying to load from environment variables...')
        
        if 'session_string' in env_vars.keys():
            session_string = env_vars['session_string']
            client = TelegramClient(StringSession(session_string), api_id, api_hash)
        else:
            print('No environment variables found. Trying to load from function arguments...')
            api_id = env_vars["app_id"]
            api_hash = env_vars['app_hash']
            phone_number = env_vars['phone_number']
            client = TelegramClient("Bullish_TG_Archiver", api_id, api_hash)
    
    print('Trying to connect to Telegram...')
    
    # client = TelegramClient(StringSession(session_string), api_id, api_hash)
    # client = TelegramClient("Bullish_TG_Archiver", api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        print('Session file not found. This is the first run, sending code request...')
        await client.send_code_request(phone_number)
        self_user = None
        while self_user is None:
            code = input('Enter the code you just received: ')
            try:
                self_user = await client.sign_in(phone_number, code)
            except errors.UnauthorizedError as e:
                print("Telegram client needs code from app. That didn't work, so I'm quitting now.")
                print(e)
                import sys
                sys.exit(10)
    print('Sign in success.')
    # string = StringSession.save(client.session)
    # print(string)
    return client


def load_pickle_file (file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}


def save_pickle_file (data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def load_backup_tracker (backup_tracker_file):
    # backup_tracker_file = env_vars['backup_tracker_file']
    return load_pickle_file(backup_tracker_file)


async def a_update_known_entities (client, messages, known_users, known_chats, known_groups):
    for message in messages:
        
        fid = None
        sid = None
        tid = None
        
        try:
            sender_id = message.sender_id
        except AttributeError:
            sender_id = None
            sid = "no sender_id"
        try:
            from_id = message.from_id
        except AttributeError:
            from_id = None
            fid = "no from_id"
        try:
            to_id = message.to_id
        except AttributeError:
            to_id = None
            tid = "no to_id"
        
        if fid or sid or tid:
            i = 1
        
        if from_id:
            user_id = message.from_id.user_id
            if user_id not in known_users:
                user_info = await getUserInfo(client=client, stuff=user_id)
                try:
                    try:
                        first_name = user_info.first_name
                    except AttributeError:
                        first_name = "no first_name"
                    
                    try:
                        last_name = user_info.last_name
                    except AttributeError:
                        last_name = "no last_name"
                    
                    try:
                        username = user_info.username
                    except AttributeError:
                        username = "no username"
                    
                    known_users[user_id] = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username
                    }
                    i = 1
                except AttributeError:
                    i = 1
        
        if to_id:
            try:
                chat_id = message.to_id.channel_id if message.to_id.channel_id else message.to_id.chat_id
                if chat_id:
                    chat = client.get_entity(chat_id)
                    if chat.megagroup or chat.gigagroup:
                        known_groups[chat_id] = {
                            'title': chat.title,
                            'username': chat.username
                        }
                    else:
                        known_chats[chat_id] = {
                            'title': chat.title,
                            'username': chat.username
                        }
            except AttributeError:
                i = 1
        
        if sender_id:
            id = message.sender_id
            try:
                user_id = message.sender_id.user_id
            except AttributeError:
                user_id = id
            if id not in known_users:
                user_info = await getUserInfo(client=client, stuff=user_id)
                # user = await client.get_entity(user_id)
                try:
                    try:
                        first_name = user_info.first_name
                    except AttributeError:
                        first_name = "no first_name"
                    
                    try:
                        last_name = user_info.last_name
                    except AttributeError:
                        last_name = "no last_name"
                    
                    try:
                        username = user_info.username
                    except AttributeError:
                        username = "no username"
                    
                    known_users[user_id] = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username
                    }
                    i = 1
                except AttributeError:
                    i = 1
    return known_users, known_chats, known_groups


async def update_known_entities (client, message, known_users, known_chats, known_groups):
    fid = None
    sid = None
    tid = None
    
    try:
        sender_id = message.sender_id
    except AttributeError:
        sender_id = None
        sid = "no sender_id"
    try:
        from_id = message.from_id
    except AttributeError:
        from_id = None
        fid = "no from_id"
    try:
        to_id = message.to_id
    except AttributeError:
        to_id = None
        tid = "no to_id"
    
    if fid or sid or tid:
        i = 1
    
    if from_id:
        user_id = message.from_id.user_id
        if user_id not in known_users:
            user_info = getUserInfo(client=client, stuff=user_id)
            try:
                try:
                    first_name = user_info.first_name
                except AttributeError:
                    first_name = "no first_name"
                
                try:
                    last_name = user_info.last_name
                except AttributeError:
                    last_name = "no last_name"
                
                try:
                    username = user_info.username
                except AttributeError:
                    username = "no username"
                
                known_users[user_id] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                }
                i = 1
            except AttributeError:
                i = 1
    
    if to_id:
        try:
            chat_id = message.to_id.channel_id if message.to_id.channel_id else message.to_id.chat_id
            if chat_id:
                chat = client.get_entity(chat_id)
                if chat.megagroup or chat.gigagroup:
                    known_groups[chat_id] = {
                        'title': chat.title,
                        'username': chat.username
                    }
                else:
                    known_chats[chat_id] = {
                        'title': chat.title,
                        'username': chat.username
                    }
        except AttributeError:
            i = 1
    
    if sender_id:
        id = message.sender_id
        try:
            user_id = message.sender_id.user_id
        except AttributeError:
            user_id = id
        if id not in known_users:
            user_info = getUserInfo(client=client, stuff=user_id)
            # user = await client.get_entity(user_id)
            try:
                try:
                    first_name = user_info.first_name
                except AttributeError:
                    first_name = "no first_name"
                
                try:
                    last_name = user_info.last_name
                except AttributeError:
                    last_name = "no last_name"
                
                try:
                    username = user_info.username
                except AttributeError:
                    username = "no username"
                
                known_users[user_id] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                }
                i = 1
            except AttributeError:
                i = 1
    return known_users, known_chats, known_groups


async def a_getUserInfo (client, stuff):
    try:
        user = await client.get_entity(stuff)
        return user
    except AttributeError:
        i = 1


def getUserInfo (client, stuff):
    try:
        user = client.get_entity(stuff)
        return user
    except AttributeError:
        i = 1


def save_backup_tracker (backup_tracker_file, tracker):
    with open(backup_tracker_file, 'w') as f:
        json.dump(tracker, f, indent=4)


async def fetch_messages (client, chat, offset_id=0, limit=100):
    all_messages = []
    while True:
        history = await client(
            GetHistoryRequest(
                peer=chat,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            )
        )
        if not history.messages:
            break
        messages = history.messages
        all_messages.extend(messages)
        offset_id = messages[-1].id
    return all_messages


def deserialize_message (message):
    message_dict = OrderedDict()
    message_dict['id'] = message.id
    message_dict['date'] = message.date.isoformat() if message.date else None
    message_dict['message'] = message.message
    from_id = None
    user_info = GetFullUserRequest(message.from_id)
    try:
        from_id = message.from_id.user_id if message.from_id else message.from_id.chat_id
    except AttributeError:
        i = 1
    else:
        from_id = message.from_id.user_id if message.from_id else "blah"
    finally:
        f = 1
    
    if from_id:
        from_user_info = GetFullUserRequest(message.from_id)
        i = 1
    message_dict['from_id'] = from_id
    
    to_id = None
    try:
        to_id = message.to_id.user_id if message.to_id else None
    except AttributeError:
        i = 1
    else:
        to_id = message.to_id.user_id if message.to_id else 'blah'
    finally:
        f = 1
    if to_id:
        to_user_info = GetFullUserRequest(message.to_id)
        i = 1
    message_dict['to_id'] = to_id
    
    message_dict['reply_to_msg_id'] = message.reply_to.reply_to_msg_id if message.reply_to else None
    message_dict['media'] = str(message.media) if message.media else None
    return message_dict


def format_message (message):
    message_dict = deserialize_message(message)
    timestamp = message.date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    sender = message_dict['from_id']
    content = message.message or 'Media'
    reply_to = f" (reply to {message.reply_to.reply_to_msg_id})" if message.reply_to else ''
    
    out = f"[{timestamp}] {sender}: {content}{reply_to}\n"
    i = 1
    
    return out


async def save_messages_to_file (client, messages, folder_path, chat_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for message in messages:
        message_date = message.date.astimezone(timezone.utc).strftime('%Y-%m-%d')
        daily_folder_path = os.path.join(folder_path, message_date)
        if not os.path.exists(daily_folder_path):
            os.makedirs(daily_folder_path)
        
        file_path = os.path.join(daily_folder_path, f'messages.log')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(format_message(message))
        
        if message.media:
            # await download_media(messages, client, chat_name, base_folder_path='telegram_messages')
            media_folder_path = os.path.join(daily_folder_path, 'media')
            
            if not os.path.exists(media_folder_path):
                os.makedirs(media_folder_path)
            
            # await download_media(messages, client, chat_name, base_folder_path=media_folder_path)
            # save_files_from_message(client, message, media_folder_path)


async def download_media (messages, client, channel_name, base_folder_path):
    for message in tqdm(messages):
        if message.media:
            message.download_media(f'files/{channel_name}/')
        # message.download_media(f'{base_folder_path}/{channel_name}/files/')


async def download_all_media (client, messages, folder_path, chat_name):
    folder = f'files/{chat_name}/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    print(f"Downloading media to {folder}")
    for message in tqdm(messages):
        if message.media:
            try:
                file_name = message.file.name
                if file_name:
                    file = await message.download_media(file=f'files/{chat_name}/{file_name}')
                    i = 1
                else:
                    i = 1
            except AttributeError:
                file_name = f"media_{message.id}"
            
            # await message.download_media(f'files/{chat_name}/{file_name}')


def save_files_from_message (client, message, folder_path):
    if message.media:
        
        file_name = None
        if hasattr(message.media, 'document'):
            # blah = message.media.document.attributes
            for attribute in message.media.document.attributes:
                if isinstance(attribute, DocumentAttributeFilename):
                    file_name = attribute.file_name
                    break
        elif hasattr(message.media, 'photo'):
            file_name = f"photo_{message.id}.jpg"
        # elif hasattr(message.media, 'webpage'):
        #     file_name = message.media.webpage.url
        
        if not file_name:
            file_name = f"media_{message.id}"
        
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'wb') as fd:
            blah = client.download_media(message.media, fd)
            i = 1
        
        print(f"Downloaded file to {file_path}")


def update_known_chats (client, chat, known_chats):
    chat_id = chat.id
    if chat_id not in known_chats:
        i = 1
        
        known_chats[chat_id] = {
            'title': chat.title,
            'username': chat.username
        }
    
    return known_chats


def update_known_groups (client, chat, known_groups):
    chat_id = chat.id
    if chat_id not in known_groups:
        i = 1
        
        known_groups[chat_id] = {
            'title': chat.title,
            # 'username': chat.username
        }
    
    return known_groups


def _get_media(self, msg):
    if isinstance(msg.media, telethon.tl.types.MessageMediaWebPage) and \
            not isinstance(msg.media.webpage, telethon.tl.types.WebPageEmpty):
        return Media(
            id=msg.id,
            type="webpage",
            url=msg.media.webpage.url,
            title=msg.media.webpage.title,
            description=msg.media.webpage.description if msg.media.webpage.description else None,
            thumb=None
        )
    elif isinstance(msg.media, telethon.tl.types.MessageMediaPhoto) or \
            isinstance(msg.media, telethon.tl.types.MessageMediaDocument) or \
            isinstance(msg.media, telethon.tl.types.MessageMediaContact):
        if self.config["download_media"]:
            # Filter by extensions?
            if len(self.config["media_mime_types"]) > 0:
                if hasattr(msg, "file") and hasattr(msg.file, "mime_type") and msg.file.mime_type:
                    if msg.file.mime_type not in self.config["media_mime_types"]:
                        logging.info(
                            "skipping media #{} / {}".format(msg.file.name, msg.file.mime_type))
                        return

            logging.info("downloading media #{}".format(msg.id))
            try:
                basename, fname, thumb = self._download_media(msg)
                return Media(
                    id=msg.id,
                    type="photo",
                    url=fname,
                    title=basename,
                    description=None,
                    thumb=thumb
                )
            except Exception as e:
                logging.error(
                    "error downloading media: #{}: {}".format(msg.id, e))


async def main ():
    env_vars = load_dotenv("BullishTechOps.env")
    
    known_users = load_pickle_file(env_vars["known_users_file"])
    known_chats = load_pickle_file(env_vars["known_chats_file"])
    known_groups = load_pickle_file(env_vars["known_groups_file"])
    
    client = await tlg_connect(
        env_vars["app_id"],
        env_vars['app_hash'],
        env_vars['phone_num'],
        env_vars['session_string']
        )

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        entity = await client.get_entity(dialog.id)

        try:
            known_chats[entity.title] = entity
        except AttributeError:
            i = 1
        
        if dialog.is_user:
            pass
            # known_users = await a_update_known_entities(client, dialog.entity, known_users, known_chats, known_groups)
        elif dialog.is_group:
            i = 1
            known_groups = update_known_groups(client, dialog.entity, known_groups)
        elif dialog.is_channel:
            i = 1
            known_chats = update_known_chats(client, dialog.entity, known_chats)
    save_pickle_file(known_chats, env_vars["known_chats_file"])
    save_pickle_file(known_groups, env_vars["known_groups_file"])
    
    backup_tracker = load_backup_tracker(env_vars['backup_tracker_file'])
    
    for dialog in dialogs:
        chat = dialog.entity
        if dialog.is_group or dialog.is_channel:
            chat_name = chat.title if hasattr(chat, 'title') else chat.username
            if not chat_name:
                chat_name = str(chat.id)
            folder_path = os.path.join('telegram_messages', chat_name)
            last_message_id = backup_tracker.get(str(chat.id), 0)
            
            # TODO: Set Fetch messages from the last message id
            # messages = await fetch_messages(client, chat, offset_id=last_message_id)
            
            messages = await fetch_messages(client, chat, offset_id=0)
            
            if messages:
                # await download_all_media(client, messages, folder_path, chat_name)
                # continue
                blah = await a_update_known_entities(client, messages, known_users, known_chats, known_groups)
                file = await download_media(messages, client, chat_name, base_folder_path='telegram_messages')
                for message in messages:
                    backup_tracker[str(chat.id)] = messages[-1].id
                    await update_known_entities(client, message, known_users, known_chats, known_groups)
                    # await a_update_known_entities(client, message, known_users, known_chats, known_groups)
                
                blah = await save_messages_to_file(client, messages, folder_path, chat_name)
                # save_files_from_messages(messages, folder_path)
                backup_tracker[str(chat.id)] = messages[-1].id
                # save_backup_tracker(env_vars['backup_tracker_file'], backup_tracker)
                save_pickle_file(backup_tracker, env_vars['backup_tracker_file'])
                save_pickle_file(known_users, env_vars["known_users_file"])
                save_pickle_file(known_chats, env_vars["known_chats_file"])
                save_pickle_file(known_groups, env_vars["known_groups_file"])
    
    # save_backup_tracker(env_vars['backup_tracker_file'], backup_tracker)
    # save_pickle_file(known_users, env_vars["known_users_file"])
    # save_pickle_file(known_chats, env_vars["known_chats_file"])
    # save_pickle_file(known_groups, env_vars["known_groups_file"])
    
    await asyncio.sleep(200)
    
    await client.disconnect()


def backup_previous_day_folder ():
    base_folder_path = 'telegram_messages'
    backup_folder_path = 'telegram_backup'
    # Get the previous date in GMT
    previous_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')
    source_folder = os.path.join(base_folder_path, previous_date)
    if os.path.exists(source_folder):
        destination_folder = os.path.join(backup_folder_path, previous_date)
        shutil.copytree(source_folder, destination_folder)
        print(f"Backup completed for {previous_date}")


def schedule_backup ():
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_previous_day_folder, 'cron', hour=0, minute=1, timezone='UTC')
    scheduler.start()


client = tlg_connect(env_vars['session_string'])


if __name__ == '__main__':
    # Start the backup scheduler
    schedule_backup()
    
    asyncio.run(main())
    
    # loop = asyncio.get_event_loop()
    # loop.run_forever(asyncio.run(main()))
    #
    # asyncio.run(main())

