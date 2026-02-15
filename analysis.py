import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scoring import compute_scores, dimensions
import os

def run_analysis():
    try:
        # Check if files exist
        if not os.path.exists('data/rawdma_before.xlsx') or not os.path.exists('data/rawdma_after.xlsx'):
            raise FileNotFoundError("Input Excel files not found in data/ directory. Please run data_generator.py first.")
        
        # Ensure images directory exists
        if not os.path.exists('images'):
            os.makedirs('images')

        # Load data
        df_before = pd.read_excel('data/rawdma_before.xlsx')
        df_after = pd.read_excel('data/rawdma_after.xlsx')

        # Apply scoring
        df_before = compute_scores(df_before)
        df_after = compute_scores(df_after)

        # check if scoring worked (i.e. if columns exist)
        if 'Overall_Maturity' not in df_before.columns:
            raise ValueError("Scoring failed: Overall_Maturity column missing.")

        # Merge for comparison
        df_comparison = pd.merge(df_before[['Company_ID', 'Overall_Maturity']], df_after[['Company_ID', 'Overall_Maturity']], on='Company_ID', suffixes=('_before', '_after'))

        # Calculate improvement
        df_comparison['Improvement'] = df_comparison['Overall_Maturity_after'] - df_comparison['Overall_Maturity_before']

        # Correlation matrix (using after data for dimensions)
        # Use dimensions from scoring.py to ensure consistency
        dim_cols = [f'{dim}_score' for dim in dimensions.keys()]
        corr_matrix = df_after[dim_cols].corr()

        # Visualizations
        plt.figure(figsize=(10, 8)) # Increased size for better readability
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix of Dimension Scores')
        plt.tight_layout()
        plt.savefig('images/correlation_heatmap.png')
        plt.close()

        # Before vs After bar chart (average maturity)
        avg_before = df_before['Overall_Maturity'].mean()
        avg_after = df_after['Overall_Maturity'].mean()
        plt.figure(figsize=(8, 6))
        plt.bar(['Before', 'After'], [avg_before, avg_after], color=['#1f77b4', '#2ca02c']) # Better colors
        plt.title('Average Overall Maturity Before vs After')
        plt.ylabel('Maturity Score (0-100)')
        plt.savefig('images/before_after_bar.png')
        plt.close()

        # Distribution plot
        plt.figure(figsize=(10, 6))
        sns.histplot(df_comparison['Improvement'], kde=True, color='purple')
        plt.title('Distribution of Maturity Improvements')
        plt.xlabel('Improvement Score')
        plt.tight_layout()
        plt.savefig('images/improvement_distribution.png')
        plt.close()

        print("Analysis completed. Analysis figures saved to images/ directory.")

    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    run_analysis()
