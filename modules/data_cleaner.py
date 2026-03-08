import pandas as pd

def clean_data(df):

    df = df.copy()

    num_cols = df.select_dtypes(include="number").columns
    txt_cols = df.select_dtypes(include="object").columns

    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    df[txt_cols] = df[txt_cols].fillna("Unknown")

    df.drop_duplicates(inplace=True)

    return df