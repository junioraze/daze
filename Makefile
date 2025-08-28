# Makefile para desenvolvimento da Wave Template
# Facilita comandos comuns de desenvolvimento

.PHONY: help install dev test clean lint format run simple advanced

# Configurações
PYTHON = python
PIP = pip
VENV = venv

help: ## Mostra esta ajuda
	@echo "Wave Template - Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	$(PIP) install -r requirements.txt

dev-install: ## Instala dependências de desenvolvimento
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 mypy pytest

setup: ## Configura ambiente de desenvolvimento
	$(PYTHON) -m venv $(VENV)
	@echo "Ative o ambiente virtual com:"
	@echo "  source $(VENV)/bin/activate  (Linux/Mac)"
	@echo "  $(VENV)\\Scripts\\activate     (Windows)"

run: ## Executa aplicação principal
	$(PYTHON) app.py

simple: ## Executa exemplo simples
	$(PYTHON) simple_example.py

advanced: ## Executa exemplo avançado
	$(PYTHON) advanced_example.py

test: ## Executa testes
	$(PYTHON) -m pytest tests/ -v

lint: ## Verifica qualidade do código
	flake8 --max-line-length=100 core/ pages/ components/ services/ auth/ utils/
	mypy core/ pages/ components/ services/ auth/ utils/ --ignore-missing-imports

format: ## Formata código com Black
	black core/ pages/ components/ services/ auth/ utils/ *.py

clean: ## Limpa arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

docs: ## Gera documentação
	@echo "Documentação disponível em:"
	@echo "  README.md - Visão geral"
	@echo "  DEVELOPMENT.md - Guia de desenvolvimento"

create-page: ## Cria nova página (uso: make create-page NAME=MinhaPage)
	@if [ -z "$(NAME)" ]; then \
		echo "Uso: make create-page NAME=MinhaPage"; \
		exit 1; \
	fi
	@echo "Criando página $(NAME)..."
	@echo "from pages.base import BasePage\nfrom h2o_wave import Q, ui\n\nclass $(NAME)(BasePage):\n    def __init__(self, app):\n        super().__init__(app, '#$(shell echo $(NAME) | tr A-Z a-z)', '$(NAME)', 'Page')\n    \n    async def render(self, q: Q):\n        self.add_card(q, 'content', ui.form_card(\n            box='content',\n            items=[\n                ui.text_xl('$(NAME) Page'),\n                ui.text('Sua nova página aqui!')\n            ]\n        ))" > pages/$(shell echo $(NAME) | tr A-Z a-z).py
	@echo "Página criada em pages/$(shell echo $(NAME) | tr A-Z a-z).py"

create-component: ## Cria novo componente (uso: make create-component NAME=MeuComponente)
	@if [ -z "$(NAME)" ]; then \
		echo "Uso: make create-component NAME=MeuComponente"; \
		exit 1; \
	fi
	@echo "Criando componente $(NAME)..."
	@echo "from components.base import BaseComponent\nfrom h2o_wave import ui\n\nclass $(NAME)(BaseComponent):\n    def render(self, data=None):\n        return ui.form_card(\n            box='component',\n            items=[\n                ui.text('$(NAME) Component'),\n                ui.text(f'Data: {data}')\n            ]\n        )" > components/$(shell echo $(NAME) | tr A-Z a-z).py
	@echo "Componente criado em components/$(shell echo $(NAME) | tr A-Z a-z).py"

check: ## Verifica se tudo está funcionando
	@echo "🔍 Verificando Wave Template..."
	@$(PYTHON) -c "import h2o_wave; print('✅ H2O Wave instalado')"
	@$(PYTHON) -c "from core import WaveApp; print('✅ Core importado')"
	@$(PYTHON) -c "from auth import AuthManager; print('✅ Auth importado')"
	@$(PYTHON) -c "from pages import BasePage; print('✅ Pages importado')"
	@$(PYTHON) -c "from components import BaseComponent; print('✅ Components importado')"
	@echo "🎉 Tudo funcionando!"

info: ## Mostra informações do projeto
	@echo "📊 Wave Template - Informações:"
	@echo "  Nome: Wave Modular Template"
	@echo "  Versão: 1.0.0"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  H2O Wave: $(shell $(PYTHON) -c 'import h2o_wave; print(h2o_wave.__version__)' 2>/dev/null || echo 'Não instalado')"
	@echo "  Arquivos: $(shell find . -name '*.py' | wc -l) arquivos Python"
	@echo "  Linhas de código: $(shell find . -name '*.py' -exec cat {} \; | wc -l)"
