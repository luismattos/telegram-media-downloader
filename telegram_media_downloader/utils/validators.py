"""
Sistema de validações para o Telegram Media Downloader.

Este módulo fornece funções de validação para entradas do usuário,
configurações e dados do sistema.
"""

import re
from pathlib import Path
from typing import Optional, List, Union
from datetime import datetime

from .logging import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Exceção para erros de validação."""
    pass


def validate_api_id(api_id: str) -> bool:
    """
    Valida o API ID do Telegram.
    
    Args:
        api_id: API ID para validar
        
    Returns:
        True se válido, False caso contrário
        
    Raises:
        ValidationError: Se o API ID for inválido
    """
    if not api_id:
        logger.error("API ID não pode estar vazio")
        raise ValidationError("API ID não pode estar vazio")
    
    if not api_id.isdigit():
        logger.error(f"API ID deve ser um número: recebido '{api_id}'")
        raise ValidationError("API ID deve ser um número")
    
    if len(api_id) < 5:
        logger.error(f"API ID deve ter pelo menos 5 dígitos: recebido '{api_id}'")
        raise ValidationError("API ID deve ter pelo menos 5 dígitos")
    
    logger.info(f"API ID validado com sucesso: {api_id}")
    return True


def validate_api_hash(api_hash: str) -> bool:
    """
    Valida o API Hash do Telegram.
    
    Args:
        api_hash: API Hash para validar
        
    Returns:
        True se válido, False caso contrário
        
    Raises:
        ValidationError: Se o API Hash for inválido
    """
    if not api_hash:
        logger.error("API Hash não pode estar vazio")
        raise ValidationError("API Hash não pode estar vazio")
    
    if len(api_hash) != 32:
        logger.error(f"API Hash deve ter exatamente 32 caracteres: recebido '{api_hash}'")
        raise ValidationError("API Hash deve ter exatamente 32 caracteres")
    
    # Verificar se contém apenas caracteres hexadecimais
    if not re.match(r'^[a-f0-9]{32}$', api_hash.lower()):
        logger.error(f"API Hash deve conter apenas caracteres hexadecimais: recebido '{api_hash}'")
        raise ValidationError("API Hash deve conter apenas caracteres hexadecimais")
    
    logger.info(f"API Hash validado com sucesso: {api_hash}")
    return True


def validate_download_path(path: Union[str, Path]) -> Path:
    """
    Valida e normaliza o caminho de download.
    
    Args:
        path: Caminho para validar
        
    Returns:
        Path normalizado
        
    Raises:
        ValidationError: Se o caminho for inválido
    """
    try:
        path_obj = Path(path).expanduser().resolve()
        
        # Verificar se é um diretório válido
        if path_obj.exists() and not path_obj.is_dir():
            raise ValidationError(f"O caminho {path} existe mas não é um diretório")
        
        # Criar diretório se não existir
        path_obj.mkdir(parents=True, exist_ok=True)
        
        return path_obj
        
    except Exception as e:
        raise ValidationError(f"Erro ao validar caminho {path}: {str(e)}")


def validate_chat_name(chat_name: str) -> bool:
    """
    Valida o nome do chat.
    
    Args:
        chat_name: Nome do chat para validar
        
    Returns:
        True se válido, False caso contrário
        
    Raises:
        ValidationError: Se o nome do chat for inválido
    """
    if not chat_name:
        logger.error("Nome do chat não pode estar vazio")
        raise ValidationError("Nome do chat não pode estar vazio")
    
    if len(chat_name.strip()) < 1:
        logger.error("Nome do chat não pode estar vazio (após strip)")
        raise ValidationError("Nome do chat não pode estar vazio")
    
    if len(chat_name) > 255:
        logger.error(f"Nome do chat muito longo (máximo 255 caracteres): recebido {len(chat_name)}")
        raise ValidationError("Nome do chat muito longo (máximo 255 caracteres)")
    
    logger.info(f"Nome do chat validado com sucesso: {chat_name}")
    return True


def validate_limit(limit: Optional[int]) -> Optional[int]:
    """
    Valida o limite de mensagens.
    
    Args:
        limit: Limite para validar
        
    Returns:
        Limite validado ou None
        
    Raises:
        ValidationError: Se o limite for inválido
    """
    if limit is None:
        return None
    
    if not isinstance(limit, int):
        raise ValidationError("Limite deve ser um número inteiro")
    
    if limit < 1:
        raise ValidationError("Limite deve ser maior que 0")
    
    if limit > 100000:
        raise ValidationError("Limite muito alto (máximo 100.000)")
    
    return limit


def validate_media_types(media_types: Optional[List[str]]) -> List[str]:
    """
    Valida os tipos de mídia.
    
    Args:
        media_types: Lista de tipos de mídia para validar
        
    Returns:
        Lista de tipos de mídia válidos
        
    Raises:
        ValidationError: Se os tipos de mídia forem inválidos
    """
    valid_types = {
        'photo', 'video', 'document', 'audio', 'voice', 'text'
    }
    
    if media_types is None:
        return list(valid_types)
    
    if not isinstance(media_types, list):
        raise ValidationError("Tipos de mídia devem ser uma lista")
    
    if not media_types:
        raise ValidationError("Lista de tipos de mídia não pode estar vazia")
    
    invalid_types = set(media_types) - valid_types
    if invalid_types:
        raise ValidationError(f"Tipos de mídia inválidos: {invalid_types}")
    
    return media_types


def validate_date_range(
    from_date: Optional[str], 
    to_date: Optional[str]
) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Valida um intervalo de datas.
    
    Args:
        from_date: Data inicial (YYYY-MM-DD)
        to_date: Data final (YYYY-MM-DD)
        
    Returns:
        Tupla com as datas validadas
        
    Raises:
        ValidationError: Se as datas forem inválidas
    """
    def parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(f"Data inválida: {date_str}. Use formato YYYY-MM-DD")
    
    from_dt = None
    to_dt = None
    
    if from_date:
        from_dt = parse_date(from_date)
    
    if to_date:
        to_dt = parse_date(to_date)
    
    if from_dt and to_dt and from_dt > to_dt:
        raise ValidationError("Data inicial não pode ser posterior à data final")
    
    return from_dt, to_dt


def validate_phone_number(phone: str) -> bool:
    """
    Valida um número de telefone.
    
    Args:
        phone: Número de telefone para validar
        
    Returns:
        True se válido, False caso contrário
        
    Raises:
        ValidationError: Se o número for inválido
    """
    if not phone:
        raise ValidationError("Número de telefone não pode estar vazio")
    
    # Remover espaços e caracteres especiais
    clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Verificar se contém apenas dígitos
    if not clean_phone.isdigit():
        raise ValidationError("Número de telefone deve conter apenas dígitos")
    
    # Verificar comprimento mínimo
    if len(clean_phone) < 8:
        raise ValidationError("Número de telefone muito curto")
    
    return True


def validate_session_file(session_path: Path) -> bool:
    """
    Valida se um arquivo de sessão existe e é válido.
    
    Args:
        session_path: Caminho do arquivo de sessão
        
    Returns:
        True se válido, False caso contrário
    """
    if not session_path.exists():
        return False
    
    if not session_path.is_file():
        return False
    
    # Verificar se o arquivo tem tamanho mínimo
    if session_path.stat().st_size < 100:
        return False
    
    return True


# Função utilitária para validar múltiplos campos
def validate_config(config_dict: dict) -> dict:
    """
    Valida um dicionário de configuração.
    
    Args:
        config_dict: Dicionário de configuração
        
    Returns:
        Dicionário validado
        
    Raises:
        ValidationError: Se alguma configuração for inválida
    """
    validated = {}
    
    # Validar API credentials
    if 'api_id' in config_dict:
        validate_api_id(config_dict['api_id'])
        validated['api_id'] = config_dict['api_id']
    
    if 'api_hash' in config_dict:
        validate_api_hash(config_dict['api_hash'])
        validated['api_hash'] = config_dict['api_hash']
    
    # Validar caminho de download
    if 'download_path' in config_dict:
        validated['download_path'] = validate_download_path(config_dict['download_path'])
    
    # Validar limite
    if 'limit' in config_dict:
        validated['limit'] = validate_limit(config_dict['limit'])
    
    # Validar tipos de mídia
    if 'media_types' in config_dict:
        validated['media_types'] = validate_media_types(config_dict['media_types'])
    
    return validated 