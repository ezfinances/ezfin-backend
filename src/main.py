from fastapi import FastAPI
from src.users.router import router as users_router
from src.bank_accounts.router import router as bank_accounts_router
from src.transactions.router import router as transactions_router
from src.dashboard.router import router as dashboard_router
from src.reports.router import router as reports_router

app = FastAPI()

app.include_router(users_router)
app.include_router(bank_accounts_router)
app.include_router(transactions_router)
app.include_router(dashboard_router)
app.include_router(reports_router)

@app.get("/")
def read_root():
    return {"msg": "Bem-vindo ao EzFin!"}

