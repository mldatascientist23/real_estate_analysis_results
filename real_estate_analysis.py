import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
FILE_PATH = 'MAT 240 Real Estate Data.xlsx'
OUTPUT_IMAGE_PATH = 'scatterplot_with_regression.png'
OUTPUT_STATS_PATH = 'regression_stats.txt'
X_VAR = 'square feet'
Y_VAR = 'listing price'

try:
    # Read the Excel file, setting the header to the 5th row (index 4)
    df = pd.read_excel(FILE_PATH, sheet_name='project 1 data', header=4)

    # Clean up column names by stripping leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Select the required data range (rows 106 to 205 of the *original* Excel sheet)
    # Since the header is row 5, the first data row (row 6) is index 0.
    # Row 106 is index 100 (106 - 6 = 100)
    # Row 205 is index 199 (205 - 6 = 199)
    # We want indices 100 up to (but not including) 200.
    df_subset = df.iloc[100:200].copy()

    # Extract X and Y data
    X = df_subset[X_VAR]
    Y = df_subset[Y_VAR]

    # --- Linear Regression using numpy.polyfit ---
    # Fit a first-degree polynomial (linear regression)
    slope, intercept = np.polyfit(X, Y, 1)

    # Calculate R-squared (Coefficient of Determination)
    # 1. Calculate the predicted Y values
    Y_pred = slope * X + intercept
    # 2. Calculate the total sum of squares (SST)
    SST = np.sum((Y - np.mean(Y))**2)
    # 3. Calculate the residual sum of squares (SSR)
    SSR = np.sum((Y - Y_pred)**2)
    # 4. Calculate R-squared
    r_squared = 1 - (SSR / SST)

    # Regression line equation
    # Format the equation for display
    sign = "+" if intercept >= 0 else "-"
    equation = f'Y = {slope:.2f}X {sign} {abs(intercept):.2f}'
    r_squared_text = f'R² = {r_squared:.4f}'

    # Create the regression line data
    X_fit = np.linspace(X.min(), X.max(), 100)
    Y_fit = slope * X_fit + intercept

    # --- Plotting ---
    plt.figure(figsize=(10, 6))

    # Scatter plot
    plt.scatter(X, Y, color='blue', label='Data Points')

    # Trend line
    plt.plot(X_fit, Y_fit, color='red', label=f'Regression Line\n{equation}\n{r_squared_text}')

    # Labels and Title
    plt.title(f'Scatterplot of {Y_VAR.title()} vs {X_VAR.title()} (Rows 106-205)')
    plt.xlabel(X_VAR.title())
    plt.ylabel(Y_VAR.title())

    # Add the regression equation and R-squared to the plot
    plt.text(0.05, 0.95, f'Regression Equation: {equation}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    plt.text(0.05, 0.90, f'R-squared: {r_squared:.4f}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

    plt.legend(loc='lower right')
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save the plot
    plt.savefig(OUTPUT_IMAGE_PATH)
    print(f"Plot saved to {OUTPUT_IMAGE_PATH}")

    # --- Save Regression Statistics ---
    with open(OUTPUT_STATS_PATH, 'w') as f:
        f.write("--- Regression Analysis Statistics ---\n")
        f.write(f"Independent Variable (X): {X_VAR}\n")
        f.write(f"Dependent Variable (Y): {Y_VAR}\n")
        f.write(f"Data Range (Original Excel Rows): 106 to 205\n\n")
        f.write(f"Regression Equation: {equation}\n")
        f.write(f"Slope (Coefficient for X): {slope:.4f}\n")
        f.write(f"Intercept (Y-intercept): {intercept:.4f}\n")
        f.write(f"R-squared (Coefficient of Determination): {r_squared:.4f}\n")
        # Note: R-value, P-value, and Standard Error require scipy, which is unavailable.
        # We will proceed with the available statistics.

    print(f"Regression statistics saved to {OUTPUT_STATS_PATH}")

except Exception as e:
    print(f"An error occurred: {e}")
    # Print the column names for debugging if the error is related to column selection
    try:
        print(f"Available columns: {df.columns.tolist()}")
    except:
        pass
