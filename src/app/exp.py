# import streamlit as st
# import pandas as pd
# from st_aggrid import GridOptionsBuilder, AgGrid, JsCode

# # Test data is copy from www.ag-grid.com
# # In order to minimize the coding time, please allow me to show it in such a weird format.
# data = {
#     "Michael Phelps": 27,
#     "Natalie Coughlin": 25,
#     "Aleksey Nemov": 24,
#     "Alicia Coutts": 24,
#     "Missy Franklin": 17,
#     "Ryan Lochte": 27,
#     "Allison Schmitt": 22,
#     "Natalie Coughlin": 21,
#     "Ian Thorpe": 17,
#     "Dara Torres": 33,
#     "Cindy Klassen": 26,
# }

# df = pd.DataFrame({"name": data.keys(), "age": data.values()})


# defaultColDef = {
#     "filter": True,
#     "resizable": True,
#     "sortable": True,
# }

# options = {
#     "rowSelection": "multiple",
#     "rowMultiSelectWithClick": True,
#     "enableRangeSelection": True,
# }

# options_builder = GridOptionsBuilder.from_dataframe(df)
# options_builder.configure_default_column(**defaultColDef)
# options_builder.configure_grid_options(**options)
# grid_options = options_builder.build()
# grid_table = AgGrid(df, grid_options, allow_unsafe_jscode=True)


from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd
import streamlit as st


data = {'cpu': ['Intel Core i7-12700K', 'Intel Core i9-12900K',
                'Intel Core i9-10850K', 'Intel Core i5-11400F'],
        'price': [350, 560, 300, 160]}


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


df = pd.DataFrame(data)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridoptions = gb.build()

response = AgGrid(
    df,
    height=200,
    gridOptions=gridoptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
    header_checkbox_selection_filtered_only=True,
    use_checkbox=True)

# st.write(type(response))
# st.write(response.keys())

v = response['selected_rows']
if v:
    st.write('Selected rows')
    st.dataframe(v)
    dfs = pd.DataFrame(v)
    csv = convert_df(dfs)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='selected.csv',
        mime='text/csv',
    )