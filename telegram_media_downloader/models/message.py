"""
Modelo de dados para mensagens do Telegram.

Este módulo define as classes e estruturas de dados para representar
mensagens e mídia do Telegram.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MediaType(Enum):
    """Tipos de mídia disponíveis."""
    PHOTO = "photo"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"
    VOICE = "voice"
    TEXT = "text"
    STICKER = "sticker"
    ANIMATION = "animation"


@dataclass
class MediaFile:
    """
    Representa um arquivo de mídia.
    
    Attributes:
        id: ID único do arquivo
        type: Tipo de mídia
        filename: Nome do arquivo
        size: Tamanho em bytes
        mime_type: Tipo MIME
        local_path: Caminho local do arquivo baixado
        download_date: Data do download
        checksum: Checksum do arquivo (se disponível)
    """
    
    id: int
    type: MediaType
    filename: str
    size: int
    mime_type: str
    local_path: Optional[Path] = None
    download_date: Optional[datetime] = None
    checksum: Optional[str] = None
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if self.size < 0:
            raise ValueError("Tamanho do arquivo não pode ser negativo")
        
        if not self.filename.strip():
            raise ValueError("Nome do arquivo não pode estar vazio")
    
    @property
    def is_downloaded(self) -> bool:
        """Se o arquivo foi baixado."""
        return self.local_path is not None and self.local_path.exists()
    
    @property
    def file_size_mb(self) -> float:
        """Tamanho do arquivo em MB."""
        return self.size / (1024 * 1024)
    
    @property
    def file_size_formatted(self) -> str:
        """Tamanho do arquivo formatado."""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.1f} GB"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'id': self.id,
            'type': self.type.value,
            'filename': self.filename,
            'size': self.size,
            'mime_type': self.mime_type,
            'local_path': str(self.local_path) if self.local_path else None,
            'download_date': self.download_date.isoformat() if self.download_date else None,
            'checksum': self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MediaFile':
        """Cria instância a partir de dicionário."""
        # Lidar com o campo type que pode vir como string ou MediaType
        type_value = data.get('type', 'document')
        if isinstance(type_value, str):
            media_type = MediaType(type_value)
        elif isinstance(type_value, MediaType):
            media_type = type_value
        else:
            # Fallback para document se o tipo for inválido
            media_type = MediaType.DOCUMENT
        
        local_path = None
        if data.get('local_path'):
            local_path = Path(data['local_path'])
        
        download_date = None
        if data.get('download_date'):
            download_date = datetime.fromisoformat(data['download_date'])
        
        return cls(
            id=data['id'],
            type=media_type,
            filename=data['filename'],
            size=data['size'],
            mime_type=data['mime_type'],
            local_path=local_path,
            download_date=download_date,
            checksum=data.get('checksum')
        )
    
    def __str__(self) -> str:
        """Representação string do arquivo."""
        status = "✅" if self.is_downloaded else "⏳"
        return f"{status} {self.filename} ({self.file_size_formatted})"
    
    def __repr__(self) -> str:
        """Representação detalhada do arquivo."""
        return f"MediaFile(id={self.id}, filename='{self.filename}', type={self.type.value})"


@dataclass
class Message:
    """
    Representa uma mensagem do Telegram.
    
    Attributes:
        id: ID único da mensagem
        chat_id: ID do chat
        sender_id: ID do remetente
        sender_name: Nome do remetente
        date: Data da mensagem
        text: Texto da mensagem
        media_files: Lista de arquivos de mídia
        is_forwarded: Se a mensagem foi encaminhada
        forwarded_from: Informações da mensagem original (se encaminhada)
        reply_to: ID da mensagem respondida (se for resposta)
        views: Número de visualizações (se disponível)
        is_edited: Se a mensagem foi editada
        edit_date: Data da edição (se editada)
    """
    
    id: int
    chat_id: int
    sender_id: int
    sender_name: str
    date: datetime
    text: Optional[str] = None
    media_files: List[MediaFile] = field(default_factory=list)
    is_forwarded: bool = False
    forwarded_from: Optional[Dict[str, Any]] = None
    reply_to: Optional[int] = None
    views: Optional[int] = None
    is_edited: bool = False
    edit_date: Optional[datetime] = None
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if not self.sender_name.strip():
            raise ValueError("Nome do remetente não pode estar vazio")
        
        if self.views is not None and self.views < 0:
            raise ValueError("Número de visualizações não pode ser negativo")
    
    @property
    def has_media(self) -> bool:
        """Se a mensagem contém mídia."""
        return len(self.media_files) > 0
    
    @property
    def media_count(self) -> int:
        """Número de arquivos de mídia."""
        return len(self.media_files)
    
    @property
    def total_size(self) -> int:
        """Tamanho total dos arquivos de mídia."""
        return sum(media.size for media in self.media_files)
    
    @property
    def total_size_formatted(self) -> str:
        """Tamanho total formatado."""
        if self.total_size < 1024:
            return f"{self.total_size} B"
        elif self.total_size < 1024 * 1024:
            return f"{self.total_size / 1024:.1f} KB"
        elif self.total_size < 1024 * 1024 * 1024:
            return f"{self.total_size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.total_size / (1024 * 1024 * 1024):.1f} GB"
    
    @property
    def downloaded_count(self) -> int:
        """Número de arquivos baixados."""
        return sum(1 for media in self.media_files if media.is_downloaded)
    
    @property
    def is_fully_downloaded(self) -> bool:
        """Se todos os arquivos foram baixados."""
        return self.has_media and self.downloaded_count == self.media_count
    
    def add_media_file(self, media_file: MediaFile):
        """Adiciona um arquivo de mídia à mensagem."""
        self.media_files.append(media_file)
        logger.debug(f"Arquivo de mídia adicionado à mensagem {self.id}: {media_file.filename}")
    
    def get_media_by_type(self, media_type: MediaType) -> List[MediaFile]:
        """Obtém arquivos de mídia por tipo."""
        return [media for media in self.media_files if media.type == media_type]
    
    def get_downloaded_media(self) -> List[MediaFile]:
        """Obtém apenas arquivos baixados."""
        return [media for media in self.media_files if media.is_downloaded]
    
    def get_pending_media(self) -> List[MediaFile]:
        """Obtém arquivos pendentes de download."""
        return [media for media in self.media_files if not media.is_downloaded]
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender_name,
            'date': self.date.isoformat(),
            'text': self.text,
            'media_files': [media.to_dict() for media in self.media_files],
            'is_forwarded': self.is_forwarded,
            'forwarded_from': self.forwarded_from,
            'reply_to': self.reply_to,
            'views': self.views,
            'is_edited': self.is_edited,
            'edit_date': self.edit_date.isoformat() if self.edit_date else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Cria instância a partir de dicionário."""
        date = datetime.fromisoformat(data['date'])
        
        media_files = [MediaFile.from_dict(media_data) for media_data in data.get('media_files', [])]
        
        edit_date = None
        if data.get('edit_date'):
            edit_date = datetime.fromisoformat(data['edit_date'])
        
        return cls(
            id=data['id'],
            chat_id=data['chat_id'],
            sender_id=data['sender_id'],
            sender_name=data['sender_name'],
            date=date,
            text=data.get('text'),
            media_files=media_files,
            is_forwarded=data.get('is_forwarded', False),
            forwarded_from=data.get('forwarded_from'),
            reply_to=data.get('reply_to'),
            views=data.get('views'),
            is_edited=data.get('is_edited', False),
            edit_date=edit_date
        )
    
    def __str__(self) -> str:
        """Representação string da mensagem."""
        media_info = f" [{self.media_count} mídias]" if self.has_media else ""
        status = "✅" if self.is_fully_downloaded else "⏳"
        return f"{status} {self.sender_name}: {self.text or 'Sem texto'}{media_info}"
    
    def __repr__(self) -> str:
        """Representação detalhada da mensagem."""
        return f"Message(id={self.id}, chat_id={self.chat_id}, sender='{self.sender_name}')"


@dataclass
class MessageList:
    """
    Lista de mensagens com funcionalidades de busca e filtro.
    
    Attributes:
        messages: Lista de mensagens
        total_count: Número total de mensagens
        last_updated: Data da última atualização
    """
    
    messages: List[Message] = field(default_factory=list)
    total_count: int = 0
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicialização pós-criação."""
        if self.total_count == 0:
            self.total_count = len(self.messages)
    
    def add_message(self, message: Message):
        """Adiciona uma mensagem à lista."""
        # Verificar se já existe
        existing = self.get_by_id(message.id)
        if existing:
            # Atualizar mensagem existente
            index = self.messages.index(existing)
            self.messages[index] = message
            logger.debug(f"Mensagem atualizada: {message.id}")
        else:
            # Adicionar nova mensagem
            self.messages.append(message)
            self.total_count += 1
            logger.debug(f"Mensagem adicionada: {message.id}")
        
        self.last_updated = datetime.now()
    
    def get_by_id(self, message_id: int) -> Optional[Message]:
        """Busca mensagem por ID."""
        for message in self.messages:
            if message.id == message_id:
                return message
        return None
    
    def filter_by_sender(self, sender_id: int) -> List[Message]:
        """Filtra mensagens por remetente."""
        return [msg for msg in self.messages if msg.sender_id == sender_id]
    
    def filter_by_date_range(self, from_date: datetime, to_date: datetime) -> List[Message]:
        """Filtra mensagens por intervalo de data."""
        return [
            msg for msg in self.messages 
            if from_date <= msg.date <= to_date
        ]
    
    def filter_with_media(self) -> List[Message]:
        """Filtra apenas mensagens com mídia."""
        return [msg for msg in self.messages if msg.has_media]
    
    def filter_downloaded(self) -> List[Message]:
        """Filtra apenas mensagens totalmente baixadas."""
        return [msg for msg in self.messages if msg.is_fully_downloaded]
    
    def filter_pending(self) -> List[Message]:
        """Filtra mensagens com downloads pendentes."""
        return [msg for msg in self.messages if msg.has_media and not msg.is_fully_downloaded]
    
    def search_text(self, query: str) -> List[Message]:
        """Busca mensagens por texto."""
        query = query.lower()
        results = []
        
        for msg in self.messages:
            if msg.text and query in msg.text.lower():
                results.append(msg)
        
        return results
    
    def sort_by_date(self, reverse: bool = False) -> List[Message]:
        """Ordena mensagens por data."""
        return sorted(self.messages, key=lambda x: x.date, reverse=reverse)
    
    def sort_by_media_count(self, reverse: bool = True) -> List[Message]:
        """Ordena mensagens por número de mídias."""
        return sorted(self.messages, key=lambda x: x.media_count, reverse=reverse)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtém estatísticas das mensagens."""
        total_messages = len(self.messages)
        messages_with_media = len(self.filter_with_media())
        downloaded_messages = len(self.filter_downloaded())
        pending_messages = len(self.filter_pending())
        
        total_media_files = sum(msg.media_count for msg in self.messages)
        downloaded_files = sum(msg.downloaded_count for msg in self.messages)
        total_size = sum(msg.total_size for msg in self.messages)
        
        return {
            'total_messages': total_messages,
            'messages_with_media': messages_with_media,
            'downloaded_messages': downloaded_messages,
            'pending_messages': pending_messages,
            'total_media_files': total_media_files,
            'downloaded_files': downloaded_files,
            'pending_files': total_media_files - downloaded_files,
            'total_size': total_size,
            'download_progress': (downloaded_files / total_media_files * 100) if total_media_files > 0 else 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'messages': [msg.to_dict() for msg in self.messages],
            'total_count': self.total_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'statistics': self.get_statistics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageList':
        """Cria instância a partir de dicionário."""
        messages = [Message.from_dict(msg_data) for msg_data in data.get('messages', [])]
        
        last_updated = None
        if data.get('last_updated'):
            last_updated = datetime.fromisoformat(data['last_updated'])
        
        return cls(
            messages=messages,
            total_count=data.get('total_count', len(messages)),
            last_updated=last_updated
        )
    
    def __len__(self) -> int:
        """Retorna o número de mensagens."""
        return len(self.messages)
    
    def __iter__(self):
        """Iterador sobre as mensagens."""
        return iter(self.messages) 