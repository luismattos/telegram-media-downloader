import os
import sys
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Chat, Channel
from telegram_media_downloader.utils.logging import get_logger
from telegram_media_downloader.utils.config import get_config

logger = get_logger(__name__)
config = get_config()

class TelegramChatLister:
    def __init__(self, api_id, api_hash, output_dir="chat_lists"):
        self.client = TelegramClient('chat_lister_session', api_id, api_hash)
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

    def save_chats_to_file(self, chats_data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"chats_list_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chats_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Chats list saved to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving chats list: {str(e)}")
            return None

    async def list_chats(self, save_to_file=True):
        try:
            logger.info("Fetching your groups...")
            chats_data = []
            total_groups = 0
            skipped = 0
            async for dialog in self.client.iter_dialogs():
                chat = dialog.entity
                is_group = False
                chat_type = None
                # Supergrupos (Channel com megagroup=True)
                if isinstance(chat, Channel) and getattr(chat, 'megagroup', False):
                    is_group = True
                    chat_type = "Supergroup"
                # Grupos normais (Chat)
                elif isinstance(chat, Chat):
                    is_group = True
                    chat_type = "Group"
                # Só processa grupos
                if is_group and hasattr(chat, 'title'):
                    total_groups += 1
                    username = f"@{chat.username}" if hasattr(chat, 'username') and chat.username else "No username"
                    chat_info = {
                        "title": chat.title,
                        "type": chat_type,
                        "username": username,
                        "id": chat.id,
                        "invite_link": getattr(chat, 'invite_link', None)
                    }
                    chats_data.append(chat_info)
                    print(f"\n{'='*50}")
                    print(f"Title: {chat.title}")
                    print(f"Type: {chat_type}")
                    print(f"Username: {username}")
                    print(f"ID: {chat.id}")
                    if getattr(chat, 'invite_link', None):
                        print(f"Invite Link: {chat.invite_link}")
                    print(f"{'='*50}")
                else:
                    skipped += 1
            if save_to_file and chats_data:
                saved_file = self.save_chats_to_file(chats_data)
                if saved_file:
                    print(f"\n📁 Lista de grupos salva em: {saved_file}")
                    print(f"📊 Total de grupos encontrados: {total_groups}")
                    print(f"⚠️  Chats ignorados (não são grupos): {skipped}")
            logger.info(f"Successfully listed {total_groups} groups (skipped {skipped})")
        except Exception as e:
            logger.error(f"Error listing groups: {str(e)}")

    async def close(self):
        await self.client.disconnect()

async def run_chat_lister():
    api_id = config.api_id
    api_hash = config.api_hash
    if not api_id or not api_hash:
        logger.error("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables")
        logger.error("You can get these from https://my.telegram.org/apps")
        return
    lister = TelegramChatLister(api_id, api_hash)
    try:
        await lister.client.start()
        await lister.list_chats()
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        await lister.close()
