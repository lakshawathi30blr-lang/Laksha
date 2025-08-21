import psycopg2
import streamlit as st

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="financee",
            user="postgres",
            password="Laksha@2312",
            port= "5433",
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None

# --- CRUD Operations for Assets ---

def create_asset(ticker, name, asset_class):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO assets (ticker_symbol, asset_name, asset_class) VALUES (%s, %s, %s) RETURNING asset_id;", (ticker, name, asset_class))
            asset_id = cur.fetchone()[0]
            conn.commit()
            return asset_id
    except psycopg2.Error as e:
        st.error(f"Error creating asset: {e}")
        conn.rollback()
        return None
    finally:
        if conn: conn.close()

def get_all_assets():
    conn = get_db_connection()
    if conn is None: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM assets;")
            return cur.fetchall()
    except psycopg2.Error as e:
        st.error(f"Error reading assets: {e}")
        return []
    finally:
        if conn: conn.close()

def update_asset(asset_id, new_ticker, new_name, new_class):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE assets SET ticker_symbol = %s, asset_name = %s, asset_class = %s WHERE asset_id = %s;", (new_ticker, new_name, new_class, asset_id))
            conn.commit()
            return True
    except psycopg2.Error as e:
        st.error(f"Error updating asset: {e}")
        conn.rollback()
        return False
    finally:
        if conn: conn.close()

def delete_asset(asset_id):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM assets WHERE asset_id = %s;", (asset_id,))
            conn.commit()
            return True
    except psycopg2.Error as e:
        st.error(f"Error deleting asset: {e}")
        conn.rollback()
        return False
    finally:
        if conn: conn.close()

# --- CRUD Operations for Transactions ---

def create_transaction(account_id, asset_id, type, date, shares, price):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO transactions (account_id, asset_id, transaction_type, transaction_date, shares, price_per_share, total_amount) VALUES (%s, %s, %s, %s, %s, %s, %s);", (account_id, asset_id, type, date, shares, price, shares * price))
            conn.commit()
            return True
    except psycopg2.Error as e:
        st.error(f"Error creating transaction: {e}")
        conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_all_transactions():
    conn = get_db_connection()
    if conn is None: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT t.transaction_id, a.ticker_symbol, t.transaction_type, t.transaction_date, t.shares, t.price_per_share, t.total_amount FROM transactions t JOIN assets a ON t.asset_id = a.asset_id;")
            return cur.fetchall()
    except psycopg2.Error as e:
        st.error(f"Error reading transactions: {e}")
        return []
    finally:
        if conn: conn.close()

# --- Business Insights Functions ---

def get_portfolio_summary():
    conn = get_db_connection()
    if conn is None: return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(DISTINCT asset_id) AS distinct_assets, SUM(total_amount) AS total_invested FROM transactions;")
            summary = cur.fetchone()
            return {"distinct_assets": summary[0], "total_invested": summary[1]}
    except psycopg2.Error as e:
        st.error(f"Error getting portfolio summary: {e}")
        return None
    finally:
        if conn: conn.close()

def get_asset_class_breakdown():
    conn = get_db_connection()
    if conn is None: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT a.asset_class, SUM(t.total_amount) as total_value FROM transactions t JOIN assets a ON t.asset_id = a.asset_id GROUP BY a.asset_class ORDER BY total_value DESC;")
            return cur.fetchall()
    except psycopg2.Error as e:
        st.error(f"Error getting asset class breakdown: {e}")
        return []
    finally:
        if conn: conn.close()

def get_transaction_insights():
    conn = get_db_connection()
    if conn is None: return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT MIN(price_per_share), MAX(price_per_share), AVG(price_per_share) FROM transactions WHERE transaction_type = 'buy';")
            return cur.fetchone()
    except psycopg2.Error as e:
        st.error(f"Error getting transaction insights: {e}")
        return None
    finally:
        if conn: conn.close()