import os

from tqdm import tqdm

from mylib.spider import LocalGovernmentCode as GovCode


def main():
    # Init
    output_dir: str = "./input"
    output_path: str = f"{output_dir}/gov_code.tsv"
    os.makedirs(output_dir, exist_ok=True)
    gc = GovCode()
    pref_codes: range = range(1, 48)
    
    # Get the local gov codes
    for pref_code in tqdm(pref_codes):
        gc.get_code(pref_code=pref_code)
    
    # Output
    gc.output(path=output_path, sep="\t", index=False)


if __name__ == "__main__":
    main()
