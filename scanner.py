
import streamlit as st
from supabase import create_client

# --- DB SETUP ---
url = "https://rjofwtimijzwunfdramj.supabase.co"
key = "sb_publishable_Imbf14ozm-Umkof0H7dx3g_6f2yLi9P"         
supabase = create_client(url, key)

st.set_page_config(page_title="Cedar Bucket Mobile", layout="centered")

# Custom CSS to make buttons huge for thumbs
st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; width: 100%; font-size: 20px; font-weight: bold; }
    input { font-size: 18px !important; }
    </style>""", unsafe_allow_html=True)

st.title("📦 Cedar Bucket Mobile")

# TABS: One for Intake, One for Lookup
tab1, tab2 = st.tabs(["📥 Intake", "🔍 Lookup"])

with tab1:
    st.subheader("New Scan")
    # Zebra scans into this box
    rfid = st.text_input("RFID Tag (Scan Now)", key="m_rfid")
    name = st.text_input("Student Name")
    item = st.selectbox("Type", ["Bin", "Fridge", "Trunk", "Other"])
    
    if st.button("SAVE TO CLOUD"):
        if rfid and name:
            data = {"rfid_epc": rfid, "student_name": name, "item_type": item, "status": "Checked In"}
            supabase.table("inventory_items").insert(data).execute()
            st.success("Logged!")
            st.balloons()

with tab2:
    st.subheader("Search Tag")
    s_rfid = st.text_input("Scan Tag to Find Owner", key="m_search")
    if s_rfid:
        res = supabase.table("inventory_items").select("*").eq("rfid_epc", s_rfid).execute()
        if res.data:
            st.info(f"Owner: {res.data[0]['student_name']}\n\nType: {res.data[0]['item_type']}")
        else:
            st.error("Not found")