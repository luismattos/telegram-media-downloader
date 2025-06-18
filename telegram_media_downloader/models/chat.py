"""
Modelo de dados para chats do Telegram.

Este módulo define as classes e estruturas de dados para representar
chats, canais e grupos do Telegram.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ChatType(Enum):
    """Tipos de chat disponíveis."""
    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    SUPERGROUP = "supergroup"
    BOT = "bot"


@dataclass
class Chat:
    """
    Representa um chat do Telegram.
    
    Attributes:
        id: ID único do chat
        title: Título/nome do chat
        username: Username do chat (se disponível)
        type: Tipo do chat
        is_verified: Se o chat é verificado
        is_scam: Se o chat é marcado como scam
        is_fake: Se o chat é marcado como fake
        members_count: Número de membros (se disponível)
        description: Descrição do chat
        created_at: Data de criação (se disponível)
        last_activity: Última atividade conhecida
        download_count: Número de arquivos baixados
        last_download: Data do último download
    """
    
    id: int
    title: str
    type: ChatType
    username: Optional[str] = None
    is_verified: bool = False
    is_scam: bool = False
    is_fake: bool = False
    members_count: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    download_count: int = 0
    last_download: Optional[datetime] = None
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if not self.title.strip():
            raise ValueError("Título do chat não pode estar vazio")
        
        if self.members_count is not None and self.members_count < 0:
            raise ValueError("Número de membros não pode ser negativo")
    
    @property
    def display_name(self) -> str:
        """Nome de exibição do chat."""
        if self.username:
            return f"{self.title} (@{self.username})"
        return self.title
    
    @property
    def is_public(self) -> bool:
        """Se o chat é público (tem username)."""
        return self.username is not None
    
    @property
    def is_group_or_channel(self) -> bool:
        """Se é um grupo ou canal."""
        return self.type in [ChatType.GROUP, ChatType.CHANNEL, ChatType.SUPERGROUP]
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'id': self.id,
            'title': self.title,
            'username': self.username,
            'type': self.type.value,
            'is_verified': self.is_verified,
            'is_scam': self.is_scam,
            'is_fake': self.is_fake,
            'members_count': self.members_count,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'download_count': self.download_count,
            'last_download': self.last_download.isoformat() if self.last_download else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        """Cria instância a partir de dicionário."""
        # Converter string de tipo para enum
        chat_type = ChatType(data.get('type', 'private'))
        
        # Converter strings de data para datetime
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'])
        
        last_activity = None
        if data.get('last_activity'):
            last_activity = datetime.fromisoformat(data['last_activity'])
        
        last_download = None
        if data.get('last_download'):
            last_download = datetime.fromisoformat(data['last_download'])
        
        return cls(
            id=data['id'],
            title=data['title'],
            type=chat_type,
            username=data.get('username'),
            is_verified=data.get('is_verified', False),
            is_scam=data.get('is_scam', False),
            is_fake=data.get('is_fake', False),
            members_count=data.get('members_count'),
            description=data.get('description'),
            created_at=created_at,
            last_activity=last_activity,
            download_count=data.get('download_count', 0),
            last_download=last_download
        )
    
    def update_download_info(self, count: int = 1):
        """Atualiza informações de download."""
        self.download_count += count
        self.last_download = datetime.now()
        logger.debug(f"Atualizado download info para {self.title}: {count} arquivos")
    
    def __str__(self) -> str:
        """Representação string do chat."""
        return f"{self.display_name} ({self.type.value})"
    
    def __repr__(self) -> str:
        """Representação detalhada do chat."""
        return f"Chat(id={self.id}, title='{self.title}', type={self.type.value})"


@dataclass
class ChatList:
    """
    Lista de chats com funcionalidades de busca e filtro.
    
    Attributes:
        chats: Lista de chats
        total_count: Número total de chats
        last_updated: Data da última atualização
    """
    
    chats: List[Chat] = field(default_factory=list)
    total_count: int = 0
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicialização pós-criação."""
        if self.total_count == 0:
            self.total_count = len(self.chats)
    
    def add_chat(self, chat: Chat):
        """Adiciona um chat à lista."""
        # Verificar se já existe
        existing = self.get_by_id(chat.id)
        if existing:
            # Atualizar chat existente
            index = self.chats.index(existing)
            self.chats[index] = chat
            logger.debug(f"Chat atualizado: {chat.title}")
        else:
            # Adicionar novo chat
            self.chats.append(chat)
            self.total_count += 1
            logger.debug(f"Chat adicionado: {chat.title}")
        
        self.last_updated = datetime.now()
    
    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        """Busca chat por ID."""
        for chat in self.chats:
            if chat.id == chat_id:
                return chat
        return None
    
    def get_by_username(self, username: str) -> Optional[Chat]:
        """Busca chat por username."""
        for chat in self.chats:
            if chat.username == username:
                return chat
        return None
    
    def search_by_title(self, query: str) -> List[Chat]:
        """Busca chats por título."""
        query = query.lower()
        results = []
        
        for chat in self.chats:
            if query in chat.title.lower():
                results.append(chat)
        
        return results
    
    def filter_by_type(self, chat_type: ChatType) -> List[Chat]:
        """Filtra chats por tipo."""
        return [chat for chat in self.chats if chat.type == chat_type]
    
    def filter_public(self) -> List[Chat]:
        """Filtra apenas chats públicos."""
        return [chat for chat in self.chats if chat.is_public]
    
    def filter_verified(self) -> List[Chat]:
        """Filtra apenas chats verificados."""
        return [chat for chat in self.chats if chat.is_verified]
    
    def sort_by_title(self, reverse: bool = False) -> List[Chat]:
        """Ordena chats por título."""
        return sorted(self.chats, key=lambda x: x.title.lower(), reverse=reverse)
    
    def sort_by_members(self, reverse: bool = True) -> List[Chat]:
        """Ordena chats por número de membros."""
        return sorted(
            self.chats, 
            key=lambda x: x.members_count or 0, 
            reverse=reverse
        )
    
    def sort_by_download_count(self, reverse: bool = True) -> List[Chat]:
        """Ordena chats por número de downloads."""
        return sorted(
            self.chats, 
            key=lambda x: x.download_count, 
            reverse=reverse
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            'chats': [chat.to_dict() for chat in self.chats],
            'total_count': self.total_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatList':
        """Cria instância a partir de dicionário."""
        chats = [Chat.from_dict(chat_data) for chat_data in data.get('chats', [])]
        
        last_updated = None
        if data.get('last_updated'):
            last_updated = datetime.fromisoformat(data['last_updated'])
        
        return cls(
            chats=chats,
            total_count=data.get('total_count', len(chats)),
            last_updated=last_updated
        )
    
    def __len__(self) -> int:
        """Retorna o número de chats."""
        return len(self.chats)
    
    def __iter__(self):
        """Iterador sobre os chats."""
        return iter(self.chats) 