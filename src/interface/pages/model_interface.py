import streamlit as st
import pandas as pd
import sqlalchemy

def get_engine(db_user, db_pass, db_host, db_name):
    """Create a SQLAlchemy engine for the specified database."""
    connection_string = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
    return sqlalchemy.create_engine(connection_string)

def import_data_from_db(engine, table_name):
    """Import data from the specified table."""
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, con=engine)
    return df

def export_data_to_db(engine, table_name, df, if_exists="append"):
    """Export a dataframe to the specified table."""
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)

def model_interface():
    st.title("Model Interface")

    # Sidebar for DB configs
    st.sidebar.subheader("Database Connection")
    db_user = st.sidebar.text_input("DB User", value="root")
    db_pass = st.sidebar.text_input("DB Password", type="password")
    db_host = st.sidebar.text_input("DB Host", value="localhost")
    db_name = st.sidebar.text_input("DB Name", value="threat_db")

    # Get engine on button click
    if st.sidebar.button("Connect to DB"):
        try:
            st.session_state["engine"] = get_engine(db_user, db_pass, db_host, db_name)
            st.sidebar.success("Connected to database!")
        except Exception as e:
            st.sidebar.error(f"Connection error: {e}")

    # Select or upload data
    st.subheader("Data Import/Export")

    table_name_import = st.text_input("Table name to import from", "threat_data")
    if st.button("Import Data"):
        if "engine" in st.session_state:
            try:
                df_imported = import_data_from_db(st.session_state["engine"], table_name_import)
                st.session_state["imported_data"] = df_imported
                st.success("Data imported successfully!")
                st.dataframe(df_imported, use_container_width=True)
            except Exception as e:
                st.error(f"Import error: {e}")
        else:
            st.warning("Please connect to the database first.")

    table_name_export = st.text_input("Table name to export to", "export_table")
    if st.button("Export Data"):
        if "engine" in st.session_state:
            if "imported_data" in st.session_state:
                try:
                    export_data_to_db(st.session_state["engine"], table_name_export, st.session_state["imported_data"])
                    st.success("Data exported successfully!")
                except Exception as e:
                    st.error(f"Export error: {e}")
            else:
                st.warning("No data available to export. Please import data first.")
        else:
            st.warning("Please connect to the database first.")

    # Model Selection
    st.subheader("Model Selection")
    all_models = ["XGBoost", "RandomForest", "NeuralNetwork", "LogisticRegression"]
    chosen_model = st.selectbox("Select a model", all_models)

    if st.button("Load Model"):
        st.success(f"{chosen_model} model selected!")
        st.session_state["model_name"] = chosen_model

if __name__ == "__main__":
    model_interface()