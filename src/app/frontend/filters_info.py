from typing import Any, Dict

import streamlit as st

EMPTY_FILTERS = "No filters applied"
NON_EMPTY_FILTERS = "Filters applied -\n\n"


def show_filters_info(applied_filters: Dict[str, Any]) -> None:
    """Display information about applied filters.

    Parameters
    ----------
    applied_filters : Dict[str, Any]
        A dictionary containing the applied filters, where keys are the filter descriptions and values represent the corresponding filter values.

    Returns
    -------
    None
    """
    filters_info = EMPTY_FILTERS

    # Filters applied
    if applied_filters:
        applied_filters_str = "\n\n".join(
            [f"{key}: {value}" for key, value in applied_filters.items()]
        )
        filters_info = NON_EMPTY_FILTERS + applied_filters_str

    st.info(filters_info)
