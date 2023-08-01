from typing import List

import streamlit as st

from genetic_testing.routers import ncbi


def download_data(database: str, ids: List[int], search_term: str) -> None:
    """
    Download sequence data from NCBI's database using the given UIDs.

    Parameters
    ----------
    database : str
        The name of the NCBI database from which data will be fetched.

    ids : List[int]
        A list of UIDs representing the entries to be fetched from the database.

    search_term : str
        The search term used to filter the data to be fetched.

    Returns
    -------
    None
        This function does not return any value. The fetched data is directly written to the Streamlit app.

    Notes
    -----
    This function uses the `fetch_data` function from the `genetic_testing.routers.ncbi` module to retrieve data
    from the specified NCBI database based on the provided list of IDs. If the `ids` list is empty, the function writes "Filtered Data is empty" to the Streamlit app. Otherwise, it fetches the data, converts it to a string, and writes "Fetched Data Successfully!" to the Streamlit app, along with a download button for the data. The downloaded file will be named "data.fasta" by default.
    """
    if len(ids) == 0:
        st.write("Filtered Data is empty")
    else:
        file_buffer = ncbi.fetch_data(database, ids)
        file_str = file_buffer.getvalue()
        if len(file_str) == 0:
            st.write(
                f"NCBI's '{database}' database has no data for '{search_term}' search term"
            )
        else:
            st.write("Fetched Data Successfully!")
            st.download_button(
                label="Download",
                data=file_str,
                file_name=f"{database}_{search_term}.fasta",
            )
