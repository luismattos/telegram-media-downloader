#!/usr/bin/env python3
"""
Script de debug para listar todos os chats e mostrar informações detalhadas
"""

import asyncio
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Chat, Channel, User
from telegram_media_downloader.utils.config import get_config
from telegram_media_downloader.utils.logging import setup_logging

async def debug_all_chats():
    """Lista todos os chats com informações detalhadas para debug"""
    config = get_config()
    setup_logging("debug_chats")
    
    client = TelegramClient(
        config.session_name,
        config.api_id,
        config.api_hash
    )
    
    try:
        await client.start()
        
        print("🔍 DEBUG: Listando TODOS os chats...")
        print("=" * 60)
        
        all_chats = []
        ignored_chats = []
        
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            chat_info = {
                "title": dialog.title,
                "entity_type": type(entity).__name__,
                "id": entity.id,
                "username": getattr(entity, 'username', None),
                "is_group": False,
                "is_channel": False,
                "is_user": False,
                "is_supergroup": False,
                "megagroup": getattr(entity, 'megagroup', None),
                "broadcast": getattr(entity, 'broadcast', None),
                "verified": getattr(entity, 'verified', None),
                "scam": getattr(entity, 'scam', None),
                "fake": getattr(entity, 'fake', None),
                "bot": getattr(entity, 'bot', None),
            }
            
            # Determinar tipo
            if isinstance(entity, Chat):
                chat_info["is_group"] = True
                chat_info["type"] = "Group"
            elif isinstance(entity, Channel):
                if entity.megagroup:
                    chat_info["is_group"] = True
                    chat_info["is_supergroup"] = True
                    chat_info["type"] = "Supergroup"
                elif entity.broadcast:
                    chat_info["is_channel"] = True
                    chat_info["type"] = "Channel"
                else:
                    chat_info["is_group"] = True
                    chat_info["type"] = "Group"
            elif isinstance(entity, User):
                chat_info["is_user"] = True
                chat_info["type"] = "User"
            
            print(f"📋 {chat_info['title']}")
            print(f"   Tipo: {chat_info['type']} ({chat_info['entity_type']})")
            print(f"   ID: {chat_info['id']}")
            print(f"   Username: {chat_info['username']}")
            print(f"   É grupo: {chat_info['is_group']}")
            print(f"   É supergrupo: {chat_info['is_supergroup']}")
            print(f"   É canal: {chat_info['is_channel']}")
            print(f"   É usuário: {chat_info['is_user']}")
            print(f"   Megagroup: {chat_info['megagroup']}")
            print(f"   Broadcast: {chat_info['broadcast']}")
            print("-" * 40)
            
            if chat_info["is_group"]:
                all_chats.append(chat_info)
            else:
                ignored_chats.append(chat_info)
        
        print(f"\n📊 RESUMO:")
        print(f"   Grupos encontrados: {len(all_chats)}")
        print(f"   Chats ignorados: {len(ignored_chats)}")
        print(f"   Total: {len(all_chats) + len(ignored_chats)}")
        
        # Salvar debug completo
        debug_data = {
            "groups": all_chats,
            "ignored": ignored_chats,
            "timestamp": datetime.now().isoformat()
        }
        
        debug_file = f"debug_chats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Debug salvo em: {debug_file}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(debug_all_chats()) 