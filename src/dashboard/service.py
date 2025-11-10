from sqlalchemy.orm import Session
from src.transactions.repository import get_transactions_by_user
from src.bank_accounts.repository import get_bank_accounts_by_user

def get_dashboard_data(db: Session, user_id: int):
    transactions = get_transactions_by_user(db, user_id)
    bank_accounts = get_bank_accounts_by_user(db, user_id)

    total_balance = sum(account.balance for account in bank_accounts)
    total_spent = sum(transaction.amount for transaction in transactions if transaction.amount < 0)
    total_received = sum(transaction.amount for transaction in transactions if transaction.amount > 0)

    return {
        "total_balance": total_balance,
        "total_spent": total_spent,
        "total_received": total_received,
        "transactions": transactions,
        "bank_accounts": bank_accounts,
    }
