"""
Serviço de dados centralizado.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import asyncio
from datetime import datetime, timedelta
import random


class DataService:
    """Serviço centralizado para operações de dados"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._cache_timeout = 300  # 5 minutos
    
    async def get_cached_data(self, key: str) -> Optional[Any]:
        """Obtém dados do cache"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if (datetime.now() - timestamp).seconds < self._cache_timeout:
                return data
            else:
                del self._cache[key]
        return None
    
    async def set_cached_data(self, key: str, data: Any) -> None:
        """Armazena dados no cache"""
        self._cache[key] = (data, datetime.now())
    
    async def load_csv_data(self, file_path: str) -> pd.DataFrame:
        """Carrega dados de arquivo CSV"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Erro ao carregar CSV: {e}")
    
    async def load_excel_data(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """Carrega dados de arquivo Excel"""
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            raise ValueError(f"Erro ao carregar Excel: {e}")
    
    async def process_dataframe(self, df: pd.DataFrame, operations: List[Dict[str, Any]]) -> pd.DataFrame:
        """Processa DataFrame com lista de operações"""
        result_df = df.copy()
        
        for operation in operations:
            op_type = operation.get('type')
            
            if op_type == 'filter':
                column = operation.get('column')
                value = operation.get('value')
                operator = operation.get('operator', '==')
                
                if operator == '==':
                    result_df = result_df[result_df[column] == value]
                elif operator == '!=':
                    result_df = result_df[result_df[column] != value]
                elif operator == '>':
                    result_df = result_df[result_df[column] > value]
                elif operator == '<':
                    result_df = result_df[result_df[column] < value]
                elif operator == '>=':
                    result_df = result_df[result_df[column] >= value]
                elif operator == '<=':
                    result_df = result_df[result_df[column] <= value]
                elif operator == 'contains':
                    result_df = result_df[result_df[column].str.contains(str(value), na=False)]
            
            elif op_type == 'sort':
                column = operation.get('column')
                ascending = operation.get('ascending', True)
                result_df = result_df.sort_values(by=column, ascending=ascending)
            
            elif op_type == 'group':
                columns = operation.get('columns')
                agg_func = operation.get('agg_func', 'sum')
                result_df = result_df.groupby(columns).agg(agg_func).reset_index()
            
            elif op_type == 'rename':
                columns = operation.get('columns')
                result_df = result_df.rename(columns=columns)
        
        return result_df
    
    async def get_sample_sales_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Gera dados de vendas de exemplo"""
        cache_key = f"sales_data_{days}"
        cached_data = await self.get_cached_data(cache_key)
        
        if cached_data:
            return cached_data
        
        base_date = datetime.now() - timedelta(days=days)
        data = []
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'vendas': random.randint(1000, 5000),
                'usuarios': random.randint(100, 800),
                'pedidos': random.randint(20, 150),
                'receita': random.randint(10000, 80000)
            })
        
        await self.set_cached_data(cache_key, data)
        return data
    
    async def get_sample_product_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """Gera dados de produtos de exemplo"""
        cache_key = f"product_data_{count}"
        cached_data = await self.get_cached_data(cache_key)
        
        if cached_data:
            return cached_data
        
        categorias = ['Eletrônicos', 'Roupas', 'Casa', 'Esporte', 'Livros']
        status_options = ['Ativo', 'Inativo', 'Pendente', 'Descontinuado']
        
        data = []
        for i in range(count):
            data.append({
                'produto': f'Produto {chr(65 + i)}',
                'categoria': random.choice(categorias),
                'preco': round(random.uniform(10.0, 500.0), 2),
                'estoque': random.randint(0, 100),
                'vendas': random.randint(0, 1000),
                'receita': random.randint(1000, 50000),
                'status': random.choice(status_options),
                'rating': round(random.uniform(1.0, 5.0), 1)
            })
        
        await self.set_cached_data(cache_key, data)
        return data
    
    async def get_sample_user_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """Gera dados de usuários de exemplo"""
        cache_key = f"user_data_{count}"
        cached_data = await self.get_cached_data(cache_key)
        
        if cached_data:
            return cached_data
        
        cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília', 'Porto Alegre']
        estados = ['SP', 'RJ', 'MG', 'DF', 'RS']
        
        data = []
        for i in range(count):
            cidade_idx = random.randint(0, len(cidades) - 1)
            data.append({
                'usuario_id': f'user_{i:03d}',
                'nome': f'Usuário {i + 1}',
                'email': f'usuario{i + 1}@email.com',
                'cidade': cidades[cidade_idx],
                'estado': estados[cidade_idx],
                'idade': random.randint(18, 70),
                'pedidos': random.randint(0, 50),
                'total_gasto': random.randint(0, 10000),
                'ultimo_acesso': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            })
        
        await self.set_cached_data(cache_key, data)
        return data
    
    async def calculate_statistics(self, data: List[Dict[str, Any]], 
                                 numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """Calcula estatísticas básicas para colunas numéricas"""
        if not data:
            return {}
        
        df = pd.DataFrame(data)
        stats = {}
        
        for column in numeric_columns:
            if column in df.columns:
                col_data = pd.to_numeric(df[column], errors='coerce').dropna()
                if not col_data.empty:
                    stats[column] = {
                        'mean': float(col_data.mean()),
                        'median': float(col_data.median()),
                        'std': float(col_data.std()),
                        'min': float(col_data.min()),
                        'max': float(col_data.max()),
                        'count': int(col_data.count())
                    }
        
        return stats
    
    async def get_data_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Retorna resumo dos dados"""
        if not data:
            return {'total_rows': 0, 'columns': []}
        
        df = pd.DataFrame(data)
        
        return {
            'total_rows': len(df),
            'columns': list(df.columns),
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict()
        }
    
    async def get_sample_user_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Gera dados de exemplo de usuários para relatórios
        Args:
            count: Número de usuários a gerar
        Returns:
            Lista de dicionários com dados de usuários
        """
        cache_key = f"user_data_{count}"
        cached_data = await self.get_cached_data(cache_key)
        
        if cached_data:
            return cached_data
        
        import random
        from datetime import datetime, timedelta
        
        users = []
        first_names = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos', 'Sofia', 'Miguel', 'Beatriz', 'Tiago', 'Lucia']
        last_names = ['Silva', 'Santos', 'Oliveira', 'Costa', 'Lima', 'Fernandes', 'Rocha', 'Alves', 'Pereira', 'Martins']
        roles = ['Admin', 'User', 'Manager', 'Viewer', 'Editor']
        departments = ['Vendas', 'Marketing', 'TI', 'RH', 'Financeiro']
        
        for i in range(count):
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f'{first} {last}'
            email = f'{first.lower()}.{last.lower()}{i+1}@company.com'
            
            users.append({
                'name': full_name,
                'email': email,
                'role': random.choice(roles),
                'department': random.choice(departments),
                'last_login': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'status': random.choice(['Ativo', 'Inativo']),
                'projects': random.randint(1, 8),
                'score': round(random.uniform(0, 100), 1)
            })
        
        await self.set_cached_data(cache_key, users)
        return users
