from sqlalchemy.orm import Session
from src.transactions.repository import get_transactions_by_user

# Define the logic for generating financial reports here
def generate_report(db: Session, user_id: int):
    transactions = get_transactions_by_user(db, user_id)

    total_spent = sum(transaction.amount for transaction in transactions if transaction.amount < 0)
    total_received = sum(transaction.amount for transaction in transactions if transaction.amount > 0)

    report = {
        "total_transactions": len(transactions),
        "total_spent": total_spent,
        "total_received": total_received,
        "transactions": transactions,
    }

    return report