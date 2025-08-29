"""
DAZE Template - Products Page
Página de gestão de produtos com filtros e ações
"""

from h2o_wave import Q, ui
from pages.base import BasePage


class ProductsPage(BasePage):
    """
    Página de Produtos - gestão e filtros
    Demonstra CRUD e filtros complexos
    """
    
    def __init__(self, app=None):
        super().__init__(
            route='products',
            title='Produtos',
            app=app,
            icon='📦'
        )
        self.description = 'Gestão de produtos e inventário'
        self.data_service = app.data_service if app else None
    
    def setup_layout(self, q: Q, zones=None):
        """Layout específico da página de produtos"""
        if not zones:
            zones = [
                ui.zone('header', size='60px'),
                ui.zone('breadcrumb', size='40px'),
                ui.zone('content', direction='row', zones=[
                    ui.zone('filters', size='30%'),
                    ui.zone('main', size='70%', direction='column', zones=[
                        ui.zone('actions', size='80px'),
                        ui.zone('products_grid', size='calc(100% - 80px)')
                    ])
                ])
            ]
        
        q.page['meta'] = ui.meta_card(
            box='', 
            layouts=[ui.layout(breakpoint='xs', zones=zones)]
        )
    
    async def render(self, q: Q):
        """Renderiza a página de produtos"""
        self.setup_layout(q)
        
        # Card de filtros
        self._create_filters_card(q)
        
        # Card de ações
        self._create_actions_card(q)
        
        # Card de produtos
        await self._create_products_card(q)
        
        await q.page.save()
    
    def _create_filters_card(self, q: Q):
        """Cria card de filtros para produtos"""
        category = self.get_state(q, 'category_filter', 'all')
        min_stock = self.get_state(q, 'min_stock_filter', 0)
        max_price = self.get_state(q, 'max_price_filter', 10000)
        
        q.page['products_filters'] = ui.form_card(
            box='filters',
            title='🔍 Filtros de Produtos',
            items=[
                ui.separator('Categoria'),
                ui.dropdown(
                    name='category_filter',
                    label='Categoria',
                    value=category,
                    choices=[
                        ui.choice('all', 'Todas'),
                        ui.choice('electronics', 'Eletrônicos'),
                        ui.choice('clothing', 'Roupas'),
                        ui.choice('books', 'Livros'),
                        ui.choice('home', 'Casa e Jardim')
                    ]
                ),
                ui.separator('Estoque'),
                ui.spinbox(
                    name='min_stock_filter',
                    label='Estoque Mínimo',
                    value=min_stock,
                    min=0,
                    max=1000,
                    step=1
                ),
                ui.separator('Preço'),
                ui.spinbox(
                    name='max_price_filter',
                    label='Preço Máximo (R$)',
                    value=max_price,
                    min=0,
                    max=50000,
                    step=100
                ),
                ui.separator('Ações'),
                ui.button(
                    name='apply_product_filters',
                    label='📦 Filtrar Produtos',
                    primary=True
                ),
                ui.button(
                    name='reset_product_filters',
                    label='🔄 Limpar Filtros'
                ),
                ui.separator('Resumo'),
                ui.text(f'**Categoria:** {category}'),
                ui.text(f'**Estoque min:** {min_stock}'),
                ui.text(f'**Preço max:** R$ {max_price}'),
                ui.text(f'**Produtos encontrados:** {self.get_state(q, "products_count", "N/A")}')
            ]
        )
    
    def _create_actions_card(self, q: Q):
        """Cria card de ações para produtos"""
        q.page['products_actions'] = ui.form_card(
            box='actions',
            title='⚡ Ações',
            items=[
                ui.buttons([
                    ui.button('add_product', '➕ Novo Produto', primary=True),
                    ui.button('import_products', '📥 Importar CSV'),
                    ui.button('export_products', '📤 Exportar'),
                    ui.button('bulk_edit', '✏️ Edição em Lote')
                ])
            ]
        )
    
    async def _create_products_card(self, q: Q):
        """Cria card com grid de produtos"""
        # Aplica filtros
        category = self.get_state(q, 'category_filter', 'all')
        min_stock = self.get_state(q, 'min_stock_filter', 0)
        max_price = self.get_state(q, 'max_price_filter', 10000)
        
        try:
            if self.data_service:
                products_data = await self.data_service.get_sample_product_data(count=20)
                # Filtra dados baseado nos critérios
                filtered_products = self._filter_products(products_data, category, min_stock, max_price)
            else:
                # Dados de fallback
                filtered_products = self._get_fallback_products()
            
            # Atualiza contador
            self.set_state(q, 'products_count', len(filtered_products))
            
            # Cria tabela de produtos
            product_rows = []
            for i, product in enumerate(filtered_products):
                status_icon = '✅' if product['stock'] > 10 else '⚠️' if product['stock'] > 0 else '❌'
                product_rows.append(ui.table_row(
                    f'product_{i}',
                    [
                        product['name'],
                        product['category'],
                        f"R$ {product['price']:.2f}",
                        str(product['stock']),
                        f"{status_icon} {product['status']}"
                    ]
                ))
            
            q.page['products_grid'] = ui.form_card(
                box='products_grid',
                title=f'📦 Produtos ({len(filtered_products)} encontrados)',
                items=[
                    ui.table(
                        name='products_table',
                        columns=[
                            ui.table_column('name', 'Nome', width='200px'),
                            ui.table_column('category', 'Categoria', width='120px'),
                            ui.table_column('price', 'Preço', width='100px'),
                            ui.table_column('stock', 'Estoque', width='80px'),
                            ui.table_column('status', 'Status', width='120px')
                        ],
                        rows=product_rows,
                        height='400px',
                        multiple=True  # Permite seleção múltipla
                    )
                ]
            )
            
        except Exception as e:
            q.page['products_grid'] = ui.form_card(
                box='products_grid',
                title='📦 Produtos - Erro',
                items=[
                    ui.text(f'⚠️ Erro ao carregar produtos: {str(e)}'),
                    ui.button('retry_products', 'Tentar Novamente')
                ]
            )
    
    def _filter_products(self, products, category, min_stock, max_price):
        """Filtra produtos baseado nos critérios selecionados"""
        if not products:
            return self._get_fallback_products()
        
        filtered = []
        for product in products:
            # Aplica filtros
            if category != 'all' and product.get('category', '').lower() != category:
                continue
            if product.get('stock', 0) < min_stock:
                continue
            if product.get('price', 0) > max_price:
                continue
            
            filtered.append(product)
        
        return filtered
    
    def _get_fallback_products(self):
        """Retorna dados de fallback para produtos"""
        return [
            {'name': 'Notebook Dell', 'category': 'electronics', 'price': 2500.00, 'stock': 15, 'status': 'Ativo'},
            {'name': 'Camiseta Polo', 'category': 'clothing', 'price': 89.90, 'stock': 5, 'status': 'Baixo Estoque'},
            {'name': 'Livro Python', 'category': 'books', 'price': 45.00, 'stock': 0, 'status': 'Sem Estoque'},
            {'name': 'Mesa de Escritório', 'category': 'home', 'price': 350.00, 'stock': 8, 'status': 'Ativo'},
            {'name': 'Smartphone Samsung', 'category': 'electronics', 'price': 1200.00, 'stock': 25, 'status': 'Ativo'}
        ]
    
    async def handle_events(self, q: Q):
        """Processa eventos específicos da página de produtos"""
        if q.args.apply_product_filters:
            # Aplica filtros de produtos
            if q.args.category_filter:
                self.set_state(q, 'category_filter', q.args.category_filter)
            if q.args.min_stock_filter is not None:
                self.set_state(q, 'min_stock_filter', int(q.args.min_stock_filter))
            if q.args.max_price_filter is not None:
                self.set_state(q, 'max_price_filter', int(q.args.max_price_filter))
            
            # Re-renderiza produtos e filtros
            await self._create_products_card(q)
            self._create_filters_card(q)  # Atualiza contador
            
            await q.page.save()
            return True
        
        elif q.args.reset_product_filters:
            # Reseta filtros
            self.set_state(q, 'category_filter', 'all')
            self.set_state(q, 'min_stock_filter', 0)
            self.set_state(q, 'max_price_filter', 10000)
            
            await self._create_products_card(q)
            self._create_filters_card(q)
            
            await q.page.save()
            return True
        
        elif q.args.add_product:
            # Simula adição de produto
            # Em um app real, abriria um modal ou nova página
            await self._show_add_product_dialog(q)
            return True
        
        elif q.args.products_table:
            # Produto selecionado na tabela
            selected = q.args.products_table
            # Aqui poderia abrir detalhes do produto
            return True
        
        elif q.args.retry_products:
            await self._create_products_card(q)
            await q.page.save()
            return True
        
        # Chama o handler base
        return await super().handle_events(q)
    
    async def _show_add_product_dialog(self, q: Q):
        """Mostra dialog para adicionar produto (exemplo)"""
        q.page['add_product_dialog'] = ui.form_card(
            box='products_grid',
            title='➕ Novo Produto',
            items=[
                ui.textbox('new_product_name', 'Nome do Produto', placeholder='Digite o nome...'),
                ui.dropdown(
                    'new_product_category',
                    'Categoria',
                    choices=[
                        ui.choice('electronics', 'Eletrônicos'),
                        ui.choice('clothing', 'Roupas'),
                        ui.choice('books', 'Livros'),
                        ui.choice('home', 'Casa e Jardim')
                    ]
                ),
                ui.spinbox('new_product_price', 'Preço (R$)', min=0, max=10000, step=0.01),
                ui.spinbox('new_product_stock', 'Estoque', min=0, max=1000, step=1),
                ui.buttons([
                    ui.button('save_product', 'Salvar', primary=True),
                    ui.button('cancel_add_product', 'Cancelar')
                ])
            ]
        )
        await q.page.save()
