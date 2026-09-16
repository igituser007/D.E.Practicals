"""
Practical 04: Noise Elimination, Feature Selection, and Exploratory Data Analysis (EDA)
----------------------------------------------------------------------------------
Uses Pandas, NumPy, Matplotlib, and Scikit-learn to:
1. Remove outliers ("noise") using the IQR method
2. Remove constant / low-variance features
3. Explore the cleaned dataset (info, summary stats, correlation, plots)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # so plots can be saved without a display
import matplotlib.pyplot as plt
from sklearn.feature_selection import VarianceThreshold

# -----------------------------
# Sample Dataset
# -----------------------------
data = {
    'Age': [20, 21, 22, 23, 24, 100],       # 100 is an outlier (noise)
    'Marks': [75, 80, 85, 90, 95, 20],
    'Attendance': [85, 88, 90, 92, 94, 50],
    'Constant': [1, 1, 1, 1, 1, 1]           # Constant feature
}

df = pd.DataFrame(data)

print("Original Dataset:")
print(df)

# =====================================
# 1. Noise Elimination (Outlier Removal)
# =====================================
Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df_clean = df[(df['Age'] >= lower) & (df['Age'] <= upper)]

print("\nDataset after Noise Elimination:")
print(df_clean)

# =====================================
# 2. Feature Selection
# Remove constant or low-variance features
# =====================================
selector = VarianceThreshold(threshold=0.0)
selector.fit_transform(df_clean)

selected_columns = df_clean.columns[selector.get_support()]

print("\nSelected Features (after removing constant columns):")
print(list(selected_columns))

df_selected = df_clean[selected_columns]

# =====================================
# 3. Exploratory Data Analysis (EDA)
# =====================================
print("\nDataset Information:")
df_selected.info()

print("\nStatistical Summary:")
print(df_selected.describe())

print("\nCorrelation Matrix:")
print(df_selected.corr())

# Histogram
df_selected.hist(figsize=(8, 6))
plt.suptitle("Histogram of Features")
plt.tight_layout()
plt.savefig("output/histogram.png")
plt.close()

# Boxplot
df_selected.boxplot(figsize=(8, 5))
plt.title("Boxplot of Dataset")
plt.tight_layout()
plt.savefig("output/boxplot.png")
plt.close()

print("\nSaved histogram.png and boxplot.png to the output folder.")
