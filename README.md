# Financial Bot 🤖

Bot de Telegram para gerenciar finanças pessoais.

## Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar token:**
```bash
export BOT_TOKEN="seu_token_aqui"
```

## Uso

```bash
python main.py
```

## Comandos

- `/saldo` - Mostrar saldo
- `/status` - Status financeiro
- `/gastos` - Últimas transações
- `/fixos` - Gastos fixos
- `/parcelados` - Parcelamentos
- `/fatura` - Fatura do cartão
- `/ajuda` - Ajuda

## Transações

- `-50 lanche` - Gasto (débito)
- `+2000 salário` - Renda (entrada)
- `100 ifood c` - Cartão de crédito

## Estrutura

```
database/          # Modelos, repositórios, conexão
services/          # Lógica de negócio
bot.py            # Handlers do Telegram
main.py           # Entrada da aplicação
messages.py       # Mensagens do usuário
```
