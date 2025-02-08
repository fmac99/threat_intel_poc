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
        fig_timeline = px.line(df_timeline, x='Date', y='Threats', title='Daily Threat Activity')
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.subheader("Geographic Distribution")
        geo_dict = st.session_state["threat_data"]["geo"]
        df_geo = pd.DataFrame(list(geo_dict.items()), columns=["country", "threats"])
        fig_geo = px.choropleth(df_geo, locations='country',
                                locationmode='country names',
                                color='threats',
                                title='Threat Origin Distribution')
        st.plotly_chart(fig_geo, use_container_width=True)
        column1, column2 = st.columns(2)
        with column1:
            st.data_editor(df_geo)
        with column2:
            st.data_editor(df_timeline)
    if st.session_state.show_chat_interface:
        with col2:
            st.subheader("Threat Intelligence Chat Assistant")
            groq_chat()

if __name__ == "__main__":
    threat_dashboard()