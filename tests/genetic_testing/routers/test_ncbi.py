"""Test NCBI Functions.

This module will test NCBI functionalities like search, summary, and fetch.

"""

from http.client import HTTPResponse
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from genetic_testing.routers import ncbi
from genetic_testing.routers.ncbi import RETMAX, RETMODE, RETTYPE

SAMPLE_FASTA_DATA = ">OQ443159.1 Panthera onca isolate 4766 large subunit ribosomal RNA gene, partial sequence; mitochondrial CATTTGTTCCT"


@pytest.fixture
def mock_esearch_result():
    """Mock the return value of the `Bio.Entrez.esearch` function"""
    return {"IdList": ["1"]}


@pytest.fixture
def mock_esummary_result():
    """Mock the return value of the `Bio.Entrez.esummary` function"""
    return [
        {
            "Item": [],
            "Id": "1",
            "Caption": "DQ009076",
            "Title": "Panthera Onca",
            "Extra": "gi|63020693|gb|DQ009076.1|[63020693]",
            "Gi": 63020693,
            "CreateDate": "2005/05/08",
            "UpdateDate": "2005/05/08",
            "Flags": 0,
            "TaxId": 5811,
            "Length": 210,
            "Status": "live",
            "ReplacedBy": "",
            "Comment": "  ",
            "AccessionVersion": "DQ009076.1",
        }
    ]


@patch("Bio.Entrez.esearch")
@patch("Bio.Entrez.esummary")
@patch("Bio.Entrez.Parser.DataHandler.read")
def test_get_data(
    mock_parser_read: MagicMock,
    mock_esummary: MagicMock,
    mock_esearch: MagicMock,
    mock_esearch_result,
    mock_esummary_result,
):
    """Unit Test for get_data Function

    This test case verifies the behavior of the get_data() function by mocking the required dependencies and checking the expected output.

    Parameters
    ----------
    mock_parser_read : MagicMock
        A mock object representing the `DataHandler.read` method from the `Bio.Entrez.Parser` module.
    mock_esummary : MagicMock
        A mock object representing the `Bio.Entrez.esummary` function.
    mock_esearch : MagicMock
        A mock object representing the `Bio.Entrez.esearch` function.
    mock_esearch_result : dict
        The predefined result of the `DataHandler.read` method for the API call using `Bio.Entrez.esearch` function.
    mock_esummary_result : dict
        The predefined result of the of the `DataHandler.read` method for the API call using `Bio.Entrez.esummary` function.
    """
    mock_esearch.return_value = MagicMock(spec=HTTPResponse)
    mock_esummary.return_value = MagicMock(spec=HTTPResponse)
    mock_parser_read.side_effect = [mock_esearch_result, mock_esummary_result]

    df_summary = ncbi.get_data("database", "search_term")

    assert (len(df_summary)) == len(mock_esummary_result)

    for i, row in df_summary.iterrows():
        for column in ncbi.NCBI_SUMMARY_FIELDS:
            assert column in row, f"Column '{column}' not found in row {i}"

            assert (
                row[column] == mock_esummary_result[0][column]
            ), f"Column '{column}' in row {i} does not match with the expected input"

    # Assert that the mock functions were called with the correct arguments
    mock_esearch.assert_called_once_with(
        db="database", term="search_term", retmax=RETMAX
    )
    mock_esummary.assert_called_once_with(db="database", id=["1"], retmax=RETMAX)
    mock_parser_read.assert_called()


@patch("Bio.Entrez.efetch")
def test_download_data(mock_efetch: MagicMock):
    mock_efetch.return_value = StringIO(SAMPLE_FASTA_DATA)
    sequences_str_buffer = ncbi.fetch_data("database", [1])
    # Verify that the result is a StringIO object
    assert isinstance(sequences_str_buffer, StringIO)
    # Assert that the Bio.Entrez.efetch function was called with the correct arguments
    mock_efetch.assert_called_once_with(
        db="database", id=[1], retmax=RETMAX, rettype=RETTYPE, retmode=RETMODE
    )
