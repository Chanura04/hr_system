import json

import httpx
import streamlit as st


st.set_page_config(page_title="HR Multi-Agent UI", layout="wide")

st.title("HR Multi-Agent Dashboard")


api_base = st.text_input("FastAPI base URL", "http://localhost:8000")
user_id = st.text_input("User ID", "user-123")
message = st.text_area("Message", "Please schedule a meeting with my manager.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit Request"):
        if not user_id or not message:
            st.warning("Please enter both a User ID and a Message.")
        else:
            endpoint = f"{api_base.rstrip('/')}/request"
            try:
                response = httpx.post(
                    endpoint,
                    json={"user_id": user_id, "message": message},
                    timeout=30,
                )
                response.raise_for_status()
                st.success("Request submitted successfully.")
                st.json(response.json())
            except Exception as exc:
                st.error(f"Unable to send request: {exc}")

with col2:
    if st.button("Load Audit Log"):
        endpoint = f"{api_base.rstrip('/')}/audit"
        try:
            response = httpx.get(endpoint, timeout=30)
            response.raise_for_status()
            st.json(response.json())
        except Exception as exc:
            st.error(f"Unable to load audit log: {exc}")

with col3:
    if st.button("Load Memory"):
        if not user_id:
            st.warning("Please enter a User ID to load memory.")
        else:
            endpoint = f"{api_base.rstrip('/')}/memory/{user_id}"
            try:
                response = httpx.get(endpoint, timeout=30)
                response.raise_for_status()
                st.json(response.json())
            except Exception as exc:
                st.error(f"Unable to load memory: {exc}")

st.markdown("---")

with st.expander("Current Configuration"):
    st.write(
        {
            "FastAPI base URL": api_base,
            "User ID": user_id,
            "Message": message,
        }
    )


