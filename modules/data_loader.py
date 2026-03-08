import pandas as pd

def load_file(file):

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)

    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)

    else:
        raise ValueError("Unsupported file type")

    # standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df