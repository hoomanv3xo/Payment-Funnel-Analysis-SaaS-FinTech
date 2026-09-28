import pandas as pd
import glob

files = glob.glob('*.csv')
print("Files:", files)

for f in sorted(files):
    df = pd.read_csv(f)
    print(f"=== {f} ===")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(2))
    print()