import streamlit as st
import plotly.express as px
from datetime import datetime

def main_interface():
    # Page config
    st.set_page_config(
        page_title="Threat Intelligence Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    with st.sidebar:
        st.title("Threat Intel")
        selected = st.radio(
            "Go to",
            ["Threat Dashboard", "Intelligence Analysis", "Threat Visualization", "Configuration"]
        )

    # Initialize session state
    if 'threat_data' not in st.session_state:
        st.session_state.threat_data = None
    if 'threat_config' not in st.session_state:
        st.session_state.threat_config = {}

    # Main content
    if selected == "Threat Dashboard":
        st.title("🛡️ Threat Intelligence Dashboard")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Threats", "47", "+12%")
        with col2:
            st.metric("Incidents", "23", "-5%")
        with col3:
            st.metric("Risk Score", "7.8", "+2.1")

    elif selected == "Intelligence Analysis":
        st.title("🔍 Intelligence Analysis")
        
        uploaded_file = st.file_uploader("Upload Data", type=['csv', 'json'])
        if uploaded_file:
            st.session_state.threat_data = pd.read_csv(uploaded_file)
            st.dataframe(st.session_state.threat_data)

    elif selected == "Threat Visualization":
        st.title("📈 Threat Visualization")
        
        if st.session_state.threat_data is not None:
            chart_type = st.selectbox("Select Chart Type", 
                                    ["Line", "Bar", "Scatter"])
            st.plotly_chart(create_chart(st.session_state.threat_data, chart_type))

    else:  # Configuration
        st.title("⚙️ Configuration")
        
        st.session_state.threat_config['theme'] = st.selectbox(
            "Theme", ["Light", "Dark"]
        )
        st.session_state.threat_config['update_interval'] = st.slider(
            "Update Interval (s)", 1, 60, 5
        )

if __name__ == "__main__":
    main_interface()