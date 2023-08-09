from typing import List

import streamlit as st

from app.common.constants import NCBI_DF


def format_ncbi_summary() -> None:
    """Format and restructure the NCBI summary DataFrame.

    This function performs formatting and restructuring tasks on the NCBI summary DataFrame, which is assumed to be stored in the Streamlit session state under the key specified by the constant `NCBI_DF`. The function performs the following actions:

    1. Extract the "Species" information from the "Title" column and store it in a new "Species" column.
    2. Convert the "Species" column to a categorical data type.
    3. Reorder the columns of the DataFrame to a predefined order.
    """
    # Extract the species
    st.session_state[NCBI_DF]["Species"] = st.session_state[NCBI_DF]["Title"].apply(
        lambda x: " ".join(x.split()[:2])
    )
    # Convert the species to categorical
    st.session_state[NCBI_DF]["Species"] = st.session_state[NCBI_DF]["Species"].astype(
        "category"
    )

    # Reorder the columns
    column_order = [
        "Species",
        "Title",
        "TaxId",
        "Id",
        "Length",
        "Gi",
        "CreateDate",
        "UpdateDate",
        "Status",
    ]
    st.session_state[NCBI_DF] = st.session_state[NCBI_DF].reindex(columns=column_order)


def get_top_organisms_counts(top_n=15) -> str:
    """Get the top N organisms and their counts in the session's NCBI DataFrame.

    Parameters
    ----------
    top_n : int, optional
        Number of top organisms to show, by default 15

    Returns
    -------
    str
        A formatted string containing the top N organisms and their counts, separated by two newlines ("\n\n").
    """
    # Calculate counts of species and sort by counts in descending order
    species_counts = (
        st.session_state[NCBI_DF]["Species"]
        .value_counts()
        .sort_values(ascending=False)
        .head(top_n)
    )

    # Create the desired output format
    species_counts_list = [
        f"{value} ({count})"
        for value, count in zip(species_counts.index, species_counts)
    ]

    return "\n\n".join(species_counts_list)
