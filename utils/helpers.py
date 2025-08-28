"""
Funções auxiliares úteis.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Optional


def format_number(value: float, decimals: int = 2, locale: str = 'pt_BR') -> str:
    """Formata número para exibição"""
    try:
        if locale == 'pt_BR':
            if decimals == 0:
                return f"{int(value):,}".replace(',', '.')
            else:
                return f"{value:,.{decimals}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def format_currency(value: float, currency: str = 'BRL') -> str:
    """Formata valor monetário"""
    formatted_value = format_number(value, 2)
    
    if currency == 'BRL':
        return f"R$ {formatted_value}"
    elif currency == 'USD':
        return f"$ {value:,.2f}"
    elif currency == 'EUR':
        return f"€ {value:,.2f}"
    else:
        return f"{currency} {formatted_value}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Formata porcentagem"""
    try:
        return f"{value:.{decimals}f}%"
    except (ValueError, TypeError):
        return str(value)


def format_date(date_value: Any, format_string: str = '%d/%m/%Y') -> str:
    """Formata data para exibição"""
    try:
        if isinstance(date_value, str):
            # Tentar converter string para datetime
            try:
                date_obj = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_value, '%Y-%m-%d')
                except ValueError:
                    return date_value
        elif isinstance(date_value, datetime):
            date_obj = date_value
        else:
            return str(date_value)
        
        return date_obj.strftime(format_string)
    except Exception:
        return str(date_value)


def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Valida formato de telefone brasileiro"""
    # Remove caracteres não numéricos
    clean_phone = re.sub(r'\D', '', phone)
    
    # Verifica se tem 10 ou 11 dígitos
    return len(clean_phone) in [10, 11] and clean_phone.isdigit()


def validate_cpf(cpf: str) -> bool:
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    clean_cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(clean_cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if clean_cpf == clean_cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    sum1 = sum(int(clean_cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum1 * 10 % 11) % 10
    
    # Calcula segundo dígito verificador
    sum2 = sum(int(clean_cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum2 * 10 % 11) % 10
    
    return clean_cpf[-2:] == f"{digit1}{digit2}"


def generate_id(prefix: str = '', length: int = 8) -> str:
    """Gera ID único"""
    if prefix:
        return f"{prefix}_{uuid.uuid4().hex[:length]}"
    return uuid.uuid4().hex[:length]


def truncate_text(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """Trunca texto mantendo palavras inteiras"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - len(suffix)]
    # Encontrar último espaço para não cortar palavra
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + suffix


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divisão segura que evita divisão por zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def clean_string(text: str) -> str:
    """Limpa string removendo caracteres especiais"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove espaços extras
    text = ' '.join(text.split())
    
    # Remove caracteres de controle
    text = ''.join(char for char in text if ord(char) >= 32)
    
    return text.strip()


def parse_numeric(value: Any) -> Optional[float]:
    """Converte valor para número de forma segura"""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove caracteres não numéricos exceto ponto e vírgula
            clean_value = re.sub(r'[^\d.,-]', '', value)
            
            # Trata formato brasileiro (vírgula como decimal)
            if ',' in clean_value and '.' in clean_value:
                # Formato 1.234,56
                clean_value = clean_value.replace('.', '').replace(',', '.')
            elif ',' in clean_value:
                # Formato 1234,56
                clean_value = clean_value.replace(',', '.')
            
            return float(clean_value) if clean_value else None
        
        return None
    except (ValueError, TypeError):
        return None


def get_file_extension(filename: str) -> str:
    """Obtém extensão do arquivo"""
    return filename.split('.')[-1].lower() if '.' in filename else ''


def is_valid_file_type(filename: str, allowed_types: list) -> bool:
    """Verifica se tipo de arquivo é permitido"""
    extension = get_file_extension(filename)
    return extension in [ext.lower() for ext in allowed_types]
