import pandas as pd

# Load the CSV
df = pd.read_csv('raw_food.csv')

# Get unique names
unique_names = sorted(df['Name'].unique())

# Print them out to inspect
print(f"Total unique names: {len(unique_names)}")
for name in unique_names:
    print(name)
