import os
import json
import logging
import shutil
import asyncio
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from typing import OrderedDict, Dict

import pyrogram
from pyrogram import Client
import yaml
from pyrogram.types import Audio, Document, Photo, Video, VideoNote, Voice
from rich.logging import RichHandler


from utils.log import LogFilter
from utils.meta import print_meta

from utils.base_config import base_config
from utils.load_dotenv import load_dotenv


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler()],
# )
# logging.getLogger("pyrogram.session.session").addFilter(LogFilter())
# logging.getLogger("pyrogram.client").addFilter(LogFilter())
# logger = logging.getLogger("media_downloader")

env_vars = load_dotenv("BullishTechOps.env")

app = Client(name='BullishTechOps',
              api_id=env_vars['api_id'],
              api_hash=env_vars['api_hash'],
              phone_number=env_vars['phone_num'],
              # session_string=env_vars['session_string'],
                )


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


async def main ():
    ...

 
if __name__ == '__main__':
    # Start the backup scheduler
    schedule_backup()
    
    # Run the main function to fetch messages
    # asyncio.run(main())
    app.run(main())
