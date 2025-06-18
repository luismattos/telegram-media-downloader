"""
Telegram Media Downloader

Um downloader de mídia e mensagens para Telegram com suporte a
downloads incrementais, organização por data e histórico detalhado.

Author: Luis Mattos
Version: 2.0.0
"""

__version__ = "2.0.0"
__author__ = "Luis Mattos"
__description__ = "Telegram Media Downloader - Download de mídia e mensagens do Telegram"

# Imports principais para facilitar o uso
from .utils.config import get_config, Config
from .utils.logging import get_logger, setup_logging, LoggerMixin
from .utils.validators import ValidationError

from .models.chat import Chat, ChatList, ChatType
from .models.message import Message, MessageList, MediaFile, MediaType

# Configuração global
config = get_config()

# Logger padrão do pacote
logger = get_logger(__name__)

__all__ = [
    # Utils
    'get_config',
    'Config', 
    'get_logger',
    'setup_logging',
    'LoggerMixin',
    'ValidationError',
    
    # Models
    'Chat',
    'ChatList', 
    'ChatType',
    'Message',
    'MessageList',
    'MediaFile',
    'MediaType',
    
    # Globals
    'config',
    'logger'
]
