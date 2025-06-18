"""
Sistema de configuração centralizado para o Telegram Media Downloader.

Este módulo gerencia todas as configurações do projeto, incluindo
variáveis de ambiente, configurações padrão e validações.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .logging import get_logger

logger = get_logger(__name__)


class Config:
    """
    Classe centralizada para gerenciar configurações do projeto.
    
    Attributes:
        api_id: ID da API do Telegram
        api_hash: Hash da API do Telegram
        download_path: Caminho para downloads
        log_dir: Diretório para logs
        session_name: Nome do arquivo de sessão
    """
    
    def __init__(self):
        """Inicializa a configuração carregando variáveis de ambiente."""
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Configurações da API
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        
        # Configurações de diretórios
        self.download_path = self._get_download_path()
        self.log_dir = "logs"
        
        # Configurações de sessão
        self.session_name = "telegram_media_downloader_session"
        
        # Configurações de download
        self.default_limit = None
        self.retry_attempts = 3
        self.retry_delay = 5  # segundos
        
        logger.info("Configuração inicializada")
    
    def _get_download_path(self) -> Path:
        """
        Obtém o caminho de download configurado.
        
        Returns:
            Path do diretório de download
        """
        env_path = os.getenv('TELEGRAM_DOWNLOAD_PATH')
        
        if env_path:
            # Usar caminho configurado no ambiente
            path = Path(env_path).expanduser()
            logger.info(f"Usando caminho de download configurado: {path}")
        else:
            # Usar caminho padrão
            path = Path.cwd() / "downloads"
            logger.info(f"Usando caminho de download padrão: {path}")
        
        # Criar diretório se não existir
        path.mkdir(parents=True, exist_ok=True)
        
        return path
    
    def validate_api_credentials(self) -> bool:
        """
        Valida as credenciais da API.
        
        Returns:
            True se as credenciais são válidas, False caso contrário
        """
        if not self.api_id:
            logger.error("TELEGRAM_API_ID não configurado")
            return False
        
        if not self.api_hash:
            logger.error("TELEGRAM_API_HASH não configurado")
            return False
        
        if not self.api_id.isdigit():
            logger.error("TELEGRAM_API_ID deve ser um número")
            return False
        
        if len(self.api_hash) != 32:
            logger.error("TELEGRAM_API_HASH deve ter 32 caracteres")
            return False
        
        logger.info("Credenciais da API validadas com sucesso")
        return True
    
    def get_session_path(self) -> Path:
        """
        Obtém o caminho do arquivo de sessão.
        
        Returns:
            Path do arquivo de sessão
        """
        return Path(f"{self.session_name}.session")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a configuração para dicionário.
        
        Returns:
            Dicionário com as configurações
        """
        return {
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'download_path': str(self.download_path),
            'log_dir': self.log_dir,
            'session_name': self.session_name,
            'default_limit': self.default_limit,
            'retry_attempts': self.retry_attempts,
            'retry_delay': self.retry_delay
        }
    
    def __str__(self) -> str:
        """Representação string da configuração."""
        config_str = f"""
Configuração do Telegram Media Downloader:
- API ID: {'Configurado' if self.api_id else 'Não configurado'}
- API Hash: {'Configurado' if self.api_hash else 'Não configurado'}
- Download Path: {self.download_path}
- Log Directory: {self.log_dir}
- Session Name: {self.session_name}
- Default Limit: {self.default_limit or 'Sem limite'}
- Retry Attempts: {self.retry_attempts}
- Retry Delay: {self.retry_delay}s
"""
        return config_str.strip()


# Instância global da configuração
config = Config()


def get_config() -> Config:
    """
    Obtém a instância global da configuração.
    
    Returns:
        Instância da configuração
    """
    return config


def reload_config() -> Config:
    """
    Recarrega a configuração.
    
    Returns:
        Nova instância da configuração
    """
    global config
    config = Config()
    return config 