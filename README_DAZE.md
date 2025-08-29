# DAZE Template - README

## O que é?
O DAZE é um template modular para aplicações H2O Wave, que padroniza o ciclo de eventos, extração de argumentos e integração plugável com @on, facilitando a criação de apps robustos e escaláveis.

## Principais Recursos
- Ciclo modular App → Page → Card → Component
- Extração robusta de argumentos (Expando, dict, __kv)
- Fallback automático de evento (q.client.last_event)
- Integração plugável com @on
- Handlers plugáveis em todos os níveis

## Como começar
1. Crie seus componentes, cards e páginas herdando das bases DAZE.
2. Implemente apenas lógica de negócio nos métodos `render` e `handle_events`.
3. No app principal, registre eventos com `register_wave_event`.
4. Use sempre a API do core para extração de args e ciclo de eventos.

## Exemplo rápido
Veja `daze_echo_example.py` para um exemplo funcional.

## Documentação completa
Consulte o arquivo `DAZE_DOC.md` para detalhes de arquitetura, uso e melhores práticas.
