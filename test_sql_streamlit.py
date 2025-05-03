import streamlit as st
import mysql.connector
import os

st.set_page_config(page_title="SQL Debug Tool", page_icon="🧪")
st.title("🧪 Google Cloud SQL – Booking Table Test")

# Load local .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Safe if running on Streamlit Cloud without dotenv

# Hybrid secret loader: check st.secrets first, then fallback to .env
def get_secret(key, default=None):
    return st.secrets.get(key) or os.getenv(key) or default

# Show query box first
query = st.text_area("🔍 Enter SQL query to run:", "SELECT * FROM bookings LIMIT 10;")

if st.button("Run Query"):
    try:
        st.write("🔐 Connecting to database...")

        conn = mysql.connector.connect(
            host=get_secret("DB_HOST"),
            port=int(get_secret("DB_PORT", "3306")),
            user=get_secret("DB_USERNAME"),
            password=get_secret("DB_PASSWORD"),
            database=get_secret("DB_DATABASE")
        )
        st.success("✅ Connected to MySQL!")

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Get and show column headers
        col_names = [desc[0] for desc in cursor.description]
        st.dataframe(rows, use_container_width=True)
        st.caption(f"Columns: {col_names}")

    except Exception as e:
        st.error(f"❌ Connection failed:\n\n{e}")
    finally:
        try:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                st.info("🔌 Connection closed.")
        except Exception as close_err:
            st.warning(f"⚠️ Error closing connection:\n\n{close_err}")