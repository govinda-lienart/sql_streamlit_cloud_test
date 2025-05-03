import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv

# Page setup
st.set_page_config(page_title="SQL Debug Tool", page_icon="🧪")
st.title("🧪 Google Cloud SQL – Booking Table Test")

# Load environment variables from .env
load_dotenv()

# SQL query input box (always visible)
query = st.text_area("🔍 Enter SQL query to run:", "SELECT * FROM bookings LIMIT 10;")

# Only connect and execute when the user clicks the button
if st.button("Run Query"):
    try:
        st.write("🔄 Attempting to connect to the database...")

        # Database connection
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            connection_timeout=5
        )
        st.success("✅ Successfully connected to MySQL.")

        # Create cursor and execute query
        cursor = conn.cursor()
        st.write(f"▶️ Running query:\n```sql\n{query}\n```")
        cursor.execute(query)
        rows = cursor.fetchall()

        # Show results
        col_names = [desc[0] for desc in cursor.description]
        st.dataframe(rows, use_container_width=True)
        st.caption(f"🧾 Columns returned: {col_names}")

    except Exception as e:
        st.error(f"❌ Connection or query failed:\n\n{e}")

    finally:
        try:
            if 'conn' in locals() and conn.is_connected():
                st.write("🔌 Closing database connection...")
                cursor.close()
                conn.close()
                st.info("✅ Connection closed successfully.")
        except Exception as close_err:
            st.warning(f"⚠️ Error during cleanup:\n\n{close_err}")