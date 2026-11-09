import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# YOUR GOOGLE APPS SCRIPT WEB APP URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyI8u1v3lD441oQI6vogDGWj-0e0EkX9gWMmKJATUvFG5owsnyVStImLhKzBa5c68cJ/exec"

st.set_page_config(page_title="EDU 213 Attendance", layout="centered")
st.title("EDU 213 Attendance System")

tab1, tab2 = st.tabs(["Student Check-In", "Lecturer Control Panel"])

# --- TAB 1: STUDENT CHECK-IN ---
with tab1:
    st.subheader("Student Portal")
    st.write("Enter your full name, matriculation number, and the active whiteboard PIN.")
    
    with st.form(key='student_checkin_form', clear_on_submit=True):
        name_input = st.text_input("Full Name (e.g., John Doe):").strip()
        matric_input = st.text_input("Matriculation Number (e.g., BUE/24/5678):").strip().upper()
        pin_input = st.text_input("Today's Classroom PIN:", type="password")
        
        submit_btn = st.form_submit_button("Submit Attendance")
        
        if submit_btn:
            active_code = st.session_state.get('active_code', '')
            today_date = datetime.now().strftime("%Y-%m-%d")
            
            if not name_input or not matric_input:
                st.warning("Please fill in both your Full Name and Matriculation Number.")
            elif pin_input != active_code or active_code == '':
                st.error("Invalid or missing Classroom PIN. Check the whiteboard.")
            else:
                try:
                    # Automatically extract department from matric number (e.g., BUE/24/1234 -> BUE)
                    parts = matric_input.split('/')
                    department = parts[0] if len(parts) > 1 else "GENERAL"
                    
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    payload = {
                        "timestamp": now,
                        "session_date": today_date,
                        "name": name_input,
                        "matric_no": matric_input,
                        "department": department,
                        "course_code": "EDU 213"
                    }
                    
                    response = requests.post(WEB_APP_URL, json=payload)
                    
                    if response.status_code == 200:
                        st.success(f"Success! Attendance recorded for {name_input} ({department}).")
                    else:
                        st.error("Failed to log attendance. Please try again.")
                except Exception as ex:
                    st.error(f"Connection error: {ex}")

# --- TAB 2: LECTURER CONTROL PANEL ---
with tab2:
    st.subheader("Lecturer Controls")
    
    new_pin = st.text_input("Set Today's 4-Digit Classroom PIN:", max_chars=4, type="password")
    if st.button("Activate PIN"):
        st.session_state['active_code'] = new_pin
        st.success(f"Classroom PIN activated: {new_pin}")
    
    st.divider()
    
    st.subheader("Live Attendance Log")
    st.info("💡 Your student check-ins are now automatically sorted by Department inside your Google Sheet!")