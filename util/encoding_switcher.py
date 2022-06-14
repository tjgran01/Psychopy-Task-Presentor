import os

# Switches encoding from utf-8 to utf-16

def main():
    
    F_DIR = "../resources/episodic_prospection_trials/practice/"
    OUT_DIR = "../instructions/encoded"
    for fname in os.listdir(F_DIR):
        if fname.endswith(".csv"):
            with open(f"{F_DIR}{fname}", 'rb') as in_f:
                with open(f"{F_DIR}/{fname}", 'wb') as out_f:
                    contents = in_f.read()
                    out_f.write(contents.decode('utf-8').encode('utf-16'))
                    print(f"written to {F_DIR}")

if __name__ == "__main__":
    main()