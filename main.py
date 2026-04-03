import os
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

from database import init_database
from bot import (
    start, help_cmd, balance_cmd, status_cmd, expenses,
    fixed_cmd, removefixed_cmd, installments_cmd, removep_cmd,
    invoice_cmd, pay_invoice_cmd, remove_cmd, handle
)

TOKEN = os.getenv("BOT_TOKEN")


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set in environment variables")

    init_database()

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("inicio", start))
    app.add_handler(CommandHandler("ajuda", help_cmd))
    app.add_handler(CommandHandler("saldo", balance_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("gastos", expenses))
    
    # Fixed expenses
    app.add_handler(CommandHandler("fixos", fixed_cmd))
    app.add_handler(CommandHandler("removerfixo", removefixed_cmd))
    
    # Installments
    app.add_handler(CommandHandler("parcelados", installments_cmd))
    app.add_handler(CommandHandler("removep", removep_cmd))
    
    # Fatura (Credit card)
    app.add_handler(CommandHandler("fatura", invoice_cmd))
    app.add_handler(CommandHandler("pagar", pay_invoice_cmd))
    
    # Remove
    app.add_handler(CommandHandler("remover", remove_cmd))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🚀 Bot rodando...")

    app.run_polling()


if __name__ == "__main__":
    main()