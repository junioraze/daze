"""
Validadores de dados.
"""

from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from datetime import datetime


class DataValidator:
    """Classe para validação de dados"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def clear_messages(self) -> None:
        """Limpa mensagens de erro e aviso"""
        self.errors.clear()
        self.warnings.clear()
    
    def add_error(self, message: str) -> None:
        """Adiciona mensagem de erro"""
        self.errors.append(message)
    
    def add_warning(self, message: str) -> None:
        """Adiciona mensagem de aviso"""
        self.warnings.append(message)
    
    def has_errors(self) -> bool:
        """Verifica se há erros"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Verifica se há avisos"""
        return len(self.warnings) > 0
    
    def validate_dataframe(self, df: pd.DataFrame, rules: Dict[str, Any]) -> bool:
        """Valida DataFrame com base em regras"""
        self.clear_messages()
        
        # Validar se DataFrame não está vazio
        if df.empty:
            self.add_error("DataFrame está vazio")
            return False
        
        # Validar colunas obrigatórias
        required_columns = rules.get('required_columns', [])
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.add_error(f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}")
        
        # Validar tipos de dados
        column_types = rules.get('column_types', {})
        for column, expected_type in column_types.items():
            if column in df.columns:
                if not self._validate_column_type(df[column], expected_type):
                    self.add_warning(f"Coluna '{column}' não está no tipo esperado: {expected_type}")
        
        # Validar valores únicos
        unique_columns = rules.get('unique_columns', [])
        for column in unique_columns:
            if column in df.columns:
                if df[column].duplicated().any():
                    self.add_error(f"Coluna '{column}' deve ter valores únicos")
        
        # Validar valores não nulos
        not_null_columns = rules.get('not_null_columns', [])
        for column in not_null_columns:
            if column in df.columns:
                if df[column].isnull().any():
                    null_count = df[column].isnull().sum()
                    self.add_error(f"Coluna '{column}' tem {null_count} valores nulos")
        
        # Validar ranges de valores
        value_ranges = rules.get('value_ranges', {})
        for column, (min_val, max_val) in value_ranges.items():
            if column in df.columns:
                numeric_data = pd.to_numeric(df[column], errors='coerce')
                if not numeric_data.isnull().all():
                    out_of_range = (numeric_data < min_val) | (numeric_data > max_val)
                    if out_of_range.any():
                        count = out_of_range.sum()
                        self.add_warning(f"Coluna '{column}' tem {count} valores fora do range [{min_val}, {max_val}]")
        
        return not self.has_errors()
    
    def _validate_column_type(self, series: pd.Series, expected_type: str) -> bool:
        """Valida tipo de uma coluna"""
        if expected_type == 'numeric':
            return pd.api.types.is_numeric_dtype(series)
        elif expected_type == 'string':
            return pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series)
        elif expected_type == 'datetime':
            return pd.api.types.is_datetime64_any_dtype(series)
        elif expected_type == 'boolean':
            return pd.api.types.is_bool_dtype(series)
        return True
    
    def validate_upload_file(self, file_path: str, allowed_extensions: List[str], 
                           max_size_mb: float = 100) -> bool:
        """Valida arquivo de upload"""
        self.clear_messages()
        
        # Validar extensão
        extension = file_path.split('.')[-1].lower()
        if extension not in [ext.lower() for ext in allowed_extensions]:
            self.add_error(f"Tipo de arquivo não permitido. Extensões aceitas: {', '.join(allowed_extensions)}")
        
        # Validar tamanho (simulado - em implementação real verificaria o arquivo)
        # Por enquanto só retorna True para extensão válida
        
        return not self.has_errors()
    
    def validate_business_rules(self, data: Dict[str, Any], rules: Dict[str, Any]) -> bool:
        """Valida regras de negócio customizadas"""
        self.clear_messages()
        
        # Exemplo de validações de negócio
        if 'min_age' in rules:
            age = data.get('age', 0)
            if age < rules['min_age']:
                self.add_error(f"Idade mínima é {rules['min_age']} anos")
        
        if 'required_fields' in rules:
            for field in rules['required_fields']:
                if field not in data or not data[field]:
                    self.add_error(f"Campo obrigatório: {field}")
        
        if 'email_validation' in rules and rules['email_validation']:
            email = data.get('email', '')
            if email and not self._validate_email_format(email):
                self.add_error("Formato de email inválido")
        
        return not self.has_errors()
    
    def _validate_email_format(self, email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Retorna resumo da validação"""
        return {
            'valid': not self.has_errors(),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy()
        }
    
    def suggest_data_fixes(self, df: pd.DataFrame) -> List[str]:
        """Sugere correções para problemas nos dados"""
        suggestions = []
        
        # Verificar valores nulos
        null_columns = df.columns[df.isnull().any()].tolist()
        if null_columns:
            suggestions.append(f"Considere preencher valores nulos nas colunas: {', '.join(null_columns)}")
        
        # Verificar duplicatas
        if df.duplicated().any():
            duplicate_count = df.duplicated().sum()
            suggestions.append(f"Remover {duplicate_count} linhas duplicadas")
        
        # Verificar colunas com apenas um valor
        single_value_columns = [col for col in df.columns if df[col].nunique() <= 1]
        if single_value_columns:
            suggestions.append(f"Colunas com valor único podem ser removidas: {', '.join(single_value_columns)}")
        
        # Verificar tipos de dados
        object_columns = df.select_dtypes(include=['object']).columns
        for col in object_columns:
            if df[col].str.replace('.', '').str.replace(',', '').str.isdigit().all():
                suggestions.append(f"Coluna '{col}' parece ser numérica mas está como texto")
        
        return suggestions
