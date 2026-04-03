MESSAGES = {
    # Commands
    "start": "💰 Bot financeiro ativo\n\nEx:\n-30 lanche\n+2000 salario\n120 ifood c\nfixo 300 ingles\nparcelado 1200 notebook 12\n\nDigite /ajuda para mais info",

    # Balance & Status
    "balance": "💰 Saldo atual: R${value:.2f}",
    
    "status": "📊 STATUS FINANCEIRO\n\n💵 Saldo: R${balance:.2f}\n💳 Fatura aberta: R${invoice:.2f}\n🔄 Fixos ativos: {fixed_count}\n📦 Parcelados: {installments_count}",

    # Transactions
    "no_transactions": "Nenhum gasto registrado ainda.",

    "transactions_header": "🧾 Últimos gastos:\n\n",

    "transaction_item": "{id} | {category} | R${value}",

    "expense_debit": "✅ {category} - R${value}",

    "expense_credit": "💳 {category} - R${value} (crédito)",
    
    "expense_entry": "💵 Entrada: {category} + R${value}",

    "invalid_format": "❌ Formato inválido.\nExemplo: 50 mercado",

    # Fixed expenses
    "fixed_created": "✅ Fixo criado: {category} - R${value}/mês\nID: {id}",
    
    "fixed_header": "📌 Gastos fixos:\n\n",
    
    "fixed_item": "{id} | {category} | R${value}",
    
    "no_fixed": "Nenhum gasto fixo cadastrado.",

    # Installments
    "installment_created": "✅ Parcelado criado: {category} - R${value} em {total_installments}x\nID: {id}",
    
    "installments_header": "📦 Parcelados:\n\n",
    
    "installment_item": "{id} | {category} | {paid}/{total}x | R${installment_value}/mês",
    
    "no_installments": "Nenhum parcelado ativo.",

    # Invoice (Credit card)
    "invoice_header": "💳 FATURA ABERTA (Vence dia 12)\n\n",
    
    "invoice_item": "{category} | R${value}",
    
    "invoice_total": "\n📊 Total: R${total:.2f}",
    
    "no_invoice": "Nenhuma fatura aberta.",
    
    "invoice_paid": "✅ Fatura paga com sucesso!",

    # Removal
    "removed": "🗑️ {item} removido com sucesso!",
    
    "not_found": "❌ Item não encontrado.",

    # Help
    "help": """
        📖 AJUDA - Bot Financeiro

        📝 COMO USAR:

        💸 Gastos imediatos:
        -30 lanche (débito)
        +2000 salario (entrada)
        120 ifood c (crédito/fatura)

        📌 Gastos fixos (mensais):
        fixo 300 ingles
        /fixos
        /removerfixo [id]

        📦 Parcelados:
        parcelado 1200 notebook 12
        /parcelados
        /removep [id]

        💳 Cartão de crédito:
        /fatura (ver fatura aberta)
        /pagar fatura (quitar)

        📊 Consultas:
        /saldo
        /status
        /gastos
        /ajuda

        🗑️ Remover:
        /remover [id] (transação)
        /removerfixo [id]
        /removep [id]

        💡 Dica: IDs aparecem ao lado de cada item para fácil controle!
    """
}
