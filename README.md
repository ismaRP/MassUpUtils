# MassUpUtils
Scripts for spectra .csv formatting and .muc XML creation.

Download and do:
```bash
chmod u+x tsv_to_csv.sh
chmod u+x create_muc.py
```

## Usage
```bash
./tsv_to_csv.sh -i path/maldi_spectra -o path/maldi_spectra_csv -t true
```
```bash
./create_muc.py -s path/maldi_spectra_csv -t path/sample_table.csv --type RAW Spectra -o path/file.muc
```
