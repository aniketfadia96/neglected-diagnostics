import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from app.common.constants import NCBI_DF_FILTER


def _preprocessing(df: pd.DataFrame):
    """Preprocess the NCBI dataframe before filtering.

    This function performs preprocessing tasks on the given DataFrame. The preprocessing includes converting specific columns to categorical data type and converting date objects to datetime format.

    Parameters
    ----------
    df : pd.DataFrame
        The original DataFrame to be preprocessed.

    Returns
    -------
    pd.DataFrame
        The DataFrame after preprocessing.

    Notes
    -----
    The function modifies the DataFrame in-place and does not return a new DataFrame. Instead, it modifies the columns directly in the input DataFrame.

    The following preprocessing steps are performed:
    1. The "Species," "TaxId," "Id," "Gi," and "Status" columns are converted to categorical data type.
    2. The "CreateDate" and "UpdateDate" columns are converted to datetime format.
    """
    # Convert columns to categorical
    df["Species"] = df["Species"].astype("category")
    df["TaxId"] = df["TaxId"].astype("category")
    df["Id"] = df["Id"].astype("category")
    df["Gi"] = df["Gi"].astype("category")
    df["Status"] = df["Status"].astype("category")

    # Convert Date objects to Datetime format
    date_strings = [str(date_element) for date_element in df["CreateDate"]]
    df["CreateDate"] = pd.to_datetime(date_strings, format="%Y/%m/%d")

    date_strings = [str(date_element) for date_element in df["UpdateDate"]]
    df["UpdateDate"] = pd.to_datetime(date_strings, format="%Y/%m/%d")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter a DataFrame based on user-selected criteria.

    This function adds a user interface (UI) to allow users to interactively filter the data based on the selected columns and their corresponding values. The function provides different filtering options depending on the data type of the columns.

    Parameters
    ----------
    df : pd.DataFrame
        The original DataFrame to be filtered.

    Returns
    -------
    pd.DataFrame
        The filtered DataFrame based on the user-selected criteria.

    Notes
    -----
    The function supports filtering based on the following data types in DataFrame columns:
    - Categorical columns: Allows users to select specific category values to filter on.
    - Numeric columns: Enables filtering based on minimum and maximum numeric values.
    - Datetime columns: Provides a date range selector for filtering based on date values.
    - Text columns: Supports filtering based on substrings or regular expressions.
    """
    st.session_state[NCBI_DF_FILTER] = st.checkbox("Add filters")

    if st.session_state[NCBI_DF_FILTER] is False:
        return df

    df = df.copy()
    _preprocessing(df)

    filter_container = st.container()
    with filter_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")

            if is_categorical_dtype(df[column]):
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                with right:
                    # Create a sub column layout
                    sub_columns = st.columns(2)
                    # Add input boxes for minimum and maximum values in the row
                    with sub_columns[0]:
                        min_length = st.number_input("Enter Minimum")

                    with sub_columns[1]:
                        max_length = st.number_input("Enter Maximum")
                df = df[df[column].between(min_length, max_length)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
