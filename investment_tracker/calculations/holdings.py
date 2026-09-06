from collections import defaultdict

from database import get_connection


def get_holdings():
    """
    Calculate current holdings from BUY and SELL transactions.

    Returns a list containing one record per
    portfolio/security combination.
    """

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            t.portfolio_id,
            p.name AS portfolio_name,
            p.account_type,

            t.security_id,
            s.symbol,
            s.name AS security_name,
            s.currency AS security_currency,

            t.transaction_type,
            t.quantity,
            t.price,
            t.commission

        FROM transactions t

        JOIN portfolios p
            ON p.id = t.portfolio_id

        JOIN securities s
            ON s.id = t.security_id

        ORDER BY
            t.portfolio_id,
            t.security_id,
            t.transaction_date,
            t.id
        """
    ).fetchall()

    connection.close()

    holdings = defaultdict(
        lambda: {
            "shares": 0.0,
            "cost": 0.0,
        }
    )

    for row in rows:

        key = (
            row["portfolio_id"],
            row["security_id"],
        )

        quantity = float(row["quantity"])
        price = float(row["price"])
        commission = float(row["commission"])

        if row["transaction_type"] == "BUY":

            holdings[key]["shares"] += quantity

            holdings[key]["cost"] += (
                quantity * price
            ) + commission

        elif row["transaction_type"] == "SELL":

            current_shares = holdings[key]["shares"]
            current_cost = holdings[key]["cost"]

            if current_shares <= 0:
                continue

            # For now we use average cost.
            #
            # This is NOT yet our final Canadian
            # ACB implementation.
            average_cost = (
                current_cost / current_shares
            )

            holdings[key]["shares"] -= quantity

            holdings[key]["cost"] -= (
                average_cost * quantity
            )

    results = []

    for key, holding in holdings.items():

        portfolio_id, security_id = key

        if abs(holding["shares"]) < 0.000001:
            continue

        shares = holding["shares"]
        cost = holding["cost"]

        average_cost = cost / shares

        # Find identifying information again.
        connection = get_connection()

        row = connection.execute(
            """
            SELECT
                p.name AS portfolio_name,
                p.account_type,
                s.symbol,
                s.name AS security_name,
                s.currency AS security_currency
            FROM portfolios p
            JOIN securities s
            WHERE p.id = ?
              AND s.id = ?
            """,
            (
                portfolio_id,
                security_id,
            ),
        ).fetchone()

        connection.close()

        results.append(
            {
                "portfolio_id": portfolio_id,
                "portfolio_name": row["portfolio_name"],
                "account_type": row["account_type"],
                "security_id": security_id,
                "symbol": row["symbol"],
                "security_name": row["security_name"],
                "currency": row["security_currency"],
                "shares": shares,
                "cost": cost,
                "average_cost": average_cost,
            }
        )

    return results