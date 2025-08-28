# 💪 Exercícios Práticos - Dominando os Conceitos

## 🎯 Como Usar Este Documento

Cada exercício tem **3 níveis de dificuldade**:
- 🟢 **Básico**: Aplicar conceito isoladamente  
- 🟡 **Intermediário**: Combinar conceitos
- 🔴 **Avançado**: Criar solução completa

**Metodologia de estudo:**
1. Leia o conceito no `STUDY_GUIDE.md`
2. Faça os exercícios na ordem
3. Compare sua solução com exemplos da template
4. Refatore usando padrões aprendidos

---

## 1. 🏗️ Exercícios de Arquitetura

### 🟢 Básico: Separação de Responsabilidades

**Problema:** Você tem esta função monolítica:
```python
def processar_vendas(dados_brutos):
    # Validação
    if not dados_brutos:
        raise ValueError("Dados vazios")
    
    # Processamento
    vendas_processadas = []
    for item in dados_brutos:
        vendas_processadas.append({
            'produto': item['nome'],
            'valor': item['preco'] * item['quantidade'],
            'categoria': item['tipo'].upper()
        })
    
    # Persistência
    with open('vendas.json', 'w') as f:
        json.dump(vendas_processadas, f)
    
    # Relatório
    total = sum(v['valor'] for v in vendas_processadas)
    print(f"Total de vendas: R$ {total:,.2f}")
    
    return vendas_processadas
```

**Exercício:** Refatore separando em camadas:
- `services/validation_service.py`
- `services/processing_service.py`  
- `services/storage_service.py`
- `services/report_service.py`

**Sua solução:**
```python
# Implemente aqui usando os padrões da template
```

### 🟡 Intermediário: Factory Pattern

**Problema:** Criar diferentes tipos de relatórios baseado em configuração.

**Exercício:** Implemente um factory que cria relatórios:
```python
class ReportFactory:
    @staticmethod
    def create_report(report_type: str, data: List[Dict]) -> 'BaseReport':
        # Sua implementação aqui
        pass

# Deve suportar:
pdf_report = ReportFactory.create_report('pdf', sales_data)
excel_report = ReportFactory.create_report('excel', sales_data)
web_report = ReportFactory.create_report('web', sales_data)
```

### 🔴 Avançado: Arquitetura Completa

**Problema:** Criar um sistema de notificações modular.

**Exercício:** Implemente:
```
notifications/
├── __init__.py
├── models.py          # Notification, User
├── providers/         # Email, SMS, Push
├── services/          # NotificationService
└── handlers/          # NotificationHandler
```

**Requisitos:**
- Suporte múltiplos provedores
- Factory para criar provedores
- Strategy pattern para escolher canal
- Observer pattern para eventos

---

## 2. 🔄 Exercícios de POO

### 🟢 Básico: Herança e Polimorfismo

**Exercício:** Complete a implementação:
```python
from abc import ABC, abstractmethod

class BaseChart(ABC):
    def __init__(self, title: str, data: List[Dict]):
        self.title = title
        self.data = data
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    def validate_data(self) -> bool:
        # Implementação comum
        return len(self.data) > 0

class BarChart(BaseChart):
    # Sua implementação aqui
    pass

class LineChart(BaseChart):
    # Sua implementação aqui
    pass

# Teste
charts = [BarChart("Vendas", data), LineChart("Tendência", data)]
for chart in charts:
    if chart.validate_data():
        print(chart.render())
```

### 🟡 Intermediário: Composição

**Exercício:** Refatore esta herança múltipla usando composição:
```python
# ❌ Problemático
class DatabaseLogger(Database, Logger):
    pass

class FileLogger(File, Logger):
    pass

# ✅ Sua solução com composição
class LoggerService:
    # Implemente usando composição
    pass
```

### 🔴 Avançado: Sistema de Plugins

**Problema:** Criar sistema onde novos tipos de componentes podem ser adicionados dinamicamente.

**Exercício:** Implemente:
```python
class PluginRegistry:
    def register_plugin(self, plugin_type: str, plugin_class: Type):
        pass
    
    def create_component(self, plugin_type: str, **kwargs) -> 'BaseComponent':
        pass

# Uso
registry = PluginRegistry()
registry.register_plugin('chart', ChartPlugin)
registry.register_plugin('table', TablePlugin)

component = registry.create_component('chart', data=sales_data)
```

---

## 3. ⚡ Exercícios de Programação Assíncrona

### 🟢 Básico: async/await

**Exercício:** Converta estas funções síncronas para assíncronas:
```python
# ❌ Síncrono
def buscar_dados_api():
    import time
    time.sleep(2)  # Simula chamada HTTP
    return {"dados": "importantes"}

def processar_dados(dados):
    import time
    time.sleep(1)  # Simula processamento
    return dados["dados"].upper()

def salvar_resultado(resultado):
    import time
    time.sleep(0.5)  # Simula salvamento
    print(f"Salvo: {resultado}")

# Sua implementação assíncrona
async def main():
    # Implemente aqui
    pass
```

### 🟡 Intermediário: Concurrent Execution

**Exercício:** Execute múltiplas operações em paralelo:
```python
async def buscar_multiplas_apis():
    urls = [
        "https://api1.com/data",
        "https://api2.com/data", 
        "https://api3.com/data"
    ]
    
    # Sua implementação - buscar todas simultaneamente
    # Dica: use asyncio.gather()
    pass
```

### 🔴 Avançado: Rate Limiting e Retry

**Exercício:** Implemente um cliente HTTP com:
- Rate limiting (máx 10 requests/segundo)
- Retry automático em caso de erro
- Circuit breaker para APIs instáveis

```python
class APIClient:
    def __init__(self, max_requests_per_second: int = 10):
        # Sua implementação
        pass
    
    async def get(self, url: str, retries: int = 3) -> Dict:
        # Implementar rate limiting + retry + circuit breaker
        pass
```

---

## 4. 💾 Exercícios de Gerenciamento de Estado

### 🟢 Básico: State Manager

**Exercício:** Implemente um gerenciador de estado simples:
```python
class SimpleStateManager:
    def __init__(self):
        # Sua implementação
        pass
    
    def set_state(self, key: str, value: Any) -> None:
        pass
    
    def get_state(self, key: str, default: Any = None) -> Any:
        pass
    
    def clear_state(self) -> None:
        pass

# Teste
state = SimpleStateManager()
state.set_state('user', {'name': 'João'})
user = state.get_state('user')
assert user['name'] == 'João'
```

### 🟡 Intermediário: Thread-Safe State

**Exercício:** Torne o state manager thread-safe:
```python
import threading
from concurrent.futures import ThreadPoolExecutor

class ThreadSafeStateManager:
    def __init__(self):
        # Implemente com locks
        pass
    
    def set_state(self, key: str, value: Any) -> None:
        # Thread-safe implementation
        pass

# Teste
def worker(state, worker_id):
    for i in range(100):
        state.set_state(f'worker_{worker_id}_{i}', i)

state = ThreadSafeStateManager()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(worker, state, i) for i in range(5)]
```

### 🔴 Avançado: Distributed State

**Exercício:** Implemente state compartilhado entre múltiplos processos usando Redis:
```python
class DistributedStateManager:
    def __init__(self, redis_url: str):
        # Implementar usando Redis
        pass
    
    async def set_state(self, key: str, value: Any, ttl: int = None) -> None:
        # Serializar e salvar no Redis
        pass
    
    async def get_state(self, key: str, default: Any = None) -> Any:
        # Buscar e deserializar do Redis
        pass
    
    async def subscribe_to_changes(self, key_pattern: str, callback: Callable):
        # Implementar pub/sub para mudanças de estado
        pass
```

---

## 5. 🔌 Exercícios de Injeção de Dependência

### 🟢 Básico: Constructor Injection

**Exercício:** Refatore esta classe para usar DI:
```python
# ❌ Dependências hard-coded
class OrderService:
    def __init__(self):
        self.email_service = EmailService()
        self.payment_service = PaymentService()
        self.inventory_service = InventoryService()
    
    def process_order(self, order):
        # Lógica usando os serviços
        pass

# ✅ Sua implementação com DI
class OrderService:
    # Implemente aqui
    pass
```

### 🟡 Intermediário: Service Container

**Exercício:** Implemente um container de DI:
```python
class ServiceContainer:
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, interface: Type, implementation: Type, singleton: bool = False):
        # Sua implementação
        pass
    
    def resolve(self, interface: Type):
        # Resolver dependências automaticamente
        pass

# Uso
container = ServiceContainer()
container.register(IEmailService, EmailService, singleton=True)
container.register(IOrderService, OrderService)

order_service = container.resolve(IOrderService)
```

### 🔴 Avançado: Decorator-based DI

**Exercício:** Implemente DI usando decorators:
```python
@service(singleton=True)
class DatabaseService:
    pass

@service()
class UserService:
    def __init__(self, db: DatabaseService):
        self.db = db

@inject
def create_user(user_service: UserService, email: str):
    return user_service.create(email)

# O decorator deve injetar dependências automaticamente
```

---

## 6. 🎨 Exercícios de Design Patterns

### 🟢 Básico: Observer Pattern

**Exercício:** Implemente um sistema de eventos:
```python
class EventManager:
    def __init__(self):
        # Sua implementação
        pass
    
    def subscribe(self, event_type: str, callback: Callable):
        pass
    
    def emit(self, event_type: str, data: Any):
        pass

# Uso
events = EventManager()
events.subscribe('user_created', lambda user: print(f"Usuário criado: {user}"))
events.emit('user_created', {'name': 'João'})
```

### 🟡 Intermediário: Strategy Pattern

**Exercício:** Implemente diferentes algoritmos de ordenação:
```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class QuickSort(SortStrategy):
    # Sua implementação
    pass

class BubbleSort(SortStrategy):
    # Sua implementação
    pass

class Sorter:
    def __init__(self, strategy: SortStrategy):
        # Sua implementação
        pass
    
    def sort_data(self, data: List[int]) -> List[int]:
        # Usar strategy
        pass
```

### 🔴 Avançado: Command Pattern

**Exercício:** Implemente sistema de undo/redo:
```python
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class CreateUserCommand(Command):
    # Implementar comando que pode ser desfeito
    pass

class CommandHistory:
    def __init__(self):
        # Implementar pilha de comandos com undo/redo
        pass
    
    def execute_command(self, command: Command):
        pass
    
    def undo(self):
        pass
    
    def redo(self):
        pass
```

---

## 7. 🏷️ Exercícios de Type Hints

### 🟢 Básico: Tipos Básicos

**Exercício:** Adicione type hints completos:
```python
def calculate_discount(price, discount_percent, is_premium_user):
    if is_premium_user:
        discount_percent += 5
    
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    
    return {
        'original_price': price,
        'discount_amount': discount_amount,
        'final_price': final_price,
        'discount_percent': discount_percent
    }

# Sua versão com type hints
```

### 🟡 Intermediário: Generic Types

**Exercício:** Implemente um repositório genérico:
```python
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self):
        # Sua implementação
        pass
    
    def save(self, entity: T) -> T:
        pass
    
    def find_by_id(self, entity_id: str) -> Optional[T]:
        pass
    
    def find_all(self) -> List[T]:
        pass

# Uso
@dataclass
class User:
    id: str
    name: str

user_repo: Repository[User] = Repository()
user = user_repo.find_by_id("123")  # Tipo é Optional[User]
```

### 🔴 Avançado: Protocol Types

**Exercício:** Use protocols para duck typing:
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return f"Circle with radius {self.radius}"

class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Rectangle {self.width}x{self.height}"

def render_shape(shape: Drawable) -> str:
    # Type checker aceita qualquer objeto com método draw()
    return shape.draw()

# Funciona sem herança explícita!
shapes = [Circle(5), Rectangle(10, 20)]
for shape in shapes:
    print(render_shape(shape))
```

---

## 8. 🛠️ Exercícios de Refatoração

### 🟢 Básico: Extract Method

**Exercício:** Refatore extraindo métodos menores:
```python
def process_order(order_data):
    # Validação (20 linhas)
    if not order_data:
        raise ValueError("Order data is required")
    if 'customer_id' not in order_data:
        raise ValueError("Customer ID is required")
    if 'items' not in order_data or len(order_data['items']) == 0:
        raise ValueError("Order must have items")
    
    # Cálculo de preços (30 linhas)
    total = 0
    for item in order_data['items']:
        item_price = item['price'] * item['quantity']
        if item.get('discount'):
            item_price *= (1 - item['discount'] / 100)
        total += item_price
    
    # Aplicar impostos (15 linhas)
    tax_rate = 0.08
    if order_data.get('state') == 'CA':
        tax_rate = 0.1
    tax_amount = total * tax_rate
    final_total = total + tax_amount
    
    # Processar pagamento (25 linhas)
    payment_data = {
        'amount': final_total,
        'customer_id': order_data['customer_id'],
        'payment_method': order_data.get('payment_method', 'credit_card')
    }
    # ... lógica de pagamento
    
    return {'order_id': 'ORD123', 'total': final_total}

# Sua versão refatorada
class OrderProcessor:
    # Extraia métodos pequenos e focados
    pass
```

### 🟡 Intermediário: Replace Conditional with Polymorphism

**Exercício:** Substitua if/else por polimorfismo:
```python
def calculate_shipping(order, shipping_type):
    if shipping_type == 'standard':
        if order['weight'] < 1:
            return 5.99
        elif order['weight'] < 5:
            return 9.99
        else:
            return 15.99
    elif shipping_type == 'express':
        base_cost = 19.99
        if order['weight'] > 2:
            base_cost += (order['weight'] - 2) * 3
        return base_cost
    elif shipping_type == 'overnight':
        return 39.99 + order['weight'] * 5
    else:
        raise ValueError(f"Unknown shipping type: {shipping_type}")

# Sua implementação usando polimorfismo
```

### 🔴 Avançado: Migração Completa

**Exercício:** Pegue uma função do seu código atual (como `make_side_panel` do cockpit.py) e migre completamente para a arquitetura da template:

1. Identifique responsabilidades
2. Separe em serviços e componentes
3. Adicione type hints
4. Implemente error handling
5. Adicione testes

---

## 🧪 Exercícios de Testes

### 🟢 Básico: Unit Tests

**Exercício:** Escreva testes para esta classe:
```python
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
    
    def divide(self, a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Seus testes usando pytest
import pytest

def test_calculator_add():
    # Sua implementação
    pass

def test_calculator_divide():
    # Sua implementação  
    pass

def test_calculator_divide_by_zero():
    # Teste de erro
    pass
```

### 🟡 Intermediário: Mocking

**Exercício:** Teste esta classe que depende de API externa:
```python
class WeatherService:
    def __init__(self, api_client):
        self.api_client = api_client
    
    async def get_temperature(self, city: str) -> float:
        response = await self.api_client.get(f"/weather/{city}")
        return response['temperature']

# Teste usando mocks
async def test_weather_service():
    # Mock do api_client
    # Teste do comportamento
    pass
```

### 🔴 Avançado: Integration Tests

**Exercício:** Teste toda a stack da aplicação Wave:
```python
async def test_dashboard_page_integration():
    # Configurar aplicação de teste
    # Simular ações do usuário
    # Verificar state management
    # Validar UI renderizada
    pass
```

---

## 🎯 Projeto Final: Mini-Aplicação Completa

**Desafio:** Crie uma aplicação de gerenciamento de tarefas usando TODOS os conceitos:

### Requisitos:
1. **Autenticação** (login/logout)
2. **CRUD de tarefas** (criar, ler, atualizar, deletar)
3. **Filtros e busca**
4. **Dashboard com estatísticas**
5. **Notificações em tempo real**
6. **Temas configuráveis**

### Arquitetura obrigatória:
```
task_manager/
├── core/              # App principal, config, state
├── auth/              # Sistema de autenticação
├── models/            # Task, User, Category
├── services/          # TaskService, NotificationService
├── components/        # TaskCard, TaskList, Statistics
├── pages/             # Dashboard, TasksPage, SettingsPage
└── tests/             # Testes unitários e integração
```

### Critérios de avaliação:
- ✅ Separação clara de responsabilidades
- ✅ Type hints em todo código
- ✅ Error handling robusto
- ✅ Testes com >80% coverage
- ✅ Documentação completa
- ✅ Código limpo e legível

---

## 🏆 Checklist de Domínio

Marque conforme for dominando cada conceito:

### Arquitetura
- [ ] Posso explicar layered architecture
- [ ] Sei implementar dependency injection
- [ ] Entendo quando usar cada design pattern
- [ ] Consigo separar responsabilidades claramente

### POO
- [ ] Uso herança apropriadamente (não excessivamente)
- [ ] Prefiro composição sobre herança
- [ ] Implemento interfaces/protocolos corretamente
- [ ] Aplico encapsulamento efetivamente

### Async
- [ ] Entendo diferença entre sync/async
- [ ] Uso async/await corretamente
- [ ] Sei lidar com concorrência e locks
- [ ] Implemento error handling em código assíncrono

### Estado
- [ ] Gerencio estado de forma centralizada
- [ ] Entendo diferença entre local/global state
- [ ] Implemento state tracking
- [ ] Lido com state em ambiente concorrente

### Qualidade
- [ ] Escrevo código com type hints
- [ ] Sigo padrões de nomenclatura
- [ ] Implemento error handling completo
- [ ] Escrevo testes para meu código

**Quando marcar todos:** Você domina a metodologia! 🎉

---

## 🚀 Próximos Passos

1. **Escolha 1 conceito** que mais te intriga
2. **Faça os exercícios** desse conceito
3. **Aplique no seu código** atual
4. **Compare** com a implementação da template
5. **Refatore** usando os padrões aprendidos
6. **Repita** para o próximo conceito

**Lembre-se:** O objetivo é **dominar**, não apenas copiar! 💪
