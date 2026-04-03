import uuid
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from database import (
    add_transaction, get_transactions, delete_transaction,
    get_balance, update_balance,
    add_fixo, get_fixos, delete_fixo,
    add_parcelado, get_parcelados, delete_parcelado,
    add_to_fatura, get_fatura_aberta, get_fatura_items, create_or_get_fatura,
    close_fatura, pay_fatura
)
from messages import MESSAGES


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["start"])


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["help"])


async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance = get_balance()
    await update.message.reply_text(
        MESSAGES["balance"].format(value=balance)
    )


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance = get_balance()
    invoice = get_fatura_aberta()
    invoice_total = invoice[4] if invoice else 0  # total is at index 4
    fixed_expenses = get_fixos()
    installments = get_parcelados()
    
    await update.message.reply_text(
        MESSAGES["status"].format(
            balance=balance,
            invoice=invoice_total,
            fixed_count=len(fixed_expenses),
            installments_count=len(installments)
        )
    )


async def expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transactions = get_transactions()

    if not transactions:
        await update.message.reply_text(MESSAGES["no_transactions"])
        return

    msg = MESSAGES["transactions_header"]

    for t in transactions[-10:]:
        msg += MESSAGES["transaction_item"].format(
            id=t[0][:4],
            category=t[3],
            value=t[2]
        ) + "\n"

    await update.message.reply_text(msg)


# Fixed Expenses
async def fixed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fixed_expenses = get_fixos()
    
    if not fixed_expenses:
        await update.message.reply_text(MESSAGES["no_fixed"])
        return
    
    msg = MESSAGES["fixed_header"]
    for f in fixed_expenses:
        msg += MESSAGES["fixed_item"].format(
            id=f[0][:4],
            category=f[2],
            value=f[1]
        ) + "\n"
    
    await update.message.reply_text(msg)


async def removefixed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /removerfixo [id]")
        return
    
    fixo_id = context.args[0]
    fixed_expenses = get_fixos()
    
    found = False
    for f in fixed_expenses:
        if f[0].startswith(fixo_id):
            delete_fixo(f[0])
            found = True
            break
    
    if found:
        await update.message.reply_text(MESSAGES["removed"].format(item="Fixo"))
    else:
        await update.message.reply_text(MESSAGES["not_found"])


# Installments
async def installments_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    installments = get_parcelados()
    
    if not installments:
        await update.message.reply_text(MESSAGES["no_installments"])
        return
    
    msg = MESSAGES["installments_header"]
    for p in installments:
        installment_value = p[1] / p[3]  # total / total_installments
        msg += MESSAGES["installment_item"].format(
            id=p[0][:4],
            category=p[2],
            paid=p[4],
            total=p[3],
            installment_value=installment_value
        ) + "\n"
    
    await update.message.reply_text(msg)


async def removep_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /removep [id]")
        return
    
    parcelado_id = context.args[0]
    installments = get_parcelados()
    
    found = False
    for p in installments:
        if p[0].startswith(parcelado_id):
            delete_parcelado(p[0])
            found = True
            break
    
    if found:
        await update.message.reply_text(MESSAGES["removed"].format(item="Parcelado"))
    else:
        await update.message.reply_text(MESSAGES["not_found"])


# Credit Card / Invoice
async def invoice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invoice = get_fatura_aberta()
    
    if not invoice:
        await update.message.reply_text(MESSAGES["no_invoice"])
        return
    
    invoice_id = invoice[0]
    items = get_fatura_items(invoice_id)
    
    msg = MESSAGES["invoice_header"]
    
    if not items:
        msg += "Vazio"
    else:
        for item in items:
            msg += MESSAGES["invoice_item"].format(
                category=item[3],
                value=item[2]
            ) + "\n"
    
    total = invoice[4]  # total is at index 4
    msg += MESSAGES["invoice_total"].format(total=total)
    
    await update.message.reply_text(msg)


async def pay_invoice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() != "fatura":
        await update.message.reply_text("❌ Use: /pagar fatura")
        return
    
    fatura = get_fatura_aberta()
    
    if not fatura:
        await update.message.reply_text(MESSAGES["no_invoice"])
        return
    
    fatura_total = fatura[4]
    balance = get_balance()
    
    if balance < fatura_total:
        await update.message.reply_text(f"❌ Saldo insuficiente! Saldo: R${balance:.2f} | Fatura: R${fatura_total:.2f}")
        return
    
    pay_fatura(fatura[0])
    update_balance(balance - fatura_total)
    
    await update.message.reply_text(MESSAGES["invoice_paid"])


async def remove_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /remover [id]")
        return
    
    txn_id = context.args[0]
    transactions = get_transactions()
    
    found = False
    for t in transactions:
        if t[0].startswith(txn_id):
            # Reverse transaction effect
            if t[1] == "debit":
                balance = get_balance()
                update_balance(balance + t[2])
            elif t[1] == "entry":
                balance = get_balance()
                update_balance(balance - t[2])
            
            delete_transaction(t[0])
            found = True
            break
    
    if found:
        await update.message.reply_text(MESSAGES["removed"].format(item="Transação"))
    else:
        await update.message.reply_text(MESSAGES["not_found"])


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().split()

    if len(text) < 2:
        await update.message.reply_text(MESSAGES["invalid_format"])
        return

    try:
        # Fixed expense: "fixo 300 ingles"
        if text[0] == "fixo":
            amount = float(text[1])
            category = text[2]
            
            fixed_id = str(uuid.uuid4())
            add_fixo(fixed_id, amount, category)
            
            await update.message.reply_text(
                MESSAGES["fixed_created"].format(
                    category=category,
                    value=amount,
                    id=fixed_id[:4]
                )
            )
            return

        # Installment: "parcelado 1200 notebook 12"
        if text[0] == "parcelado":
            if len(text) < 4:
                await update.message.reply_text("❌ Use: parcelado [valor] [categoria] [parcelas]")
                return
            
            amount = float(text[1])
            category = text[2]
            total_installments = int(text[3])
            
            installment_id = str(uuid.uuid4())
            add_parcelado(installment_id, amount, category, total_installments)
            
            await update.message.reply_text(
                MESSAGES["installment_created"].format(
                    category=category,
                    value=amount,
                    total_installments=total_installments,
                    id=installment_id[:4]
                )
            )
            return

        # Regular transactions
        first_char = text[0][0]
        
        # Income: "+2000 salario"
        if first_char == "+":
            amount = float(text[0][1:])
            category = text[1]
            
            txn_id = str(uuid.uuid4())
            date = datetime.now().strftime("%d/%m")
            
            balance = get_balance()
            update_balance(balance + amount)
            
            add_transaction(txn_id, "entry", amount, category, date)
            
            await update.message.reply_text(
                MESSAGES["expense_entry"].format(
                    category=category,
                    value=amount
                )
            )
            return

        # Debit or Credit: "-30 lanche" or "120 ifood c"
        amount = float(text[0].lstrip("-"))
        category = text[1]

        txn_type = "debit"
        if len(text) > 2 and text[2] == "c":
            txn_type = "credit"

        txn_id = str(uuid.uuid4())
        date = datetime.now().strftime("%d/%m")

        if txn_type == "debit":
            balance = get_balance()
            update_balance(balance - amount)
        else:  # credit
            # Add to invoice
            current_month = datetime.now().strftime("%m/%Y")
            invoice_id = create_or_get_fatura(current_month)
            add_to_fatura(invoice_id, txn_id, amount, category, date)

        add_transaction(txn_id, txn_type, amount, category, date)

        if txn_type == "credit":
            response = MESSAGES["expense_credit"].format(
                category=category,
                value=amount
            )
        else:
            response = MESSAGES["expense_debit"].format(
                category=category,
                value=amount
            )

        await update.message.reply_text(response)

    except (ValueError, IndexError):
        await update.message.reply_text(MESSAGES["invalid_format"])
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")