#!/usr/bin/env python3
"""
Lista todos os chats do usuário, separando por categorias: Grupos, Canais de transmissão e Usuários.
"""

import asyncio
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Chat, Channel, User
from telegram_media_downloader.utils.config import get_config
from telegram_media_downloader.utils.logging import setup_logging

async def list_all_chats():
    config = get_config()
    setup_logging("list_chats")

    client = TelegramClient(
        config.session_name,
        config.api_id,
        config.api_hash
    )

    try:
        await client.start()
        print("\n🔍 Listando todos os chats do usuário...\n")

        groups = []
        channels = []
        users = []
        outros = []

        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            chat_info = {
                "title": dialog.title,
                "entity_type": type(entity).__name__,
                "id": entity.id,
                "username": getattr(entity, 'username', None),
                "megagroup": getattr(entity, 'megagroup', None),
                "broadcast": getattr(entity, 'broadcast', None),
                "type": None
            }

            if isinstance(entity, Chat):
                chat_info["type"] = "Group"
                groups.append(chat_info)
            elif isinstance(entity, Channel):
                if getattr(entity, 'megagroup', False):
                    chat_info["type"] = "Supergroup"
                    groups.append(chat_info)
                elif getattr(entity, 'broadcast', False):
                    chat_info["type"] = "Channel (Broadcast)"
                    channels.append(chat_info)
                else:
                    chat_info["type"] = "Group (Channel)"
                    groups.append(chat_info)
            elif isinstance(entity, User):
                chat_info["type"] = "User"
                users.append(chat_info)
            else:
                chat_info["type"] = "Outro"
                outros.append(chat_info)

        # Exibir Grupos
        print("="*50)
        print("\U0001F465 GRUPOS (inclui grupos normais e supergrupos)")
        print("="*50)
        for g in groups:
            print(f"Título: {g['title']}")
            print(f"Tipo: {g['type']} ({g['entity_type']})")
            print(f"ID: {g['id']}")
            print(f"Username: {g['username']}")
            print("-"*30)
        print(f"Total de grupos: {len(groups)}\n")

        # Exibir Canais
        print("="*50)
        print("\U0001F4E2 CANAIS DE TRANSMISSÃO")
        print("="*50)
        for c in channels:
            print(f"Título: {c['title']}")
            print(f"Tipo: {c['type']} ({c['entity_type']})")
            print(f"ID: {c['id']}")
            print(f"Username: {c['username']}")
            print("-"*30)
        print(f"Total de canais: {len(channels)}\n")

        # Exibir Usuários
        print("="*50)
        print("\U0001F464 USUÁRIOS (contatos/bots)")
        print("="*50)
        for u in users:
            print(f"Nome: {u['title']}")
            print(f"ID: {u['id']}")
            print(f"Username: {u['username']}")
            print("-"*30)
        print(f"Total de usuários: {len(users)}\n")

        # Exibir outros
        if outros:
            print("="*50)
            print("OUTROS TIPOS DE CHATS")
            print("="*50)
            for o in outros:
                print(f"Título: {o['title']}")
                print(f"Tipo: {o['type']} ({o['entity_type']})")
                print(f"ID: {o['id']}")
                print(f"Username: {o['username']}")
                print("-"*30)
            print(f"Total outros: {len(outros)}\n")

        # Salvar tudo em JSON
        all_data = {
            "groups": groups,
            "channels": channels,
            "users": users,
            "outros": outros,
            "timestamp": datetime.now().isoformat()
        }
        out_file = f"chat_lists/chats_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Lista completa salva em: {out_file}")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(list_all_chats()) 