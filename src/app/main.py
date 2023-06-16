"""Demo App for Neglected Diagnostics.

This is a demo app for neglected diagnostics built using Streamlit and Biopython. The PIs want me 
to build a quick prototype. So, I am first focusing on building a quick prototype that implements 
things end to end and then work towards improving individual modules.
"""

import pandas as pd
import streamlit as st

from genetic_testing.routers import ncbi

st.title("Neglected Diagnostics: Perform Genetic Testing At Scale!")

database = st.selectbox("Select the database to search", ("nucleotide", "gene"))
search_term = st.text_input(
    label="Enter the search term",
    placeholder="Example: human[organism] AND topoisomerase[protein name]")

if st.button('Perform Operation'):
    uids = ncbi.search(database, search_term)
    print('Total number of documents returned for the above search query: ' + str(len(uids)))
    document_summaries = ncbi.summary(database, uids)
    parsed_summaries = ncbi.parse_summary(document_summaries)
    df_summaries = pd.DataFrame.from_dict(parsed_summaries)
    st.dataframe(df_summaries)

download_ids = st.text_input(
    label="Enter the id of the species to download the sequence data",
    placeholder="2155465881")

if st.button('Download'):
    document = ncbi.fetch(database, download_ids)
    st.write(document)
    