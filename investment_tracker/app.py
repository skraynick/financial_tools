import streamlit as st
from database import (
    initialize_database,
    get_portfolios,
    add_portfolio,
    get_securities,
    add_security,
    add_transaction,
    get_transactions,
)

from calculations.holdings import  get_holdings

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------

st.set_page_config(
    page_title="Investment Tracker",
    page_icon="📈",
    layout="wide",
)

initialize_database()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("Investment Tracker")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Portfolios",
        "Securities",
        "Transactions",
        "Holdings",
    ],
)


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

if page == "Dashboard":

    st.title("📈 Investment Dashboard")

    portfolios = get_portfolios()
    securities = get_securities()
    transactions = get_transactions()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Portfolios",
        len(portfolios),
    )

    col2.metric(
        "Securities",
        len(securities),
    )

    col3.metric(
        "Transactions",
        len(transactions),
    )

    st.divider()

    st.subheader("Portfolios")

    if portfolios:
        for portfolio in portfolios:
            st.write(
                f"**{portfolio['name']}** — "
                f"{portfolio['account_type']} — "
                f"{portfolio['base_currency']}"
            )
    else:
        st.info(
            "No portfolios yet. Go to Portfolios to create your first one."
        )


# ---------------------------------------------------------
# Portfolios
# ---------------------------------------------------------

elif page == "Portfolios":

    st.title("💼 Portfolios")

    st.subheader("Add Portfolio")

    with st.form("portfolio_form"):

        name = st.text_input(
            "Portfolio name",
            placeholder="Example: Long Term",
        )

        account_type = st.selectbox(
            "Account type",
            [
                "Non-registered",
                "TFSA",
                "RRSP",
                "RRIF",
                "FHSA",
                "Other",
            ],
        )

        base_currency = st.selectbox(
            "Base currency",
            [
                "CAD",
                "USD",
                "EUR",
                "GBP",
            ],
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Add Portfolio"
        )

        if submitted:

            if not name.strip():
                st.error("Please enter a portfolio name.")

            else:
                add_portfolio(
                    name=name.strip(),
                    account_type=account_type,
                    base_currency=base_currency,
                    notes=notes,
                )

                st.success(
                    f"Portfolio '{name}' added."
                )

                st.rerun()

    st.divider()

    st.subheader("Existing Portfolios")

    portfolios = get_portfolios()

    if portfolios:

        for portfolio in portfolios:

            st.write(
                f"### {portfolio['name']}"
            )

            st.write(
                f"Account: {portfolio['account_type']}  \n"
                f"Currency: {portfolio['base_currency']}"
            )

            if portfolio["notes"]:
                st.write(portfolio["notes"])

    else:
        st.info("No portfolios created yet.")


# ---------------------------------------------------------
# Holdings
# ---------------------------------------------------------

elif page == "Holdings":

    st.title("📊 Holdings")

    holdings = get_holdings()

    if not holdings:

        st.info(
            "No current holdings. "
            "Add some BUY transactions first."
        )

    else:

        import pandas as pd

        df = pd.DataFrame(holdings)

        display_df = df[
            [
                "portfolio_name",
                "account_type",
                "symbol",
                "security_name",
                "shares",
                "average_cost",
                "cost",
                "currency",
            ]
        ].copy()

        display_df.columns = [
            "Portfolio",
            "Account",
            "Symbol",
            "Security",
            "Shares",
            "Average Cost",
            "Cost Basis",
            "Currency",
        ]

        display_df["Shares"] = (
            display_df["Shares"]
            .round(4)
        )

        display_df["Average Cost"] = (
            display_df["Average Cost"]
            .round(4)
        )

        display_df["Cost Basis"] = (
            display_df["Cost Basis"]
            .round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # Summary by portfolio

        st.subheader("Portfolio Summary")

        summary = (
            df.groupby("portfolio_name")
            .agg(
                securities=("symbol", "count"),
                positions=("shares", "sum"),
                cost_basis=("cost", "sum"),
            )
            .reset_index()
        )

        summary.columns = [
            "Portfolio",
            "Securities",
            "Shares",
            "Cost Basis",
        ]

        summary["Cost Basis"] = (
            summary["Cost Basis"]
            .round(2)
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------
# Securities
# ---------------------------------------------------------

elif page == "Securities":

    st.title("📊 Securities")

    st.subheader("Add Security")

    with st.form("security_form"):

        symbol = st.text_input(
            "Symbol",
            placeholder="RY",
        )

        name = st.text_input(
            "Name",
            placeholder="Royal Bank of Canada",
        )

        exchange = st.text_input(
            "Exchange",
            placeholder="TSX",
        )

        country = st.text_input(
            "Country",
            placeholder="Canada",
        )

        currency = st.selectbox(
            "Currency",
            [
                "CAD",
                "USD",
                "GBP",
                "EUR",
                "AUD",
                "JPY",
                "Other",
            ],
        )

        asset_type = st.selectbox(
            "Asset type",
            [
                "Stock",
                "ETF",
                "REIT",
                "Bond",
                "Other",
            ],
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Add Security"
        )

        if submitted:

            if not symbol.strip():
                st.error("Please enter a symbol.")

            elif not name.strip():
                st.error("Please enter a security name.")

            else:

                try:

                    add_security(
                        symbol=symbol.strip(),
                        name=name.strip(),
                        exchange=exchange.strip(),
                        country=country.strip(),
                        currency=currency,
                        asset_type=asset_type,
                        notes=notes,
                    )

                    st.success(
                        f"{symbol.upper()} added."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not add security: {error}"
                    )

    st.divider()

    st.subheader("Existing Securities")

    securities = get_securities()

    if securities:

        for security in securities:

            st.write(
                f"**{security['symbol']}** — "
                f"{security['name']} "
                f"({security['exchange']}) — "
                f"{security['currency']}"
            )

    else:

        st.info(
            "No securities created yet."
        )


# ---------------------------------------------------------
# Transactions
# ---------------------------------------------------------

elif page == "Transactions":

    st.title("🧾 Transactions")

    portfolios = get_portfolios()
    securities = get_securities()

    if not portfolios:

        st.warning(
            "Create a portfolio before adding transactions."
        )

    elif not securities:

        st.warning(
            "Create at least one security before adding transactions."
        )

    else:

        st.subheader("Add Transaction")

        portfolio_options = {
            f"{p['name']} ({p['account_type']})": p["id"]
            for p in portfolios
        }

        security_options = {
            f"{s['symbol']} — {s['name']}": s["id"]
            for s in securities
        }

        with st.form("transaction_form"):

            portfolio_name = st.selectbox(
                "Portfolio",
                list(portfolio_options.keys()),
            )

            security_name = st.selectbox(
                "Security",
                list(security_options.keys()),
            )

            transaction_date = st.date_input(
                "Transaction date"
            )

            transaction_type = st.selectbox(
                "Transaction type",
                [
                    "BUY",
                    "SELL",
                ],
            )

            quantity = st.number_input(
                "Number of shares",
                min_value=1,
                step=1,
            )



            price = st.number_input(
                "Price per share",
                min_value=0.0,
                step=0.01,
            )

            currency = st.selectbox(
                "Currency",
                [
                    "CAD",
                    "USD",
                    "GBP",
                    "EUR",
                    "AUD",
                    "JPY",
                    "Other",
                ],
            )

            commission = st.number_input(
                "Commission / fees",
                min_value=0.0,
                step=0.01,
            )

            notes = st.text_area(
                "Notes"
            )

            submitted = st.form_submit_button(
                "Save Transaction"
            )

            if quantity <= 0:
                st.error("Number of shares must be at least 1.")

            else:
                add_transaction(
                    portfolio_id=portfolio_options[portfolio_name],
                    security_id=security_options[security_name],
                    transaction_date=str(transaction_date),
                    transaction_type=transaction_type,
                    quantity=quantity,
                    price=price,
                    currency=currency,
                    commission=commission,
                    notes=notes,
                )

                st.success("Transaction saved.")
                st.rerun()

            if submitted:

                if quantity <= 0:

                    st.error(
                        "Quantity must be greater than zero."
                    )

                elif price < 0:

                    st.error(
                        "Price cannot be negative."
                    )

                else:

                    add_transaction(
                        portfolio_id=portfolio_options[
                            portfolio_name
                        ],
                        security_id=security_options[
                            security_name
                        ],
                        transaction_date=str(
                            transaction_date
                        ),
                        transaction_type=transaction_type,
                        quantity=quantity,
                        price=price,
                        currency=currency,
                        commission=commission,
                        notes=notes,
                    )

                    st.success(
                        "Transaction saved."
                    )

                    st.rerun()

    st.divider()

    st.subheader("Transaction History")

    transactions = get_transactions()

    if transactions:

        import pandas as pd

        df = pd.DataFrame(
            [dict(row) for row in transactions]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No transactions recorded yet."
        )
