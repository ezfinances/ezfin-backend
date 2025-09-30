import pytest
from ..main import app
from httpx import AsyncClient

# Dados de exemplo para usuário
USERNAME = "usuario_teste"
PASSWORD = "senha_teste"
HTTPS_USERS = "https://users"

# CREATE
@pytest.mark.asyncio
@pytest.mark.skip(reason="Teste de criação de usuário")
async def test_create_user():
    pass

# READ
@pytest.mark.asyncio
@pytest.mark.skip(reason="Teste de leitura de usuário")
async def test_read_user():
    pass

# UPDATE
@pytest.mark.asyncio
@pytest.mark.skip(reason="Teste de atualização de usuário")
async def test_update_user():
    pass