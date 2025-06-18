import os
import sys
import json
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telegram_media_downloader.utils.logging import get_logger
from telegram_media_downloader.utils.config import get_config

logger = get_logger(__name__)
config = get_config()

class InteractiveSetup:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.download_path = None
        self.chats = []
        self.selected_chat = None
        self.download_limit = None
        self.download_photos = True
        self.download_videos = True
        self.download_documents = True
        self.download_text = True
        logger.info("InteractiveSetup initialized")
    def print_header(self):
        print("\n" + "="*60)
        print("🤖 TELEGRAM MEDIA DOWNLOADER - SETUP INTERATIVO")
        print("="*60)
        print("Configure e use o downloader de mídia do Telegram")
        print("="*60 + "\n")
        logger.info("Interactive setup header displayed")
    def print_success(self, message):
        print(f"✅ {message}")
        logger.info(f"SUCCESS: {message}")
    def print_error(self, message):
        print(f"❌ {message}")
        logger.error(f"ERROR: {message}")
    def print_info(self, message):
        print(f"ℹ️  {message}")
        logger.info(f"INFO: {message}")
    def print_warning(self, message):
        print(f"⚠️  {message}")
        logger.warning(f"WARNING: {message}")
    def get_input(self, prompt, default=None):
        if default:
            user_input = input(f"{prompt} (padrão: {default}): ").strip()
            result = user_input if user_input else default
        else:
            user_input = input(f"{prompt}: ").strip()
            result = user_input
        logger.debug(f"User input for '{prompt}': {result}")
        return result
    def get_yes_no(self, prompt, default="n"):
        while True:
            response = self.get_input(f"{prompt} (y/n)", default).lower()
            if response in ['y', 'yes', 's', 'sim']:
                logger.debug(f"User answered YES to: {prompt}")
                return True
            elif response in ['n', 'no', 'não']:
                logger.debug(f"User answered NO to: {prompt}")
                return False
            else:
                print("Por favor, responda 'y' para sim ou 'n' para não.")
                logger.debug(f"Invalid user input: {response}")
    def check_api_credentials(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        if self.api_id and self.api_hash:
            self.print_success("Credenciais da API encontradas no arquivo .env")
            logger.info("API credentials found in .env file")
            return True
        else:
            self.print_warning("Credenciais da API não encontradas")
            logger.warning("API credentials not found in .env file")
            return False
    def configure_api_credentials(self):
        print("\n🔑 CONFIGURAÇÃO DA API DO TELEGRAM")
        print("-" * 40)
        logger.info("Starting API credentials configuration")
        self.print_info("Para obter suas credenciais da API:")
        print("1. Acesse: https://my.telegram.org/auth")
        print("2. Faça login com seu número de telefone")
        print("3. Clique em 'API development tools'")
        print("4. Preencha o formulário e crie um aplicativo")
        print("5. Copie o api_id e api_hash\n")
        self.api_id = self.get_input("Digite seu API ID")
        self.api_hash = self.get_input("Digite seu API Hash")
        if not self.api_id.isdigit():
            self.print_error("API ID deve ser um número")
            logger.error(f"Invalid API ID format: {self.api_id}")
            return False
        if len(self.api_hash) != 32:
            self.print_error("API Hash deve ter 32 caracteres")
            logger.error(f"Invalid API Hash length: {len(self.api_hash)}")
            return False
        self.save_credentials_to_env()
        logger.info("API credentials configured successfully")
        return True
    def save_credentials_to_env(self):
        try:
            env_content = f"""# Telegram Media Downloader Configuration\nTELEGRAM_API_ID={self.api_id}\nTELEGRAM_API_HASH={self.api_hash}\n"""
            with open('.env', 'w') as f:
                f.write(env_content)
            self.print_success("Credenciais salvas no arquivo .env")
            logger.info("Credentials saved to .env file")
        except Exception as e:
            self.print_error(f"Erro ao salvar credenciais: {e}")
            logger.error(f"Error saving credentials to .env: {e}")
    def configure_download_path(self):
        print("\n📁 CONFIGURAÇÃO DO DIRETÓRIO DE DOWNLOAD")
        print("-" * 40)
        logger.info("Starting download path configuration")
        current_path = os.getenv('TELEGRAM_DOWNLOAD_PATH', '~/Downloads/telegram')
        self.print_info(f"Diretório atual: {current_path}")
        if self.get_yes_no("Deseja alterar o diretório de download?", "n"):
            new_path = self.get_input("Digite o novo caminho", current_path)
            self.download_path = os.path.expanduser(new_path)
            self.update_env_file('TELEGRAM_DOWNLOAD_PATH', new_path)
            self.print_success(f"Diretório de download configurado: {new_path}")
            logger.info(f"Download path configured: {new_path}")
        else:
            self.download_path = os.path.expanduser(current_path)
            logger.info(f"Using default download path: {self.download_path}")
    def update_env_file(self, key, value):
        try:
            env_lines = []
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_lines = f.readlines()
            env_lines = [line for line in env_lines if not line.startswith(f'{key}=')]
            env_lines.append(f'{key}={value}\n')
            with open('.env', 'w') as f:
                f.writelines(env_lines)
            logger.info(f"Updated .env file with {key}={value}")
        except Exception as e:
            self.print_error(f"Erro ao atualizar arquivo .env: {e}")
            logger.error(f"Error updating .env file: {e}")
    async def list_available_chats(self):
        print("\n📋 LISTANDO GRUPOS E CANAIS DISPONÍVEIS")
        print("-" * 40)
        logger.info("Starting chat listing process")
        try:
            client = TelegramClient('setup_session', self.api_id, self.api_hash)
            await client.start()
            self.print_info("Conectando ao Telegram...")
            logger.info("Connected to Telegram")
            chats = []
            async for dialog in client.iter_dialogs():
                chat = dialog.entity
                
                # Determinar o título baseado no tipo de entidade
                if hasattr(chat, 'title'):
                    # Para grupos, canais e supergrupos
                    title = chat.title
                elif hasattr(chat, 'first_name'):
                    # Para usuários
                    first_name = chat.first_name or ""
                    last_name = chat.last_name or ""
                    title = f"{first_name} {last_name}".strip()
                else:
                    # Fallback
                    title = str(chat.id)
                
                # Determinar tipo
                if hasattr(chat, 'megagroup') and chat.megagroup:
                    chat_type = "Supergroup"
                elif hasattr(chat, 'gigagroup') and chat.gigagroup:
                    chat_type = "Gigagroup"
                elif hasattr(chat, 'broadcast') and chat.broadcast:
                    chat_type = "Channel"
                elif hasattr(chat, 'first_name'):
                    chat_type = "User"
                else:
                    chat_type = "Group/Chat"
                
                username = f"@{chat.username}" if hasattr(chat, 'username') and chat.username else "Sem username"
                chats.append({
                    'title': title,
                    'type': chat_type,
                    'username': username,
                    'id': chat.id,
                    'entity': chat
                })
            await client.disconnect()
            if not chats:
                self.print_error("Nenhum grupo ou canal encontrado")
                logger.error("No chats found")
                return None
            logger.info(f"Found {len(chats)} chats")
            self.chats = chats
            return self.select_chat_simple()
        except Exception as e:
            self.print_error(f"Erro ao listar chats: {e}")
            logger.error(f"Error listing chats: {e}")
            return None
    def select_chat_simple(self):
        print(f"\nEncontrados {len(self.chats)} grupos/canais:")
        print("Digite o número do grupo/canal que deseja baixar:\n")
        logger.info("Starting chat selection process")
        page_size = 10
        current_page = 0
        total_pages = (len(self.chats) + page_size - 1) // page_size
        while True:
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(self.chats))
            print(f"\n📋 PÁGINA {current_page + 1}/{total_pages}")
            print("=" * 50)
            for i in range(start_idx, end_idx):
                chat = self.chats[i]
                print(f"{i+1:2d}. {chat['title']}")
                print(f"    Tipo: {chat['type']} | Username: {chat['username']}")
                print()
            if total_pages > 1:
                print("Navegação: 'n' = próxima página, 'p' = página anterior, 'q' = sair")
            choice = self.get_input("Digite o número do grupo/canal (ou comando de navegação)").strip().lower()
            if choice == 'n' and current_page < total_pages - 1:
                current_page += 1
                logger.debug(f"Navigating to next page: {current_page + 1}")
                continue
            elif choice == 'p' and current_page > 0:
                current_page -= 1
                logger.debug(f"Navigating to previous page: {current_page + 1}")
                continue
            elif choice == 'q':
                logger.info("User cancelled chat selection")
                return None
            elif choice.isdigit():
                choice_num = int(choice) - 1
                if 0 <= choice_num < len(self.chats):
                    selected_chat = self.chats[choice_num]
                    self.print_success(f"Selecionado: {selected_chat['title']}")
                    logger.info(f"Chat selected: {selected_chat['title']} (ID: {selected_chat['id']})")
                    return selected_chat
                else:
                    self.print_error("Número inválido")
                    logger.warning(f"Invalid chat number: {choice}")
            else:
                self.print_error("Entrada inválida")
                logger.warning(f"Invalid input: {choice}")
    def configure_download_options(self):
        print("\n⚙️  CONFIGURAÇÕES DE DOWNLOAD")
        print("-" * 40)
        logger.info("Starting download options configuration")
        limit = self.get_input("Limite de mensagens (deixe vazio para todas)", "")
        if limit and limit.isdigit():
            self.download_limit = int(limit)
            logger.info(f"Download limit set to: {self.download_limit}")
        else:
            self.download_limit = None
            logger.info("No download limit set (download all messages)")
        print("\nTipos de mídia para baixar:")
        self.download_photos = self.get_yes_no("Fotos", "y")
        self.download_videos = self.get_yes_no("Vídeos", "y")
        self.download_documents = self.get_yes_no("Documentos", "y")
        self.download_text = self.get_yes_no("Mensagens de texto", "y")
        logger.info(f"Download options - Photos: {self.download_photos}, Videos: {self.download_videos}, Documents: {self.download_documents}, Text: {self.download_text}")
        self.save_download_options()
    def save_download_options(self):
        config = {
            'download_limit': self.download_limit,
            'download_photos': self.download_photos,
            'download_videos': self.download_videos,
            'download_documents': self.download_documents,
            'download_text': self.download_text,
            'download_path': self.download_path
        }
        try:
            with open('download_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.print_success("Configurações salvas")
            logger.info("Download configuration saved to download_config.json")
        except Exception as e:
            self.print_error(f"Erro ao salvar configurações: {e}")
            logger.error(f"Error saving download configuration: {e}")
    async def start_download(self):
        if not self.selected_chat:
            self.print_error("Nenhum grupo/canal selecionado")
            logger.error("No chat selected for download")
            return
        print(f"\n🚀 INICIANDO DOWNLOAD")
        print("-" * 40)
        print(f"Grupo/Canal: {self.selected_chat['title']}")
        
        # Calcular caminho do subdiretório
        from telegram_media_downloader.core.downloader import TelegramMediaDownloader
        temp_downloader = TelegramMediaDownloader(self.api_id, self.api_hash, self.download_path)
        chat_name = temp_downloader.get_safe_directory_name(self.selected_chat['entity'])
        chat_download_path = os.path.join(self.download_path, chat_name)
        
        print(f"Diretório: {chat_download_path}")
        print(f"Limite: {self.download_limit or 'Todas as mensagens'}")
        logger.info(f"Starting download - Chat: {self.selected_chat['title']}, Path: {chat_download_path}, Limit: {self.download_limit}")
        if self.get_yes_no("Confirmar download?", "y"):
            try:
                downloader = TelegramMediaDownloader(
                    self.api_id, 
                    self.api_hash, 
                    self.download_path
                )
                logger.info("Downloader instance created successfully")
                
                # Conectar o cliente antes de usar
                await downloader.client.start()
                logger.info("Downloader client connected successfully")
                
                await downloader.download_media_from_chat(
                    self.selected_chat['entity'], 
                    self.download_limit
                )
                
                # Fechar o cliente após o download
                await downloader.close()
                
                self.print_success("Download concluído!")
                logger.info("Download completed successfully")
            except ImportError:
                self.print_error("Erro: Não foi possível importar o módulo telegram_media_downloader")
                self.print_info("Certifique-se de que o pacote está instalado corretamente")
                logger.error("Failed to import telegram_media_downloader module")
            except Exception as e:
                self.print_error(f"Erro durante o download: {e}")
                logger.error(f"Error during download: {e}", exc_info=True)
        else:
            logger.info("Download cancelled by user")
    async def run_setup(self):
        self.print_header()
        logger.info("Starting interactive setup process")
        
        # Configurações iniciais (só uma vez)
        try:
            if not self.check_api_credentials():
                if not self.configure_api_credentials():
                    self.print_error("Configuração da API falhou")
                    logger.error("API configuration failed")
                    return
            self.configure_download_path()
        except Exception as e:
            self.print_error(f"Erro durante configuração inicial: {e}")
            logger.error(f"Initial configuration error: {e}", exc_info=True)
            return
        
        # Loop principal
        while True:
            try:
                # Listar chats disponíveis
                self.selected_chat = await self.list_available_chats()
                if not self.selected_chat:
                    self.print_error("Nenhum grupo/canal selecionado")
                    logger.error("No chat selected")
                    break
                
                # Configurar opções de download
                self.configure_download_options()
                
                # Executar download
                await self.start_download()
                
                # Perguntar o que fazer depois
                if not self.show_continue_menu():
                    break
                    
            except KeyboardInterrupt:
                self.print_warning("Operação cancelada pelo usuário")
                logger.warning("Operation cancelled by user (KeyboardInterrupt)")
                break
            except Exception as e:
                self.print_error(f"Erro durante a operação: {e}")
                logger.error(f"Operation error: {e}", exc_info=True)
                if not self.get_yes_no("Tentar novamente?", "y"):
                    break
        
        self.print_success("Programa finalizado!")
        logger.info("Program finished successfully")

    def show_continue_menu(self):
        """Mostra menu de opções após o download"""
        print(f"\n🔄 O QUE VOCÊ QUER FAZER AGORA?")
        print("-" * 40)
        print("1. Baixar de outro grupo/canal")
        print("2. Alterar diretório de download")
        print("3. Sair do programa")
        print("-" * 40)
        
        while True:
            choice = self.get_input("Digite sua escolha (1-3)", "1").strip()
            
            if choice == "1":
                logger.info("User chose to download from another chat")
                return True
            elif choice == "2":
                logger.info("User chose to change download directory")
                self.configure_download_path()
                return True
            elif choice == "3":
                logger.info("User chose to exit")
                return False
            else:
                self.print_error("Opção inválida. Digite 1, 2 ou 3.")
                logger.warning(f"Invalid menu choice: {choice}")

def main_interactive():
    logger.info("Starting Telegram Media Downloader Interactive Setup")
    setup = InteractiveSetup()
    try:
        asyncio.run(setup.run_setup())
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelado pelo usuário")
        logger.warning("Setup cancelled by user (KeyboardInterrupt)")
    except Exception as e:
        print(f"\n❌ Erro durante o setup: {e}")
        logger.error(f"Main error: {e}", exc_info=True)
