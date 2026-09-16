"""
Practical 03: Handling Missing Values, Duplicate Records, and Data Normalization
---------------------------------------------------------------------------
Uses Pandas to:
1. Fill missing values (Age/Marks with mean, Name with 'Unknown')
2. Remove duplicate rows
3. Normalize numeric columns using Min-Max scaling
"""

import pandas as pd

# -----------------------------
# Sample Data
# -----------------------------
data = {
    'Name': ['Amit', 'Riya', 'Amit', 'Neha', None],
    'Age': [22, 24, 22, None, 26],
    'Marks': [85, 90, 85, 78, None]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# -----------------------------
# 1. Handling Missing Values
# -----------------------------
print("\nHandling Missing Values...")

df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Marks'] = df['Marks'].fillna(df['Marks'].mean())
df['Name'] = df['Name'].fillna('Unknown')

print(df)

# -----------------------------
# 2. Removing Duplicate Rows
# -----------------------------
print("\nRemoving Duplicates...")

df = df.drop_duplicates()

print(df)

# -----------------------------
# 3. Data Normalization (Min-Max)
# Formula: (x - min) / (max - min)
# -----------------------------
print("\nNormalizing Age and Marks...")

df['Age_Normalized'] = (df['Age'] - df['Age'].min()) / (df['Age'].max() - df['Age'].min())
df['Marks_Normalized'] = (df['Marks'] - df['Marks'].min()) / (df['Marks'].max() - df['Marks'].min())

print(df)

print("\nFinal Processed Data:")
print(df)

# Save the final cleaned data so it can be inspected as a file too
df.to_csv("output/cleaned_data.csv", index=False)
print("\nSaved cleaned data to output/cleaned_data.csv")
