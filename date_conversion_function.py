import pandas as pd

def convert_date_columns(df):
    """
    Convert all columns in the DataFrame that include the word 'Date' (in any part of the header and case-insensitive)
    to datetime type. Raises an error if no such columns are found.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: The DataFrame with columns containing 'Date' converted to datetime type.
    """
    # Use a case-insensitive search for 'Date' in column names
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    
    # If no columns containing 'Date' are found, raise an error
    if not date_columns:
        raise ValueError("No columns containing 'Date' were found.")
    
    # Convert identified columns to datetime type
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    
    return df

# Example usage
# Assume 'df' is your DataFrame
# df = convert_date_columns(df)
