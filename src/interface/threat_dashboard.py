import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

def threat_dashboard():
    # Page Title
    st.title("Threat Intelligence Dashboard")

    # Toggle Chat
    if 'show_chat_interface' not in st.session_state:
        st.session_state.show_chat_interface = False

    if st.button("Toggle Chat"):
        st.session_state.show_chat_interface = not st.session_state.show_chat_interface
    
    # If chat is toggled off, display single column
    # If toggled on, display two columns
    if st.session_state.show_chat_interface:
        col1, col2 = st.columns(2)
    else:
        # If chat is off, just make one wide column
        col1, _ = st.columns((1, 0.0001))

    # Left Column: Existing Dashboard
    with col1:
        st.subheader("Threat Timeline")
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        values = np.random.randint(10, 50, size=len(dates))
        df_timeline = pd.DataFrame({'Date': dates, 'Threats': values})
        fig_timeline = px.line(df_timeline, x='Date', y='Threats', title='Daily Threat Activity')
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.subheader("Geographic Distribution")
        df_geo = pd.DataFrame({
            'country': ['USA', 'China', 'Russia', 'UK', 'Germany'],
            'threats': [45, 32, 28, 15, 12]
        })
        fig_geo = px.choropleth(df_geo, locations='country',
                                locationmode='country names',
                                color='threats',
                                title='Threat Origin Distribution')
        st.plotly_chart(fig_geo, use_container_width=True)

        colA, colB = st.columns(2)

        with colA:
            st.subheader("Threat Severity Breakdown")
            severity_data = {
                'Severity': ['Critical', 'High', 'Medium', 'Low'],
                'Count': [12, 25, 45, 18]
            }
            df_severity = pd.DataFrame(severity_data)
            fig_severity = px.pie(df_severity, values='Count', names='Severity',
                                  title='Threat Severity Distribution')
            st.plotly_chart(fig_severity, use_container_width=True)

        with colB:
            st.subheader("Recent Alerts")
            alerts = [
                {"timestamp": "2024-01-31 14:23", "type": "Malware", "severity": "Critical"},
                {"timestamp": "2024-01-31 13:45", "type": "Phishing", "severity": "High"},
                {"timestamp": "2024-01-31 12:30", "type": "Data Leak", "severity": "Critical"},
                {"timestamp": "2024-01-31 11:15", "type": "Suspicious Access", "severity": "Medium"}
            ]
            df_alerts = pd.DataFrame(alerts)
            st.dataframe(df_alerts, use_container_width=True)

        st.subheader("Top Active Threats")
        threats = {
            "Threat": ["Ransomware Campaign", "APT Group Activity", "Zero-day Exploit", "Supply Chain Attack"],
            "Risk Score": [9.8, 8.7, 8.5, 8.2],
            "Affected Systems": [45, 32, 28, 15],
            "Status": ["Active", "Active", "Investigating", "Contained"]
        }
        df_threats = pd.DataFrame(threats)
        st.dataframe(df_threats, use_container_width=True)

    # Right Column: Simple LLM Chat Interface (only if toggled on)
    if st.session_state.show_chat_interface:
        with col2:
            st.subheader("Threat Intelligence Chat Assistant")

            if "messages" not in st.session_state:
                st.session_state["messages"] = []

            # Display chat history
            for msg in st.session_state["messages"]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # Chat input
            if user_input := st.chat_input("Ask about threats, assets, or incidents..."):
                # Add user message
                st.session_state["messages"].append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                # Placeholder response
                response_text = "This is a placeholder response from the Threat Chat Assistant."

                st.session_state["messages"].append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant"):
                    st.write(response_text)

if __name__ == "__main__":
    threat_dashboard()