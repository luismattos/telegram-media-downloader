"""
Sistema de logging unificado para o Telegram Media Downloader.

Este módulo fornece uma configuração centralizada de logging que pode ser
usada por todos os componentes do projeto.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    name: str,
    log_dir: str = "logs",
    level: int = logging.INFO,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG
) -> logging.Logger:
    """
    Configura um logger com handlers para console e arquivo.
    
    Args:
        name: Nome do logger (geralmente __name__)
        log_dir: Diretório onde salvar os logs
        level: Nível geral do logger
        console_level: Nível para output no console
        file_level: Nível para output no arquivo
        
    Returns:
        Logger configurado com handlers
    """
    # Criar diretório de logs se não existir
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Obter logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Limpar handlers existentes para evitar duplicação
    logger.handlers.clear()
    
    # Formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    module_name = name.split('.')[-1] if '.' in name else name
    log_filename = f"{module_name}_{timestamp}.log"
    file_handler = logging.FileHandler(
        log_path / log_filename, 
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger já configurado ou cria um novo.
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Se o logger já tem handlers, retorna como está
    if logger.handlers:
        return logger
    
    # Caso contrário, configura um novo
    return setup_logging(name)


class LoggerMixin:
    """
    Mixin para adicionar funcionalidade de logging a classes.
    
    Usage:
        class MyClass(LoggerMixin):
            def __init__(self):
                super().__init__()
                self.logger.info("Classe inicializada")
    """
    
    def __init__(self, logger_name: Optional[str] = None):
        """
        Inicializa o mixin de logging.
        
        Args:
            logger_name: Nome do logger. Se None, usa o nome da classe
        """
        if logger_name is None:
            logger_name = self.__class__.__module__ + '.' + self.__class__.__name__
        
        self.logger = get_logger(logger_name)
    
    def log_success(self, message: str):
        """Log de sucesso com emoji."""
        self.logger.info(f"✅ {message}")
    
    def log_error(self, message: str):
        """Log de erro com emoji."""
        self.logger.error(f"❌ {message}")
    
    def log_info(self, message: str):
        """Log de informação com emoji."""
        self.logger.info(f"ℹ️ {message}")
    
    def log_warning(self, message: str):
        """Log de aviso com emoji."""
        self.logger.warning(f"⚠️ {message}")
    
    def log_debug(self, message: str):
        """Log de debug."""
        self.logger.debug(f"🔍 {message}")


# Logger padrão para o módulo
logger = get_logger(__name__) 