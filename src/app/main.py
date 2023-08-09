"""Demo App for Neglected Diagnostics.

This is a demo app for neglected diagnostics built using Streamlit and Biopython. The PIs want me 
to build a quick prototype. So, I am first focusing on building a quick prototype that implements 
things end to end and then work towards improving individual modules.
"""

from typing import List

import pandas as pd
import streamlit as st

from app.common import data_processing, setup
from app.common.constants import (
    MAIN_PAGE_COLS_GAP,
    MAIN_PAGE_COLS_SIZE,
    NCBI_DF,
    NCBI_DF_FILTER,
    NCBI_SUMMARY_FORM,
    TOP_N_ORGANISMS,
)
from app.frontend.aggrid_table import aggrid_table
from app.frontend.download_data import download_data
from app.frontend.filter_dataframe import filter_dataframe
from app.frontend.filters_info import show_filters_info
from genetic_testing.routers import ncbi

# Initialize the Streamlit session state keys
setup.initialize()

# Divides the page layout into two columns of relative width
query_col, summary_col = st.columns(MAIN_PAGE_COLS_SIZE, gap=MAIN_PAGE_COLS_GAP)

with query_col:
    st.header("Neglected Diagnostics: Democratizing Genetic Testing!")
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
                data_processing.format_ncbi_summary()

    df_aggrid = pd.DataFrame()
    if st.session_state[NCBI_SUMMARY_FORM]:
        aggrid_table = aggrid_table()  # Initialize and Render Aggrid Table
        df_aggrid = aggrid_table["data"]

    # Streamlit UI to filter the dataset
    df_filtered, applied_filters = filter_dataframe(df_aggrid)
    if st.session_state[NCBI_DF_FILTER]:
        st.dataframe(df_filtered)
        st.write(f"Size of final data: {len(df_filtered)}")

        if st.button("Prepare Download"):
            download_data(database, df_filtered["Id"].unique(), search_term)

    # Streamlit UI to show the applied filters
    show_filters_info(applied_filters)

with summary_col:
    # Show the summary only if user has submitted the query form
    if st.session_state[NCBI_SUMMARY_FORM]:
        st.header("Top Organisms")
        st.write(data_processing.get_top_organisms_counts(TOP_N_ORGANISMS))
