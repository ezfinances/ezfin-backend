-- ============================================================================
-- MODELAGEM DO BANCO DE DADOS - EZFIN
-- ============================================================================
-- Sistema de Gestão Financeira Pessoal
-- Database: PostgreSQL 16
-- ============================================================================

-- ============================================================================
-- TABELA: USERS (Usuários)
-- ============================================================================
-- Armazena informações de autenticação e identificação dos usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                          -- Identificador único
    username VARCHAR(255) NOT NULL UNIQUE,          -- Nome de usuário (único)
    email VARCHAR(255) NOT NULL UNIQUE,             -- Email (único)
    hashed_password VARCHAR(255) NOT NULL,          -- Senha criptografada
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data de atualização
);

-- Índices para melhor performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);


-- ============================================================================
-- TABELA: BANK_ACCOUNTS (Contas Bancárias)
-- ============================================================================
-- Armazena as contas bancárias vinculadas a cada usuário
CREATE TABLE IF NOT EXISTS bank_accounts (
    id SERIAL PRIMARY KEY,                          -- Identificador único
    user_id INTEGER NOT NULL,                       -- FK para usuário proprietário
    account_name VARCHAR(255) NOT NULL,             -- Nome da conta (ex: "Conta Corrente")
    account_number VARCHAR(50) NOT NULL UNIQUE,    -- Número da conta (único)
    bank_name VARCHAR(255) NOT NULL,                -- Nome do banco (ex: "Banco do Brasil")
    account_type VARCHAR(50),                       -- Tipo de conta (corrente, poupança)
    status VARCHAR(50) DEFAULT 'active',            -- Status (active, inactive)
    balance NUMERIC(15, 2) DEFAULT 0.00,            -- Saldo atual
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de atualização
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para melhor performance
CREATE INDEX idx_bank_accounts_user_id ON bank_accounts(user_id);
CREATE INDEX idx_bank_accounts_account_number ON bank_accounts(account_number);


-- ============================================================================
-- TABELA: TRANSACTIONS (Transações)
-- ============================================================================
-- Registra todas as transações (receitas e despesas) do usuário
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,                          -- Identificador único
    user_id INTEGER NOT NULL,                       -- FK para usuário
    bank_account_id INTEGER,                        -- FK para conta bancária (opcional)
    amount NUMERIC(15, 2) NOT NULL,                 -- Valor da transação
    transaction_type VARCHAR(50) NOT NULL,          -- Tipo (income, expense, transfer)
    category VARCHAR(100),                          -- Categoria (salary, food, transport, etc)
    description VARCHAR(500),                       -- Descrição da transação
    timestamp TIMESTAMP NOT NULL,                   -- Data e hora da transação
    status VARCHAR(50) DEFAULT 'completed',         -- Status (completed, pending, cancelled)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação do registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de atualização
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id) ON DELETE SET NULL
);

-- Índices para melhor performance
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_bank_account_id ON transactions(bank_account_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX idx_transactions_category ON transactions(category);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);


-- ============================================================================
-- RELACIONAMENTOS
-- ============================================================================
-- 1:N - Um usuário possui múltiplas contas bancárias
--       users.id -> bank_accounts.user_id

-- 1:N - Um usuário possui múltiplas transações
--       users.id -> transactions.user_id

-- 1:N - Uma conta bancária possui múltiplas transações
--       bank_accounts.id -> transactions.bank_account_id


-- ============================================================================
-- TABELAS DE REFERÊNCIA (LOOKUP TABLES)
-- ============================================================================

-- Categorias de despesas
CREATE TABLE IF NOT EXISTS expense_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    icon VARCHAR(50)
);

-- Tipos de contas bancárias
CREATE TABLE IF NOT EXISTS account_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Bancos cadastrados
CREATE TABLE IF NOT EXISTS banks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(10) UNIQUE,
    country VARCHAR(100) DEFAULT 'Brazil'
);


-- ============================================================================
-- DADOS INICIAIS (SEEDS)
-- ============================================================================

-- Categorias de despesas padrão
INSERT INTO expense_categories (name, description, icon) VALUES
    ('Alimentação', 'Gastos com comida e bebida', '🍔'),
    ('Transporte', 'Gasolina, ônibus, metrô, táxi', '🚗'),
    ('Saúde', 'Farmácia, consultas, medicamentos', '🏥'),
    ('Educação', 'Cursos, livros, materiais escolares', '📚'),
    ('Lazer', 'Cinema, jogos, eventos', '🎮'),
    ('Moradia', 'Aluguel, condomínio, água, luz', '🏠'),
    ('Salário', 'Renda do trabalho', '💰'),
    ('Freelance', 'Trabalho autônomo', '💻'),
    ('Investimento', 'Aplicações, ações', '📈'),
    ('Outro', 'Outras categorias', '❓')
ON CONFLICT (name) DO NOTHING;

-- Tipos de contas bancárias
INSERT INTO account_types (name, description) VALUES
    ('Conta Corrente', 'Conta para transações do dia a dia'),
    ('Conta Poupança', 'Conta para economias e investimentos'),
    ('Conta Salário', 'Conta específica para recebimento de salário'),
    ('Conta Investimento', 'Conta para investimentos'),
    ('Carteira Digital', 'Carteira digital ou app de pagamento')
ON CONFLICT (name) DO NOTHING;

-- Principais bancos brasileiros
INSERT INTO banks (name, code, country) VALUES
    ('Banco do Brasil', '001', 'Brazil'),
    ('Caixa Econômica Federal', '104', 'Brazil'),
    ('Banco Santander', '033', 'Brazil'),
    ('Banco Bradesco', '237', 'Brazil'),
    ('Banco Itaú', '341', 'Brazil'),
    ('Banco Inter', '077', 'Brazil'),
    ('Nubank', 'nubank', 'Brazil'),
    ('Banco BTG Pactual', '030', 'Brazil'),
    ('Banco Sicredi', '748', 'Brazil'),
    ('Banco PagSeguro', 'pagseguro', 'Brazil')
ON CONFLICT (name) DO NOTHING;


-- ============================================================================
-- VIEWS ÚTEIS
-- ============================================================================

-- View: Resumo financeiro por usuário
CREATE OR REPLACE VIEW v_user_financial_summary AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(DISTINCT ba.id) as total_accounts,
    COUNT(DISTINCT t.id) as total_transactions,
    COALESCE(SUM(ba.balance), 0) as total_balance,
    COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expenses
FROM users u
LEFT JOIN bank_accounts ba ON u.id = ba.user_id
LEFT JOIN transactions t ON u.id = t.user_id
GROUP BY u.id, u.username, u.email;

-- View: Transações por categoria
CREATE OR REPLACE VIEW v_transactions_by_category AS
SELECT 
    user_id,
    category,
    transaction_type,
    COUNT(*) as quantity,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount
FROM transactions
GROUP BY user_id, category, transaction_type
ORDER BY user_id, total_amount DESC;

-- View: Saldo por conta bancária
CREATE OR REPLACE VIEW v_account_balances AS
SELECT 
    ba.id,
    ba.account_name,
    ba.bank_name,
    ba.account_type,
    ba.status,
    ba.balance,
    COUNT(t.id) as transaction_count,
    MAX(t.timestamp) as last_transaction
FROM bank_accounts ba
LEFT JOIN transactions t ON ba.id = t.bank_account_id
GROUP BY ba.id, ba.account_name, ba.bank_name, ba.account_type, ba.status, ba.balance;


-- ============================================================================
-- CONSTRAINTS E REGRAS DE NEGÓCIO
-- ============================================================================
-- 1. Um usuário pode ter múltiplas contas bancárias
-- 2. Uma transação é sempre vinculada a um usuário
-- 3. Uma transação pode estar vinculada a uma conta bancária (opcional)
-- 4. O saldo de uma conta é atualizado através de transações
-- 5. Transações deletadas cascateiam em relação ao usuário
-- 6. Usuários são únicos por email e username
-- 7. Contas bancárias são únicas por número (mesmo entre usuários)

-- ============================================================================
-- FIM DA MODELAGEM
-- ============================================================================
