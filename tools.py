from langchain_core.tools import tool
import pandas as pd
import streamlit as st
from typing import Any

# sleep_csv = st.file_uploader("Choose a csv file", type="csv", help="Upload a csv file with sleep data from fitbit")

# def parse_date(date_str):
#     date_format = "%Y-%m-%d %I:%M%p"
#     try:
#         return pd.to_datetime(date_str, format=date_format)
#     except ValueError:
#         return date_str
    
# df = pd.read_csv(sleep_csv, skiprows=1)
# df['Start Time'] = df['Start Time'].apply(parse_date)
# df['End Time'] = df['End Time'].apply(parse_date)
# @tool
# def graphAgent( x: str, y: str, df: Any):
#     """This functions creates a scatter chart with the given x and y values from the dataframe df that is passed in. x and y must be strings and from the dataframe that you are using, check the columns before using this function."""
#     pd = pd.DataFrame(df)
#     st.scatter_chart(df, x=x, y=y)