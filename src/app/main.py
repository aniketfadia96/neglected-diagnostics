"""Demo App for Neglected Diagnostics.

This is a demo app for neglected diagnostics built using Streamlit and Biopython. The PIs want me 
to build a quick prototype. So, I am first focusing on building a quick prototype that implements 
things end to end and then work towards improving individual modules.
"""

from typing import List

import pandas as pd
import streamlit as st

from app.common import preprocessing, setup
from app.common.constants import NCBI_DF, NCBI_DF_FILTER, NCBI_SUMMARY_FORM
from app.frontend.aggrid_table import aggrid_table
from app.frontend.download_data import download_data
from app.frontend.filter_dataframe import filter_dataframe
from genetic_testing.routers import ncbi

# Initialize the Streamlit session state keys
setup.initialize()

st.title("Neglected Diagnostics: Perform Genetic Testing At Scale!")
# Streamlit form to capture search conditions
with st.form("query"):
    database = st.selectbox("Select the database to search", ("nucleotide", "gene"))
    search_term = st.text_input(
        label="Enter the search term",
        placeholder="Example: human[organism] AND topoisomerase[protein name]",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        # search term is empty
        if search_term == "":
            st.error("Please input a search term before you submit")
        else:
            st.session_state[NCBI_SUMMARY_FORM] = True
            st.session_state[NCBI_DF] = ncbi.get_data(database, search_term)
            preprocessing.format_ncbi_summary()

df_aggrid = pd.DataFrame()
if st.session_state[NCBI_SUMMARY_FORM]:
    aggrid_table = aggrid_table()  # Initialize and Render Aggrid Table
    df_aggrid = aggrid_table["data"]

# Streamlit UI to filter the dataset
df_filtered = filter_dataframe(df_aggrid)
if st.session_state[NCBI_DF_FILTER]:
    st.dataframe(df_filtered)
    st.write(f"Size of final data: {len(df_filtered)}")

    if st.button("Prepare Download"):
        download_data(database, df_filtered["Id"].unique(), search_term)
