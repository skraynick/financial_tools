import sqlite3
from pathlib import Path


DATABASE_FILE = Path(__file__).parent / "investments.db"
SCHEMA_FILE = Path(__file__).parent / "schema.sql"


def get_connection():
    """Return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create database tables if they don't already exist."""
    connection = get_connection()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


def get_portfolios():
    """Return all portfolios."""
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM portfolios
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return rows


def add_portfolio(name, account_type, base_currency="CAD", notes=""):
    """Add a new portfolio."""
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO portfolios (
            name,
            account_type,
            base_currency,
            notes
        )
        VALUES (?, ?, ?, ?)
        """,
        (name, account_type, base_currency, notes),
    )

    connection.commit()
    connection.close()


def get_securities():
    """Return all securities."""
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM securities
        ORDER BY symbol
        """
    ).fetchall()

    connection.close()

    return rows


def add_security(
    symbol,
    name,
    exchange,
    country,
    currency,
    asset_type="Stock",
    notes="",
):
    """Add a security."""
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO securities (
            symbol,
            name,
            exchange,
            country,
            currency,
            asset_type,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            symbol.upper(),
            name,
            exchange,
            country,
            currency,
            asset_type,
            notes,
        ),
    )

    connection.commit()
    connection.close()


def add_transaction(
    portfolio_id,
    security_id,
    transaction_date,
    transaction_type,
    quantity,
    price,
    currency,
    commission=0,
    notes="",
):
    """Add an investment transaction."""
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO transactions (
            portfolio_id,
            security_id,
            transaction_date,
            transaction_type,
            quantity,
            price,
            currency,
            commission,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            portfolio_id,
            security_id,
            transaction_date,
            transaction_type,
            quantity,
            price,
            currency,
            commission,
            notes,
        ),
    )

    connection.commit()
    connection.close()


def get_transactions():
    """Return transactions with portfolio and security names."""
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            t.id,
            t.transaction_date,
            p.name AS portfolio,
            s.symbol,
            s.name AS security,
            t.transaction_type,
            t.quantity,
            t.price,
            t.currency,
            t.commission,
            t.notes
        FROM transactions t
        JOIN portfolios p
            ON p.id = t.portfolio_id
        JOIN securities s
            ON s.id = t.security_id
        ORDER BY t.transaction_date DESC, t.id DESC
        """
    ).fetchall()

    connection.close()

    return rows
