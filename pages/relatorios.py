"""
Página de Relatórios - Exemplo de nova página no template DAZE
"""

from h2o_wave import Q, ui
from pages.base import BasePage
from typing import List
import random

class RelatoriosPage(BasePage):
    def __init__(self):
        super().__init__(route="relatorios", title="Relatórios")
    
    async def render(self, q: Q) -> None:
        """Renderiza a página de relatórios"""
        
        # 1. Setup do layout responsivo
        self.setup_responsive_layout(q, has_nav=True, has_sidebar=False)
        
        # 2. Header
        self.create_responsive_header(q, "📋 Relatórios")
        
        # 3. Navegação
        nav_items = [
            ui.nav_item(name='home', label='🏠 Home'),
            ui.nav_item(name='relatorios', label='📋 Relatórios'),
            ui.nav_item(name='config', label='⚙️ Config'),
        ]
        self.create_responsive_nav(q, nav_items)
        
        # 4. Conteúdo principal
        self.add_card(q, 'relatorios_content', ui.form_card(
            box='content',
            title='📊 Gerar Relatórios',
            items=[
                ui.text('**Selecione o tipo de relatório:**'),
                ui.separator(),
                
                # Opções de relatório
                ui.choice_group(
                    name='tipo_relatorio',
                    label='Tipo de Relatório',
                    value='vendas',
                    choices=[
                        ui.choice('vendas', 'Relatório de Vendas'),
                        ui.choice('usuarios', 'Relatório de Usuários'),
                        ui.choice('performance', 'Relatório de Performance'),
                    ]
                ),
                
                ui.separator(),
                
                # Período
                ui.date_picker(
                    name='data_inicio',
                    label='Data Início',
                    value='2024-01-01'
                ),
                
                ui.date_picker(
                    name='data_fim',
                    label='Data Fim',
                    value='2024-12-31'
                ),
                
                ui.separator(),
                
                # Botões de ação
                ui.buttons([
                    ui.button('gerar_relatorio', label='📊 Gerar Relatório', primary=True),
                    ui.button('baixar_modelo', label='📥 Baixar Modelo'),
                    ui.button('voltar_home', label='🏠 Voltar ao Home'),
                ])
            ]
        ))
    
    async def handle_events(self, q: Q) -> bool:
        """Trata eventos específicos da página de relatórios"""
        
        if q.args.gerar_relatorio:
            # Simular geração de relatório
            tipo = q.args.tipo_relatorio or 'vendas'
            self._mostrar_relatorio_gerado(q, tipo)
            return True
            
        if q.args.baixar_modelo:
            # self.show_notification(q, "Modelo baixado com sucesso!", "success")
            return True
            
        if q.args.voltar_home:
            # Deixa o handler principal tratar a navegação
            return False
            
        return False
    
    def _mostrar_relatorio_gerado(self, q: Q, tipo: str) -> None:
        """Mostra resultado do relatório gerado"""
        
        # Dados simulados baseados no tipo
        dados = {
            'vendas': {
                'total': f'R$ {random.randint(10000, 100000):,}',
                'items': random.randint(50, 500),
                'crescimento': f'{random.randint(5, 30)}%'
            },
            'usuarios': {
                'total': f'{random.randint(100, 1000)} usuários',
                'novos': f'{random.randint(10, 100)} novos',
                'ativos': f'{random.randint(50, 200)} ativos'
            },
            'performance': {
                'uptime': f'{random.randint(95, 99)}.{random.randint(1, 9)}%',
                'requests': f'{random.randint(1000, 10000):,}',
                'response_time': f'{random.randint(100, 500)}ms'
            }
        }
        
        dados_tipo = dados.get(tipo, dados['vendas'])
        
        # Atualizar card com resultado
        self.add_card(q, 'resultado_relatorio', ui.form_card(
            box='content',
            title=f'✅ Relatório de {tipo.title()} Gerado',
            items=[
                ui.text('**Resumo do Relatório:**'),
                ui.separator(),
                *[ui.text(f'• **{k.title()}:** {v}') for k, v in dados_tipo.items()],
                ui.separator(),
                ui.text('📅 **Gerado em:** ' + str(random.choice(['hoje', 'ontem', 'há 2 dias']))),
                ui.separator(),
                ui.buttons([
                    ui.button('download_pdf', label='📄 Download PDF', primary=True),
                    ui.button('download_excel', label='📊 Download Excel'),
                    ui.button('novo_relatorio', label='🔄 Novo Relatório'),
                ])
            ]
        ))
        
        # self.show_notification(q, f"Relatório de {tipo} gerado com sucesso!", "success")
