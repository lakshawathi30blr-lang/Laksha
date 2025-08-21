import streamlit as st
import backend as backend

st.set_page_config(layout="wide")

# Main App Title and Header
st.title("💰 Personal Financial Portfolio Tracker")
st.markdown("Your name, Your Roll No") # Replace with your details

# Navigation Bar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Assets", "Transactions", "Business Insights"])

# --- Dashboard ---
if page == "Dashboard":
    st.header("Dashboard Overview")
    summary = backend.get_portfolio_summary()
    if summary:
        st.markdown("### Portfolio Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Investments", f"${summary['total_invested'] or 0:.2f}")
        col2.metric("Distinct Assets", f"{summary['distinct_assets'] or 0}")
    
    st.markdown("### Asset Class Breakdown")
    breakdown = backend.get_asset_class_breakdown()
    if breakdown:
        import pandas as pd
        df = pd.DataFrame(breakdown, columns=['Asset Class', 'Total Value'])
        st.bar_chart(df.set_index('Asset Class'))
    else:
        st.info("No data to display. Add some transactions.")
    
    st.markdown("### Recent Transactions")
    transactions = backend.get_all_transactions()
    if transactions:
        import pandas as pd
        df = pd.DataFrame(transactions, columns=['ID', 'Ticker', 'Type', 'Date', 'Shares', 'Price', 'Total Amount'])
        st.dataframe(df.head(10))
    else:
        st.info("No recent transactions found.")

# --- Assets (CRUD) ---
elif page == "Assets":
    st.header("Asset Management (CRUD)")
    
    # CREATE operation
    st.subheader("Add a New Asset (Create)")
    with st.form("add_asset_form"):
        ticker = st.text_input("Ticker Symbol (e.g., AAPL)")
        name = st.text_input("Asset Name (e.g., Apple Inc.)")
        asset_class = st.selectbox("Asset Class", ["Equity", "Fixed Income", "Cryptocurrency", "Other"])
        submit_button = st.form_submit_button("Add Asset")
        if submit_button:
            if backend.create_asset(ticker, name, asset_class):
                st.success(f"Asset '{ticker}' added successfully!")
                st.experimental_rerun()
            else:
                st.error("Failed to add asset.")

    # READ, UPDATE, and DELETE operations
    st.subheader("Manage Existing Assets (Read, Update, Delete)")
    assets = backend.get_all_assets()
    if assets:
        assets_df = pd.DataFrame(assets, columns=['ID', 'Ticker', 'Name', 'Class'])
        st.dataframe(assets_df)

        with st.expander("Update/Delete Asset"):
            asset_to_modify = st.selectbox("Select Asset to Modify", assets, format_func=lambda x: f"{x[1]} - {x[2]}")
            if asset_to_modify:
                asset_id_to_modify = asset_to_modify[0]
                
                # UPDATE operation
                st.subheader("Update Asset")
                new_ticker = st.text_input("New Ticker Symbol", value=asset_to_modify[1], key=f"upd_ticker_{asset_id_to_modify}")
                new_name = st.text_input("New Asset Name", value=asset_to_modify[2], key=f"upd_name_{asset_id_to_modify}")
                new_class = st.selectbox("New Asset Class", ["Equity", "Fixed Income", "Cryptocurrency", "Other"], index=["Equity", "Fixed Income", "Cryptocurrency", "Other"].index(asset_to_modify[3]), key=f"upd_class_{asset_id_to_modify}")
                if st.button("Update Asset"):
                    if backend.update_asset(asset_id_to_modify, new_ticker, new_name, new_class):
                        st.success("Asset updated successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to update asset.")

                # DELETE operation
                st.subheader("Delete Asset")
                if st.button("Delete Asset", help="This will delete the asset permanently."):
                    if backend.delete_asset(asset_id_to_modify):
                        st.success("Asset deleted successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete asset.")
    else:
        st.info("No assets found. Add one above.")

# --- Transactions (CRUD) ---
elif page == "Transactions":
    st.header("Transaction Log (CRUD)")
    
    # CREATE operation
    st.subheader("Add a New Transaction (Create)")
    all_assets = backend.get_all_assets()
    if not all_assets:
        st.warning("Please add an asset first in the 'Assets' section.")
    else:
        asset_dict = {f"{a[1]} - {a[2]}": a[0] for a in all_assets}
        with st.form("add_transaction_form"):
            selected_asset = st.selectbox("Select Asset", list(asset_dict.keys()))
            trans_type = st.selectbox("Transaction Type", ["Buy", "Sell", "Dividend"])
            trans_date = st.date_input("Transaction Date")
            shares = st.number_input("Number of Shares", min_value=0.01, format="%.2f")
            price = st.number_input("Price per Share", min_value=0.01, format="%.2f")
            submit_transaction_button = st.form_submit_button("Add Transaction")
            
            if submit_transaction_button:
                asset_id = asset_dict[selected_asset]
                account_id = 1 
                if backend.create_transaction(account_id, asset_id, trans_type, trans_date, shares, price):
                    st.success("Transaction added successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to add transaction.")
    
    # READ operation
    st.subheader("All Transactions (Read)")
    transactions = backend.get_all_transactions()
    if transactions:
        import pandas as pd
        df = pd.DataFrame(transactions, columns=['ID', 'Ticker', 'Type', 'Date', 'Shares', 'Price', 'Total Amount'])
        st.dataframe(df)
    else:
        st.info("No transactions found.")

# --- Business Insights ---
elif page == "Business Insights":
    st.header("Portfolio Insights")
    
    st.subheader("Portfolio Aggregates")
    summary = backend.get_portfolio_summary()
    if summary:
        col1, col2 = st.columns(2)
        col1.metric("Total Investments (SUM)", f"${summary['total_invested'] or 0:.2f}")
        col2.metric("Total Asset Types (COUNT)", f"{summary['distinct_assets'] or 0}")
    
    st.subheader("Transaction Price Analysis (MIN, MAX, AVG)")
    insights = backend.get_transaction_insights()
    if insights:
        col1, col2, col3 = st.columns(3)
        col1.metric("Highest Purchase Price", f"${insights[1] or 0:.2f}")
        col2.metric("Lowest Purchase Price", f"${insights[0] or 0:.2f}")
        col3.metric("Average Purchase Price", f"${insights[2] or 0:.2f}")
    else:
        st.info("No buy transactions to analyze.")