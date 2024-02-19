# test_date_converter_pytest.py
import pandas as pd
import pytest
from date_conversion_function import convert_date_columns

def test_columns_with_date_converted():
    """Test columns with 'Date' are correctly converted to datetime."""
    data = {
        'StartDate': ['2023-01-01', '2023-01-02'],
        'EndDate': ['2023-02-01', '2023-02-02'],
        'strings': ['test1', 'test2']
    }
    df = pd.DataFrame(data)
    
    # Convert date columns
    converted_df = convert_date_columns(df)
    
    # Assert 'StartDate' and 'EndDate' columns are converted to datetime
    assert pd.api.types.is_datetime64_any_dtype(converted_df['StartDate'])
    assert pd.api.types.is_datetime64_any_dtype(converted_df['EndDate'])
    
    # Assert 'NotADate' column remains unchanged
    assert not pd.api.types.is_datetime64_any_dtype(converted_df['strings'])

def test_error_raised_no_date_columns():
    """Test that an error is raised if no columns contain 'Date'."""
    data = {'Name': ['Alice', 'Bob'], 'Age': [30, 25]}
    df = pd.DataFrame(data)
    
    with pytest.raises(ValueError):
        convert_date_columns(df)
