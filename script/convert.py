import tabula
import numpy as np
import pandas as pd


def isNan(value):
    return_val = True
    try:
        return_val = np.isnan(value)
    except:
        return_val = False
    return return_val


def clean_df(frame):
    # Initialize empty dataframe
    new_frame = pd.DataFrame()
    # Iterate over columns
    for (colName, data) in frame.iteritems():
        # Initialize empty Series
        series = pd.Series([], dtype=str)
        # Iterate over values
        for index, value in data.items():
            if isNan(value):
                continue
            if isinstance(value, str):
                series = series.append(
                    pd.Series(value.split("\r")), ignore_index=True)
            else:
                # Convert value to string, then to series, then append
                series = series.append(pd.Series([str(value)]))
        if new_frame.empty == True:
            new_frame = series.reset_index(drop=True)
        else:
            new_frame = pd.concat(
                [new_frame, series.reset_index(drop=True)], axis=1)
    return new_frame


def convert_to_csv(pdf_path, output_path):
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

    bigger_frame = clean_df(raw_df.iloc[0:, 0:3])
    smaller_frame = clean_df(raw_df.iloc[0:, 3:])

    # Swap if big is not big
    if len(bigger_frame) < len(smaller_frame):
        temp = bigger_frame
        bogger_frame = smaller_frame
        smaller_frame = bigger_frame

    # Renaming smaller frame's last row index to bigger frame's last row index to facilitate a correct join
    smaller_frame = smaller_frame.rename(
        index={(len(smaller_frame)-1): (len(bigger_frame)-1)})

    final_frame = pd.concat([bigger_frame, smaller_frame], axis=1)

    header = final_frame.iloc[0]
    header.reset_index(drop=True)
    final_frame_data = (final_frame.iloc[1:]).reset_index(drop=True)
    final_frame_data.columns = header

    final_frame_data.to_csv((output_path + "/Output.csv"), index=False)
