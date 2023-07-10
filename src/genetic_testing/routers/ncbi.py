"""Module to search and download sequence data from the NCBI datasource. 

This module is still work in progress. Currently, I am working on implementing the search 
functionality
"""

import os

outdir = "ncbi_downloads"
os.makedirs(outdir, exist_ok=True)
from typing import Dict, List, Union

import streamlit as st
from Bio import SeqIO
from Bio import Entrez
from Bio.Entrez.Parser import DictionaryElement, ListElement

ENTREZ_EMAIL = "ENTREZ_EMAIL"
SUMMARY_FIELDS = [
    "Id",
    "Title",
    "Gi",
    "CreateDate",
    "UpdateDate",
    "TaxId",
    "Length",
    "Status",
]

if ENTREZ_EMAIL in st.secrets:
    Entrez.email = st.secrets[ENTREZ_EMAIL]
else:
    Entrez.email = os.environ.get(ENTREZ_EMAIL, "")


def search(database: str, term: str) -> List[int]:
    """Get the List of UIDs matching the Entrez query.

    This function searches the provided NCBI database and returns the list of UIDs matching the
    Entrez query.

    Args:
        database (str): Name of the Entrez database.
        term (str): Entrez text query.

    Returns:
        List[int]: A list of UIDs.
    """
    handle = Entrez.esearch(db=database, term=term, retmax=10000)
    uids = []
    if handle:
        record = Entrez.read(handle)
        uids = record["IdList"]

    return uids


def summary(database: str, ids: Union[int, List[int]]) -> DictionaryElement:
    """Get the document summaries for the input UIDs.

    This function returns the document summaries for the input list of UIDs and datasource.

    Args:
        database (str): Name of the Entrez database.
        term (str): Entrez text query.

    Returns:
        : A list of UIDs.
    """
    handle = Entrez.esummary(db=database, id=ids, retmax=10000)
    if handle:
        record = Entrez.read(handle)
        handle.close()
    return record


def parse_summary(document_summaries: ListElement) -> List[Dict[str, str]]:
    """Get the document summaries for the input UIDs.

    This function returns the document summaries for the input list of UIDs and datasource.

    Args:

    Returns:
    """
    parsed_summaries = []
    for document_summary in document_summaries:
        parsed_summaries.append(
            {key: document_summary.get(key, None) for key in SUMMARY_FIELDS}
        )
    return parsed_summaries


def fetch(database: str, ids: Union[int, List[int]]) -> str:
    """Download the document summaries for the input UIDs.

    This function downloads the document summaries for the input list of UIDs and datasource.

    Args:

    Returns:
    """
    handle = Entrez.efetch(db=database, id=ids, retmax=10000, rettype="fasta")
    if handle:
        sequence_records = SeqIO.parse(handle, "fasta")
        records_written = SeqIO.write(
            sequence_records, os.path.join(outdir, "example.fasta"), "fasta"
        )
        print(f"Successfully downloaded {records_written} records")
        record = "File Downloaded Successfully!"
        handle.close()
    return record
