"""Demo App for Neglected Diagnostics.

This is a demo app for neglected diagnostics built using Streamlit and Biopython. The PIs want me 
to build a quick prototype. So, I am first focusing on building a quick prototype that implements 
things end to end and then work towards improving individual modules.
"""

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

from genetic_testing.routers import ncbi

if "SUMMARY_FORM_SUBMIT" not in st.session_state:
    st.session_state["SUMMARY_FORM_SUBMIT"] = False

if "df_summary" not in st.session_state:
    st.session_state["df_summary"] = pd.DataFrame()
    st.session_state["rerun"] = False
    st.session_state["summary_form_submit_count"] = 0

# AgGrid
defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,   
}

# column_defs = [{"headerName": "Title", 
#                 "field": "Title", 
#                 "filter": "agMultiColumnFilter",
#                 "filterParams": {
#                     "filterOptions": ["contains", "notContains"]
#                 }}]

options = {
    "rowSelection": "multiple",
    "rowMultiSelectWithClick": True,
    "enableRangeSelection": True,
}

def rerun():
    st.session_state.rerun = True

def get_data(database, search_term):
    uids = ncbi.search(database, search_term)
    print('Total number of documents returned for the above search query: ' + str(len(uids)))
    document_summaries = ncbi.summary(database, uids)
    parsed_summaries = ncbi.parse_summary(document_summaries)
    df_summaries = pd.DataFrame.from_dict(parsed_summaries)
    return df_summaries

def preprocess_summary_data():
    # Extract the species
    st.session_state["df_summary"]["Species"] = st.session_state["df_summary"]["Title"].apply(lambda x: ' '.join(x.split()[:2]))

    # Reorder the columns
    column_order = ["Species", "Title", "TaxId", "Id", "Length", "Gi", "CreateDate", "UpdateDate", "Status"]
    st.session_state["df_summary"] = st.session_state["df_summary"].reindex(columns=column_order)

st.title("Neglected Diagnostics: Perform Genetic Testing At Scale!")

with st.form("query"):    
    database = st.selectbox("Select the database to search", ("nucleotide", "gene"))
    search_term = st.text_input(label="Enter the search term", placeholder="Example: human[organism] AND topoisomerase[protein name]")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state["summary_form_submit_count"] += 1
        print("Summary form submission count",  st.session_state["summary_form_submit_count"])
        
        st.session_state["df_summary"] = get_data(database, search_term)
        print("Number of rows in summary after fetching data: ", len(st.session_state["df_summary"]))
        preprocess_summary_data()
        
        st.session_state["SUMMARY_FORM_SUBMIT"] = True
        
selected_df = pd.DataFrame()
if st.session_state["SUMMARY_FORM_SUBMIT"]:
    #st.write("Number of rows in df_summary_edited before: ", len(st.session_state["df_summary"]))
    
    #st.session_state["df_summary"] = st.data_editor(st.session_state["df_summary"], num_rows="dynamic", on_change=rerun)
    
    options_builder = GridOptionsBuilder.from_dataframe(st.session_state["df_summary"])
    options_builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    options_builder.configure_side_bar()
    options_builder.configure_selection("multiple", use_checkbox=True)
    options_builder.configure_column("Title", filter="agMultiColumnFilter", filterParams={"maxNumConditions": 4})
    options_builder.configure_column("Species", filter="agMultiColumnFilter")
    options_builder.configure_default_column(**defaultColDef)
    options_builder.configure_grid_options(**options)
    grid_options = options_builder.build()
    grid_table = AgGrid(st.session_state["df_summary"], 
                        gridOptions=grid_options,
                        update_mode=GridUpdateMode.MODEL_CHANGED,
                        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,)
    
    #st.write("Number of rows in df_summary_edited after: ", len(grid_table["data"]))
    #st.write(grid_table["data"])
    #st.write(type(grid_table))
    #st.write(grid_table.keys())
    #selected_df = grid_table["selected_rows"]
    # if selected_df:
    #     st.write('Selected rows')
    #     st.dataframe(selected_df)

    filtered_df = grid_table['data']
    st.write('Filtered rows')
    st.dataframe(filtered_df)
    

#st.write(st.session_state)

# if st.session_state.rerun:
#     st.session_state.rerun = False
#     st.experimental_rerun()




# download_ids = st.text_input(
#     label="Enter the id of the species to download the sequence data",
#     placeholder="2155465881")

# if st.button('Download'):
#     document = ncbi.fetch(database, download_ids)
#     st.write(document)


