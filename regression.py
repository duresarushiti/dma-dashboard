import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scoring import compute_scores, dimensions
import os

def run_regression():
    try:
        # Check if file exists
        if not os.path.exists('data/rawdma_after.xlsx'):
             raise FileNotFoundError("Input file data/rawdma_after.xlsx not found.")

        # Load after data (as it's the improved state)
        df = pd.read_excel('data/rawdma_after.xlsx')
        df = compute_scores(df)

        if 'Overall_Maturity' not in df.columns:
             raise ValueError("Scoring failed. Dependencies missing.")

        # Features and target
        # Dynamically build feature list from dimensions
        feature_cols = [f'{dim}_score' for dim in dimensions.keys()]
        X = df[feature_cols]
        y = df['Overall_Maturity']

        # Fit model
        model = LinearRegression()
        model.fit(X, y)

        # Predictions
        y_pred = model.predict(X)

        # R²
        r2 = r2_score(y, y_pred)

        # Coefficients
        coefficients = dict(zip(X.columns, model.coef_))

        print(f"R² Score: {r2:.3f}")
        print("Coefficients:")
        for dim, coef in coefficients.items():
            print(f"{dim}: {coef:.3f}")

        # Interpretation: Dimensions with higher coefficients have greater impact on overall maturity.
        # Note: Since Overall Maturity is an exact average of dimensions, R2 will be 1.0 and coefs should be equal (1/6).

    except Exception as e:
        print(f"Error in regression analysis: {e}")

if __name__ == "__main__":
    run_regression()
