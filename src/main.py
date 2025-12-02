"""Arquivo principal"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.users.router import router as users_router
from src.bank_accounts.router import router as bank_accounts_router
from src.transactions.router import router as transactions_router
from src.dashboard.router import router as dashboard_router
from src.reports.router import router as reports_router
# Import all models to ensure they are registered with Base
# from src.users import model as users_model
# from src.bank_accounts import model as bank_accounts_model
# from src.transactions import model as transactions_model

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS para aceitar requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Desenvolvimento Local
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5000",
        # Docker
        "http://host.docker.internal:3000",
        "http://host.docker.internal:3001",
        "http://host.docker.internal:5000",
        "http://frontend:3000",
        "http://frontend:5000",
        # Produção - Fly.io
        "https://ezfin-frontend.fly.dev",
        "https://ezfin-backend.fly.dev",
        "http://ezfin-frontend.fly.dev",
        "http://ezfin-backend.fly.dev",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(users_router)
app.include_router(bank_accounts_router)
app.include_router(transactions_router)
app.include_router(dashboard_router)
app.include_router(reports_router)

@app.get("/")
def read_root():
    """Imprime uma mensagem no front pra mostrar que esta funcionando"""
    return {"msg": "Bem-vindo ao EzFin!"}
