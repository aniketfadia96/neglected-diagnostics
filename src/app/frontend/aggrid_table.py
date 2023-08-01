from typing import DefaultDict, Dict

import streamlit as st
from st_aggrid import (
    AgGrid,
    ColumnsAutoSizeMode,
    DataReturnMode,
    GridOptionsBuilder,
    GridUpdateMode,
)

from app.common.constants import NCBI_DF

DEFAULT_COL_DEF = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,
}


def _initialize_grid_options() -> DefaultDict:
    """Initialize and configure options for the AgGrid table.

    This function creates an AgGrid options builder using the DataFrame stored in the Streamlit session state. It then configures various options for the AgGrid table, such as default column settings, pagination, etc.

    Returns
    -------
    DefaultDict
        A dictionary representing the configuration options for the AgGrid table.

    Notes
    -----
    Before calling this function, ensure that you have stored your DataFrame in the Streamlit session state using the key specified by the constant `NCBI_DF`. The table options will be based on the data in this DataFrame.

    The `DEFAULT_COL_DEF` constant contains a dictionary of default column settings for the AgGrid table.
    """
    options_builder = GridOptionsBuilder.from_dataframe(st.session_state[NCBI_DF])
    options_builder.configure_default_column(**DEFAULT_COL_DEF)
    options_builder.configure_pagination(
        paginationAutoPageSize=False, paginationPageSize=10
    )

    grid_options = options_builder.build()

    return grid_options


def aggrid_table() -> Dict:
    """Create an AgGrid table with custom options and return it.

    This function initializes and configures an AgGrid table using the provided DataFrame
    stored in the Streamlit session state.

    Returns
    -------
    Dict
        A dictionary representing the AgGrid table.

    Notes
    -----
    - Before calling this function, ensure that you have stored your DataFrame in the
    Streamlit session state using the key specified by the constant `NCBI_DF`. The table will be created using the data from this DataFrame.

    - `enable_enterprise_modules` should be set to False to be eligible to use the Open-Source version of `aggrid`. Refer here for more details - https://www.ag-grid.com/javascript-data-grid/licensing/
    """
    grid_options = _initialize_grid_options()
    grid_table = AgGrid(
        st.session_state[NCBI_DF],
        gridOptions=grid_options,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED,
        enable_enterprise_modules=False,
    )

    return grid_table
