import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import json
from groq import Groq

def groq_chat():
    api_key = json.load(open("/home/frank/threat_intel_poc_key.json"))["tipoc"]
    client = Groq(api_key=api_key)

    if "llm_model" not in st.session_state:
        st.session_state["llm_model"] = "llama-3.3-70b-versatile"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about threats, assets, or incidents..."):
        # Add user message
        threat_data_reference = st.session_state.get("threat_data", {})
        st.session_state.messages.append({"role": "user", "content": str("threat_data-->" + str(threat_data_reference))})
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Example: Access threat data in session state
        threat_data_reference = st.session_state.get("threat_data", {})
        # Incorporate logic to use `threat_data_reference` if desired.
        #st.write(threat_data_reference)
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state["llm_model"],
                messages=[
                   
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=2048
            )
            assistant_msg = response.choices[0].message.content   
            st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
            st.markdown(assistant_msg)

def threat_dashboard():
    st.title("Threat Intelligence Dashboard")
    # High-level stat cards
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.metric("Active Incidents", "23", "+5")
    with colB:
        st.metric("Critical Threats", "12", "+2")
    with colC:
        st.metric("Avg Severity Score", "7.5", "+0.3")
    with colD:
        st.metric("High Risk Assets", "15")
    # Toggle Chat
    if 'show_chat_interface' not in st.session_state:
        st.session_state.show_chat_interface = False

    if st.button("Toggle Chat"):
        st.session_state.show_chat_interface = not st.session_state.show_chat_interface

    # Generate or load threat data
    # (For demonstration, we use random data. Store in session state.)
    st.session_state["threat_data"] = {
        "timeline": list(np.random.randint(10, 50, size=10)),
        "geo": {"USA": 45, "China": 32, "Russia": 28}
    }

    # Columns based on chat toggle
    if st.session_state.show_chat_interface:
        col1, col2 = st.columns(2)
    else:
        col1, _ = st.columns((1, 0.0001))

    with col1:
        st.subheader("Threat Timeline")
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        df_timeline = pd.DataFrame({'Date': dates, 'Threats': st.session_state["threat_data"]["timeline"]})
        
        # Slicers to control time series
        min_date = df_timeline["Date"].min()
        max_date = df_timeline["Date"].max()
        date_range = st.date_input("Select Date Range", [min_date, max_date])

        if len(date_range) == 2:
            start_date, end_date = date_range
            # Filter data according to selected dates
            df_filtered = df_timeline[(df_timeline["Date"] >= pd.to_datetime(start_date)) &
                                      (df_timeline["Date"] <= pd.to_datetime(end_date))]
        else:
            df_filtered = df_timeline

        fig_timeline = px.line(df_filtered, x='Date', y='Threats', title='Daily Threat Activity')
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.subheader("Geographic Distribution")
        geo_dict = st.session_state["threat_data"]["geo"]
        df_geo = pd.DataFrame(list(geo_dict.items()), columns=["country", "threats"])
        fig_geo = px.choropleth(df_geo, locations='country',
                                locationmode='country names',
                                color='threats',
                                title='Threat Origin Distribution')
        st.plotly_chart(fig_geo, use_container_width=True)
        st.subheader("Threat Distribution (Pie)")
        df_distribution = pd.DataFrame({
            "Type": ["Ransomware", "Malware", "Phishing", "Others"], 
            "Count": [12, 18, 7, 5]
        })
        fig_dist = px.pie(df_distribution, values='Count', names='Type', title='Threat Distribution')
        st.plotly_chart(fig_dist, use_container_width=True)
        st.subheader("Geo Data & Timeline Data Editors")

        # Filtering and sorting controls for df_geo
        st.markdown("#### Filter & Sort Geo Data")
        geo_filter_col = st.selectbox("Filter column (Geo)", df_geo.columns, key="geo_filter_col")
        geo_filter_val = st.text_input("Filter value (Geo)", key="geo_filter_val")
        geo_sort_col = st.selectbox("Sort by column (Geo)", df_geo.columns, key="geo_sort_col")
        geo_desc = st.checkbox("Sort descending (Geo)", key="geo_desc")

        df_geo_filtered = df_geo.copy()

        # Apply filter (simple equality check)
        if geo_filter_val:
            df_geo_filtered = df_geo_filtered[df_geo_filtered[geo_filter_col].astype(str) == geo_filter_val]

        # Apply sorting
        df_geo_filtered = df_geo_filtered.sort_values(by=geo_sort_col, ascending=not geo_desc)

        # Data editor for df_geo
        st.data_editor(
            df_geo_filtered, 
            hide_index=True, 
            num_rows="dynamic"
        )

        # Filtering and sorting controls for df_timeline
        st.markdown("#### Filter & Sort Timeline Data")
        time_filter_col = st.selectbox("Filter column (Timeline)", df_timeline.columns, key="time_filter_col")
        time_filter_val = st.text_input("Filter value (Timeline)", key="time_filter_val")
        time_sort_col = st.selectbox("Sort by column (Timeline)", df_timeline.columns, key="time_sort_col")
        time_desc = st.checkbox("Sort descending (Timeline)", key="time_desc")

        df_timeline_filtered = df_timeline.copy()

        # Apply filter (simple equality check)
        if time_filter_val:
            df_timeline_filtered = df_timeline_filtered[
                df_timeline_filtered[time_filter_col].astype(str) == time_filter_val
            ]

        # Apply sorting
        df_timeline_filtered = df_timeline_filtered.sort_values(by=time_sort_col, ascending=not time_desc)

        # Data editor for df_timeline
        st.data_editor(
            df_timeline_filtered, 
            hide_index=True, 
            num_rows="dynamic"
        )

    if st.session_state.show_chat_interface:
        with col2:
            st.subheader("Threat Intelligence Chat Assistant")
            groq_chat()

if __name__ == "__main__":
    threat_dashboard()