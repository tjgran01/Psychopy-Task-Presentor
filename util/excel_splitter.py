import pandas as pd
import os

def main():

    fpaths = [f"{os.getcwd()}/resources/raw/nonsocial_scenarios.xlsx", f"{os.getcwd()}/resources/raw/social_scenarios.xlsx"]
    EXPORT_FPATH = "resources/"

    for fpath in fpaths:

        fname = "social_self_control_trials.csv"
        if "nonsocial" in fpath:
            fname = "non_social_self_control_trials.csv"

        ex_trials = pd.read_excel(fpath, sheet_name="experiment")
        prac_trials = pd.read_excel(fpath, sheet_name="exercise")
        ex_trials.to_csv(f"{os.getcwd()}/{EXPORT_FPATH}{fname[:-4]}/{fname}", index=False)
        prac_trials.to_csv(f"{os.getcwd()}/{EXPORT_FPATH}{fname[:-4]}/practice/{fname}", index=False)


if __name__ == "__main__":
    main()