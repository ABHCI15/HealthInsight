from langchain_core.tools import tool
import pandas as pd
import streamlit as st
from typing import Any


@tool
def graphAgent( x: str, df: Any):
    """This functions creates a scatter chart with the given x and y values from the dataframe df that is passed in. Make sure the x and y are proper strings of column names and it makes sense to plot them together in a meaningful way make sure they are actual column names. Use df.dict to pass in as df parameter.Y is time in bed."""
    st.scatter_chart(df, x=x, y="Time in Bed")