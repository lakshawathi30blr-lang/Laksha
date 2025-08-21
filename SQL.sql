-- Table for User Profile
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Table for Accounts
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table for Assets (Stocks, Bonds, Crypto)
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    ticker_symbol VARCHAR(10) UNIQUE NOT NULL,
    asset_name VARCHAR(255) NOT NULL,
    asset_class VARCHAR(50) NOT NULL
);

-- Table for Transactions
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    asset_id INT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    shares DECIMAL(18, 8) NOT NULL,
    price_per_share DECIMAL(18, 8) NOT NULL,
    total_amount DECIMAL(18, 8) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- Insert a single user and account for the application
INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');
INSERT INTO accounts (user_id, account_name, account_type) VALUES (1, 'Main Brokerage', 'Brokerage');