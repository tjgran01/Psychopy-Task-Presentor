from scipy.io import savemat
import os
import pandas as pd
import datetime

def main():

    test_f = f"{os.getcwd()}/../data/trigger_data/2021-09-07/XXXX_trigger_data_2021-09-07_18_34_54_923789.csv"
    df = pd.read_csv(test_f)
    events = df["trigger_string"].unique().tolist()

    for e in events:
        

if __name__ == "__main__":
    main()
