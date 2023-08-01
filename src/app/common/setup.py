import pandas as pd
import streamlit as st

from app.common.constants import NCBI_DF, NCBI_DF_FILTER, NCBI_SUMMARY_FORM


def initialize() -> None:
    """Initialize the Streamlit session state.

    This function initializes the Streamlit session state by checking the existence of specific keys for storing data and state variables. If any of these keys are not present in the session state, the function creates them and sets their initial values.
    """
    if NCBI_SUMMARY_FORM not in st.session_state:
        st.session_state[NCBI_SUMMARY_FORM] = False
        st.session_state[NCBI_DF_FILTER] = False

    if NCBI_DF not in st.session_state:
        st.session_state[NCBI_DF] = pd.DataFrame()
