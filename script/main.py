import tabula
import numpy as np
import pandas as pd

pdf_path = "./Balsheet.pdf"

# Read PDF and convert to data frame
raw_df = tabula.read_pdf("BalSheet.pdf", pages='all')
raw_df = pd.DataFrame(raw_df)

# Extract only the first cell
raw_df = raw_df.iloc[0, 0]

# Transposing values
raw_df.iloc[2, 5] = raw_df.iloc[2, 4]
raw_df.iloc[2, 4] = raw_df.iloc[2, 3]
raw_df.iloc[2, 3] = np.nan
raw_df.iloc[3, 5] = raw_df.iloc[3, 4]
raw_df.iloc[3, 4] = raw_df.iloc[3, 3]
raw_df.iloc[3, 3] = np.nan


def isNan(value):
    return_val = True
    try:
        return_val = np.isnan(value)
    except:
        return_val = False
    return return_val


def clean_df(frame):
    # Iterate over columns
    for (colName, data) in frame.iteritems():
        # Iterate over values
        series = pd.Series([], dtype=str)
        for index, value in data.items():
            if isNan(value):
                continue
            if isinstance(value, str):
                series = series.append(
                    pd.Series(value.split("\r")), ignore_index=True)
            else:
                # Convert value to string, then to series, then append
                series = series.append(pd.Series([str(value)]))
        print(series)


clean_df(raw_df.iloc[0:, 0:3])
clean_df(raw_df.iloc[0:, 3:])
