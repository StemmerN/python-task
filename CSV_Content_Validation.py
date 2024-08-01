import pandas as pd

# Load the cleaned CSV file
vehicles_csv_path = "C:\\Users\\nikolais\\Documents\\python-task\\vehicles.csv"
vehicles_df = pd.read_csv(vehicles_csv_path, delimiter=';')

# Check for missing values and data consistency
print("Missing values in vehicles_cleaned.csv:")
print(vehicles_df.isnull().sum())

print("\nData preview:")
print(vehicles_df.head())

# Check for inconsistent rows
for i, row in vehicles_df.iterrows():
    if len(row) != len(vehicles_df.columns):
        print(f"Inconsistent row at index {i}: {row}")
