Practical 04 - Noise Elimination, Feature Selection, and EDA
=============================================================

OBJECTIVE
---------
Remove outliers ("noise") from a dataset, drop constant/low-variance
features, and run basic exploratory data analysis (summary stats,
correlation, histograms, boxplots).

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas, numpy, matplotlib, scikit-learn


WHAT THE CODE DOES
-------------------
1. Builds a small sample dataset with one clear outlier (Age=100) and one
   constant column.
2. Removes the outlier using the IQR (Interquartile Range) method.
3. Uses scikit-learn's VarianceThreshold to drop the constant column.
4. Prints dataset info, a statistical summary, and a correlation matrix.
5. Saves a histogram and a boxplot of the cleaned features as PNG files.

OUTPUT
------
- output/console_output.txt : full console output (actual, executed).
- output/histogram.png       : histograms of Age, Marks, Attendance.
- output/boxplot.png         : boxplot of the same features.


