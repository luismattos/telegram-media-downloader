import os
import sys
import json
import hashlib
import asyncio
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

from telegram_media_downloader.utils.logging import get_logger
from telegram_media_downloader.utils.config import get_config

logger = get_logger(__name__)
config = get_config()

class TelegramMediaDownloader:
    def __init__(self, api_id, api_hash, download_path):
        try:
            self.client = TelegramClient('media_downloader_session', api_id, api_hash)
            self.download_path = download_path
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                logger.info(f"Created download directory: {download_path}")
            # Remover histórico global - agora será específico por grupo
            self.downloaded_files = {}
            # Cache para informações de usuários
            self.user_cache = {}
        except ValueError as e:
            logger.error("Invalid API credentials. Please check your API_ID and API_HASH.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error initializing client: {str(e)}")
            sys.exit(1)

    def load_history(self, chat_name):
        """Carrega histórico específico do grupo/canal"""
        history_file = os.path.join(self.download_path, chat_name, 'download_history.json')
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading history for {chat_name}: {str(e)}")
                return {}
        return {}

    def save_history(self, chat_name):
        """Salva histórico específico do grupo/canal"""
        try:
            history_file = os.path.join(self.download_path, chat_name, 'download_history.json')
            with open(history_file, 'w') as f:
                json.dump(self.downloaded_files, f, indent=2)
            logger.info(f"History saved for {chat_name}: {history_file}")
        except Exception as e:
            logger.error(f"Error saving history for {chat_name}: {str(e)}")

    def get_file_hash(self, message):
        try:
            unique_str = f"{message.id}_{message.date.timestamp()}"
            return hashlib.md5(unique_str.encode()).hexdigest()
        except Exception:
            return None

    async def find_chat_by_title(self, title):
        try:
            async for dialog in self.client.iter_dialogs():
                if dialog.name.lower() == title.lower():
                    return dialog.entity
            return None
        except Exception as e:
            logger.error(f"Error finding chat: {str(e)}")
            return None

    def save_conversation_entry(self, message, chat_download_path, chat_name, media_filename=None):
        """
        Salva uma entrada no arquivo de conversa do grupo, incluindo:
        - Mensagens de texto
        - Mensagens de serviço
        - Mensagens de mídia (imagem, vídeo, documento, etc.)
        """
        try:
            conversation_file = os.path.join(chat_download_path, f"{chat_name}_conversation.txt")
            timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")
            sender_info = self.get_user_info_from_message(message)
            entry = None

            # Mensagens de texto
            if hasattr(message, 'text') and message.text:
                entry = f"[{timestamp}] {sender_info}:\n{message.text}\n"
            # Mensagens de mídia
            elif media_filename:
                media_type = self.get_media_type(message)
                entry = f"[{timestamp}] {sender_info}: [{media_type} enviado: {media_filename}]\n"
            # Mensagens de serviço
            elif hasattr(message, 'action') and message.action:
                action_desc = self.describe_service_action(message)
                entry = f"[{timestamp}] {action_desc}\n"
            else:
                # Mensagem desconhecida
                entry = f"[{timestamp}] {sender_info}: [mensagem não suportada]\n"

            entry += "-" * 80 + "\n"
            with open(conversation_file, 'a', encoding='utf-8') as f:
                f.write(entry)
            return conversation_file
        except Exception as e:
            logger.error(f"Error saving conversation entry: {str(e)}")
            return None

    def get_media_type(self, message):
        """Retorna o tipo de mídia em português"""
        if hasattr(message, 'photo') and message.photo:
            return "imagem"
        if hasattr(message, 'video') and message.video:
            return "vídeo"
        if hasattr(message, 'document') and message.document:
            return "documento"
        if hasattr(message, 'audio') and message.audio:
            return "áudio"
        if hasattr(message, 'voice') and message.voice:
            return "áudio (voz)"
        return "mídia"

    def describe_service_action(self, message):
        """Descreve a ação de serviço de forma legível"""
        try:
            action = message.action
            # Exemplos comuns
            if hasattr(action, 'user_id'):
                user_id = action.user_id
                user_name = self.get_user_info(user_id)
                if action.__class__.__name__ == 'MessageActionChatAddUser':
                    return f"{user_name} foi adicionado ao grupo"
                if action.__class__.__name__ == 'MessageActionChatJoinedByLink':
                    return f"{user_name} entrou no grupo via link de convite"
                if action.__class__.__name__ == 'MessageActionChatDeleteUser':
                    return f"{user_name} saiu do grupo"
            # Outros tipos
            return str(action)
        except Exception as e:
            logger.debug(f"Erro ao descrever ação de serviço: {e}")
            return "[ação de serviço]"

    async def download_media_from_chat(self, chat_entity, limit=None):
        try:
            # Criar nome seguro para o diretório
            chat_name = self.get_safe_directory_name(chat_entity)
            chat_download_path = os.path.join(self.download_path, chat_name)
            
            logger.info(f"Starting download from {chat_entity.title}")
            logger.info(f"Download path: {chat_download_path}")
            
            # Criar diretório do chat se não existir
            if not os.path.exists(chat_download_path):
                os.makedirs(chat_download_path)
                logger.info(f"Created chat directory: {chat_download_path}")
            
            # Carregar histórico específico deste grupo
            self.downloaded_files = self.load_history(chat_name)
            logger.info(f"Loaded history for {chat_name}: {len(self.downloaded_files)} files")
            
            messages = await self.client.get_messages(chat_entity, limit=limit)
            total_messages = len(messages)
            logger.info(f"Found {total_messages} messages to process")
            downloaded_media = 0
            downloaded_text = 0
            skipped_count = 0
            processed_count = 0
            
            # Criar cabeçalho do arquivo de conversa único
            self.save_conversation_header(chat_name, chat_download_path)
            
            # Processar mensagens em ordem cronológica
            for message in messages:
                processed_count += 1
                if processed_count % 100 == 0:
                    logger.info(f"Processed {processed_count}/{total_messages} messages")
                
                file_hash = self.get_file_hash(message)
                if file_hash in self.downloaded_files:
                    skipped_count += 1
                    continue
                
                media_filename = None
                # Processar mídia
                if message.media:
                    try:
                        media_dir = os.path.join(chat_download_path, "media")
                        if not os.path.exists(media_dir):
                            os.makedirs(media_dir)
                        file_path = await self.client.download_media(
                            message.media,
                            file=os.path.join(media_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_")
                        )
                        if file_path:
                            downloaded_media += 1
                            media_filename = os.path.basename(file_path)
                            self.downloaded_files[file_hash] = {
                                'file_path': file_path,
                                'message_id': message.id,
                                'date': message.date.isoformat(),
                                'type': 'media',
                                'chat_name': chat_name
                            }
                            logger.info(f"Downloaded media: {file_path}")
                    except Exception as e:
                        logger.error(f"Error downloading media from message {message.id}: {str(e)}")
                
                # Registrar toda mensagem no arquivo de conversa
                try:
                    self.save_conversation_entry(message, chat_download_path, chat_name, media_filename)
                except Exception as e:
                    logger.error(f"Error saving conversation entry for message {message.id}: {str(e)}")
                
                # Registrar texto no histórico (para estatística)
                if message.text and message.text.strip():
                    try:
                        self.downloaded_files[file_hash] = {
                            'file_path': chat_download_path,
                            'message_id': message.id,
                            'date': message.date.isoformat(),
                            'type': 'text',
                            'chat_name': chat_name
                        }
                        downloaded_text += 1
                        logger.info(f"Added text to conversation: {chat_download_path}")
                    except Exception as e:
                        logger.error(f"Error saving text message {message.id}: {str(e)}")
                
                if (downloaded_media + downloaded_text) % 10 == 0:
                    self.save_history(chat_name)
            
            self.save_history(chat_name)
            logger.info(f"Download completed:")
            logger.info(f"- Media files downloaded: {downloaded_media}")
            logger.info(f"- Text messages added to conversation: {downloaded_text}")
            logger.info(f"- Files skipped (already downloaded): {skipped_count}")
            logger.info(f"Conversation file: {chat_download_path}/{chat_name}_conversation.txt")
        except Exception as e:
            logger.error(f"Error in download_media_from_chat: {str(e)}")

    def get_safe_directory_name(self, chat_entity):
        """Cria um nome seguro para diretório baseado no título do chat"""
        try:
            if hasattr(chat_entity, 'title'):
                # Para grupos, canais e supergrupos
                name = chat_entity.title
            elif hasattr(chat_entity, 'first_name'):
                # Para usuários
                first_name = chat_entity.first_name or ""
                last_name = chat_entity.last_name or ""
                name = f"{first_name} {last_name}".strip()
            else:
                # Fallback
                name = f"chat_{chat_entity.id}"
            
            # Remover caracteres inválidos para nome de diretório
            import re
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
            safe_name = safe_name.strip()
            
            # Limitar tamanho
            if len(safe_name) > 50:
                safe_name = safe_name[:50]
            
            return safe_name
        except Exception as e:
            logger.error(f"Error creating safe directory name: {e}")
            return f"chat_{chat_entity.id}"

    async def close(self):
        await self.client.disconnect()

    def get_user_info(self, sender_id):
        """Obtém informações do usuário com cache"""
        if sender_id in self.user_cache:
            return self.user_cache[sender_id]
        
        # Por enquanto, usar apenas o ID
        # O problema é que get_entity pode falhar para usuários com privacidade
        user_info = f"User_{sender_id}"
        self.user_cache[sender_id] = user_info
        return user_info

    def get_user_info_from_message(self, message):
        """Obtém informações do usuário diretamente da mensagem"""
        try:
            # Tentar obter informações do sender da mensagem
            if hasattr(message, 'sender') and message.sender:
                sender = message.sender
                
                # Verificar se tem username
                if hasattr(sender, 'username') and sender.username:
                    return f"@{sender.username} (ID: {sender.id})"
                
                # Verificar se tem nome completo
                if hasattr(sender, 'first_name') or hasattr(sender, 'last_name'):
                    first_name = getattr(sender, 'first_name', '') or ''
                    last_name = getattr(sender, 'last_name', '') or ''
                    full_name = f"{first_name} {last_name}".strip()
                    
                    if full_name:
                        return f"{full_name} (ID: {sender.id})"
                    elif first_name:
                        return f"{first_name} (ID: {sender.id})"
                
                # Verificar se tem display_name
                if hasattr(sender, 'display_name') and sender.display_name:
                    return f"{sender.display_name} (ID: {sender.id})"
            
            # Fallback para sender_id
            if hasattr(message, 'sender_id') and message.sender_id:
                return f"User_{message.sender_id}"
            
            return "Unknown"
            
        except Exception as e:
            logger.debug(f"Error getting user info from message: {e}")
            if hasattr(message, 'sender_id') and message.sender_id:
                return f"User_{message.sender_id}"
            return "Unknown"

    def save_conversation_header(self, chat_name, chat_download_path):
        """Cria cabeçalho para o arquivo de conversa único"""
        try:
            conversation_file = os.path.join(chat_download_path, f"{chat_name}_conversation.txt")
            
            # Só criar cabeçalho se o arquivo não existir
            if not os.path.exists(conversation_file):
                header = f"""
{'='*80}
CONVERSA: {chat_name}
{'='*80}

"""
                with open(conversation_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                    
        except Exception as e:
            logger.error(f"Error creating conversation header: {str(e)}")

async def run_downloader():
    api_id = config.api_id
    api_hash = config.api_hash
    download_path = str(config.download_path)
    if not api_id or not api_hash:
        logger.error("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables")
        logger.error("You can get these from https://my.telegram.org/apps")
        sys.exit(1)
    downloader = TelegramMediaDownloader(api_id, api_hash, download_path)
    try:
        await downloader.client.start()
        if len(sys.argv) > 1:
            chat_title = sys.argv[1]
        else:
            chat_title = input("Enter chat title: ")
        chat_entity = await downloader.find_chat_by_title(chat_title)
        if chat_entity:
            await downloader.download_media_from_chat(chat_entity, limit=None)
        else:
            logger.error(f"Could not find chat with title: {chat_title}")
            logger.error("Please make sure you are a member of this chat/channel")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        await downloader.close()
