# Legal Simplifier

This project simplifies complex text using a dataset of input-output sentence pairs.

## Dataset Files
Place these files inside the `dataset/` folder:

- comp-simp1.csv
- comp-simp2.csv
- final.csv
- final_s.csv

## Required Columns
Each CSV file must contain:
- input
- output

## Run Training
```bash
python train.py