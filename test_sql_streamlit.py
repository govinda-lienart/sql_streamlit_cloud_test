import streamlit as st
import mysql.connector

st.set_page_config(page_title="SQL Debug Tool", page_icon="🧪")

st.title("🧪 Google Cloud SQL – Booking Table Test")

try:
    # Connect using Streamlit secrets
    conn = mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USERNAME"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_DATABASE"]
    )
    st.success("✅ Connected to MySQL!")

    cursor = conn.cursor()

    # Optional query box
    query = st.text_area("🔍 Enter SQL query to run:", "SELECT * FROM bookings LIMIT 10;")

    if st.button("Run Query"):
        cursor.execute(query)
        rows = cursor.fetchall()

        # Try to get column names
        try:
            col_names = [desc[0] for desc in cursor.description]
            st.dataframe(rows, use_container_width=True)
            st.caption(f"Columns: {col_names}")
        except:
            st.write(rows)

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