"""Demo App for Neglected Diagnostics.

This is a demo app for neglected diagnostics built using Streamlit and Biopython. The PIs want me 
to build a quick prototype. So, I am first focusing on building a quick prototype that implements 
things end to end and then work towards improving individual modules.
"""

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from genetic_testing.routers import ncbi

if "SUMMARY_FORM_SUBMIT" not in st.session_state:
    st.session_state["SUMMARY_FORM_SUBMIT"] = False

if "df_summary" not in st.session_state:
    st.session_state["df_summary"] = pd.DataFrame()
    st.session_state["rerun"] = False
    st.session_state["summary_form_submit_count"] = 0

def rerun():
    st.session_state.rerun = True

def get_data(database, search_term):
    uids = ncbi.search(database, search_term)
    print('Total number of documents returned for the above search query: ' + str(len(uids)))
    document_summaries = ncbi.summary(database, uids)
    parsed_summaries = ncbi.parse_summary(document_summaries)
    df_summaries = pd.DataFrame.from_dict(parsed_summaries)
    return df_summaries

st.title("Neglected Diagnostics: Perform Genetic Testing At Scale!")

with st.form("query"):    
    database = st.selectbox("Select the database to search", ("nucleotide", "gene"))
    search_term = st.text_input(label="Enter the search term", placeholder="Example: human[organism] AND topoisomerase[protein name]")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state["summary_form_submit_count"] += 1
        print("Summary form submission count",  st.session_state["summary_form_submit_count"])
        
        st.session_state["df_summary"] = get_data(database, search_term)
        print("Size of df_summary_edited after fetching data: ", len(st.session_state["df_summary"]))
    
        st.session_state["SUMMARY_FORM_SUBMIT"] = True
        
if st.session_state["SUMMARY_FORM_SUBMIT"]:
    #st.write("Number of rows in df_summary_edited before: ", len(st.session_state["df_summary"]))
    
    st.session_state["df_summary"] = st.data_editor(st.session_state["df_summary"], num_rows="dynamic", on_change=rerun)
    #AgGrid(st.session_state["df_summary"])
    
    #st.write("Number of rows in df_summary_edited after: ", len(st.session_state["df_summary"]))

#st.write(st.session_state)

if st.session_state.rerun:
    st.session_state.rerun = False
    st.experimental_rerun()



# download_ids = st.text_input(
#     label="Enter the id of the species to download the sequence data",
#     placeholder="2155465881")

# if st.button('Download'):
#     document = ncbi.fetch(database, download_ids)
#     st.write(document)


# import streamlit as st
# import pandas as pd

# st.write(st.session_state)

# # Initialize session state with dataframes
# # Include initialization of "edited" slots by copying originals
# if 'df1' not in st.session_state:
#     st.session_state.df1 = pd.DataFrame({
#         "col1": ["a1", "a2", "a3"],
#         "Values": [1, 2, 3]
#     })
#     st.session_state.edited_df1 = st.session_state.df1.copy()
#     st.session_state.df2 = pd.DataFrame({
#         "col1": ["b1", "b2", "b3"], 
#         "Values": [1, 2, 3]
#     })
#     st.session_state.edited_df2 = st.session_state.df2.copy()

# # Save edits by copying edited dataframes to "original" slots in session state
# def save_edits():
#     st.session_state.df1 = st.session_state.edited_df1.copy()
#     st.session_state.df2 = st.session_state.edited_df2.copy()

# # Sidebar to select page and commit changes upon selection
# page = st.sidebar.selectbox("Select: ", ("A","B"), on_change=save_edits)

# # Convenient shorthand notation
# df1 = st.session_state.df1
# df2 = st.session_state.df2

# # Page functions commit edits in real time to "editied" slots in session state
# def funct1():
#     st.session_state.edited_df1 = st.data_editor(df1, num_rows="dynamic")
#     st.write(st.session_state)
#     return

# def funct2():
#     st.session_state.edited_df2 = st.data_editor(df2, num_rows="dynamic")
#     st.write(st.session_state)
#     return

# if  page == "A":
#     st.header("Page A")
#     funct1()
# elif page == "B":
#     st.header("Page B")
#     funct2()


# import streamlit as st

# st.write(st.session_state)

# with st.form('my_form'):
#     st.session_state.A = st.text_input('A')
#     st.text_input('B', key='B')
#     st.form_submit_button('Submit')

# st.write(st.session_state)

# import streamlit as st
# import pandas as pd

# if 'df' not in st.session_state:
#     st.session_state.df = pd.DataFrame({'A':[1,2,3,4],'B':[1,2,3,4]})

# edited_df = st.data_editor(st.session_state.df)

# st.session_state.df = edited_df

# st.write(st.session_state)
