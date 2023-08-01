"""Module to search and download sequence data from the NCBI datasource. 

This module is still work in progress. Currently, I am working on implementing the search 
functionality
"""

import os
from io import StringIO
from typing import Dict, List

import pandas as pd
import streamlit as st
from Bio import Entrez, SeqIO
from Bio.Entrez.Parser import DictionaryElement, ListElement, StringElement

from utils.log import _init_logger

logger = _init_logger(__name__)

ENTREZ_EMAIL = "ENTREZ_EMAIL"
NCBI_SUMMARY_FIELDS = [
    "Id",
    "Title",
    "Gi",
    "CreateDate",
    "UpdateDate",
    "TaxId",
    "Length",
    "Status",
]
RETMAX = 10000
RETTYPE = "fasta"  # Specifies the record view returned, such as Abstract or MEDLINE from PubMed, or GenPept or FASTA from protein.
RETMODE = "text"  # Specifies the data format of the records returned, such as plain text, HMTL or XML.

if ENTREZ_EMAIL in st.secrets:
    Entrez.email = st.secrets[ENTREZ_EMAIL]
else:
    Entrez.email = os.environ.get(ENTREZ_EMAIL, "")


def _search(database: str, term: str) -> ListElement[StringElement]:
    """Get the List of UIDs matching the Entrez query.

    This function searches the provided Entrez database and returns the list of UIDs matching the Entrez query.

    Parameters
    ----------
    database : str
        Name of the Entrez database.
    term : str
        Entrez text query.

    Returns
    -------
    ListElement[StringElement]
       A list of UIDs.
    """
    handle = Entrez.esearch(db=database, term=term, retmax=RETMAX)
    uids = []
    if handle:
        record = Entrez.read(handle)
        uids = record["IdList"]
        handle.close()
    return uids


def _summary(
    database: str, ids: ListElement[StringElement]
) -> ListElement[DictionaryElement]:
    """Get the document summaries for the input UIDs.

    This function returns the document summaries for the input list of UIDs and Entrez database.

    Parameters
    ----------
    database : str
        Name of the Entrez database.
    ids : ListElement[StringElement]
        A list of UIDs.

    Returns
    -------
    ListElement[DictionaryElement]
        A list of dictionaries where each dictionary element is a single summary
    """
    handle = Entrez.esummary(db=database, id=ids, retmax=RETMAX)
    if handle:
        record = Entrez.read(handle)
        handle.close()
    return record


def _parse_summary(
    document_summaries: ListElement[DictionaryElement],
) -> List[Dict[str, str]]:
    """Parse document summaries.

    This function parses the input document summaries and selects a subset of columns for the final summary

    Parameters
    ----------
    document_summaries : ListElement[DictionaryElement]
       A list of dictionary elements representing document summaries.

    Returns
    -------
    List[Dict[str, str]]
        A list of dictionaries containing parsed document summaries.
    """
    parsed_summaries = []
    for document_summary in document_summaries:
        parsed_summaries.append(
            {key: document_summary.get(key, None) for key in NCBI_SUMMARY_FIELDS}
        )
    return parsed_summaries


def get_data(database: str, search_term: str) -> pd.DataFrame:
    """Retrieve data from the Entrez database based on a search term.

    Parameters
    ----------
    database : str
        Name of the Entrez database.
    search_term : str
        The term used to search the specified database.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the retrieved data.
    """
    uids = _search(database, search_term)
    logger.info(
        f"Total number of documents returned for database = '{database}' and search query = '{search_term}' is {len(uids)}"
    )
    document_summaries = _summary(database, uids)
    parsed_summaries = _parse_summary(document_summaries)
    df_summaries = pd.DataFrame.from_dict(parsed_summaries)
    return df_summaries


def fetch_data(database: str, ids: List[int]) -> StringIO:
    """Download the sequence data for the input UIDs from the specified Entrez database.

    Parameters
    ----------
    database : str
        Name of the Entrez database from which the sequence data will be fetched.
    ids : List[int]
        List of UIDs.

    Returns
    -------
    StringIO
        A StringIO object containing the fetched sequence data in FASTA format.

    Notes
    -----
    This function uses the Entrez.efetch method from the Biopython library to retrieve sequence data from the specified Entrez database based on the provided list of UIDs. The data is fetched in FASTA format. The function returns a StringIO object that contains the fetched sequence data.
    """
    handle = Entrez.efetch(
        db=database, id=ids, retmax=RETMAX, rettype=RETTYPE, retmode=RETMODE
    )
    if handle:
        sequences_iterator = SeqIO.parse(handle, RETTYPE)
        sequences_str_buffer = StringIO()
        # Write the data to the StringIO object in FASTA format
        SeqIO.write(sequences_iterator, sequences_str_buffer, RETTYPE)
        # Reset the file position indicator to the beginning
        sequences_str_buffer.seek(0)
        handle.close()

    return sequences_str_buffer
