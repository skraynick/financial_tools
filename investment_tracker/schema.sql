CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    base_currency TEXT NOT NULL DEFAULT 'CAD',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS securities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT,
    country TEXT,
    currency TEXT NOT NULL DEFAULT 'CAD',
    asset_type TEXT NOT NULL DEFAULT 'Stock',
    notes TEXT,

    UNIQUE(symbol, exchange)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    security_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,

    quantity REAL NOT NULL DEFAULT 0,
    price REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL,

    commission REAL NOT NULL DEFAULT 0,
    notes TEXT,

    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    FOREIGN KEY (security_id) REFERENCES securities(id)
);

CREATE TABLE IF NOT EXISTS dividends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    security_id INTEGER NOT NULL,
    dividend_date TEXT NOT NULL,

    shares REAL NOT NULL,
    dividend_per_share REAL NOT NULL,

    gross_amount REAL NOT NULL,
    foreign_tax REAL NOT NULL DEFAULT 0,
    other_tax REAL NOT NULL DEFAULT 0,
    net_amount REAL NOT NULL,

    currency TEXT NOT NULL,
    notes TEXT,

    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    FOREIGN KEY (security_id) REFERENCES securities(id)
);

CREATE TABLE IF NOT EXISTS cash_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,

    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,

    notes TEXT,

    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);

CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    security_id INTEGER NOT NULL,
    price_date TEXT NOT NULL,

    price REAL NOT NULL,
    currency TEXT NOT NULL,

    FOREIGN KEY (security_id) REFERENCES securities(id),

    UNIQUE(security_id, price_date)
);
