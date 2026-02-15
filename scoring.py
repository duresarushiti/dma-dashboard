import pandas as pd

# Scoring dictionary
score_dict = {
    'Yes': 1,
    'No': 0,
    'Not used': 0,
    'Consider to use': 1,
    'Testing': 2,
    'Implementing': 3,
    'Operational': 4,
    'Partially': 0.5
}

# Dimension mappings with descriptive names
dimensions = {
    'Digital Business Strategy': ['Digital Strategy Defined', 'Digital Strategy Implemented'],
    'Digital Readiness': ['Employees Trained in Digital Skills', 'Remote Work Infrastructure', 'Digital Tools Adoption'],
    'Human-Centric Digitalisation': ['User Experience Priority', 'Employee Well-being Monitoring'],
    'Data Governance': ['Data Security Measures', 'Data Usage for Decision Making'],
    'Automation & AI': ['AI and Automation Usage'],
    'Green Digitalisation': ['Sustainability in Digitalization']
}

# Flatten list of questions for easy access
all_questions = [q for qs in dimensions.values() for q in qs]

def compute_scores(df):
    """
    Computes dimension scores and overall maturity for a given DataFrame.
    Assumes proper column names exist.
    """
    try:
        # Check if required columns exist
        missing_cols = [col for col in all_questions if col not in df.columns]
        if missing_cols:
            # Fallback for old data format (Q1..Q11) if mixing versions, or just error
            # For this assignment, we assume the data follows the new format.
            raise ValueError(f"Missing columns in input data: {missing_cols}")

        # Add score columns for each Question
        for q in all_questions:
            # Create a score column, e.g., 'Digital Strategy Defined_score'
            df[f'{q}_score'] = df[q].map(score_dict).fillna(0)

        # Compute dimension scores
        for dim, qs in dimensions.items():
            # Average score of questions in this dimension * 25 (to scale 0-4 to 0-100)
            score_cols = [f'{q}_score' for q in qs]
            df[f'{dim}_score'] = df[score_cols].mean(axis=1) * 25

        # Overall maturity
        df['Overall_Maturity'] = df[[f'{dim}_score' for dim in dimensions]].mean(axis=1)

        return df

    except Exception as e:
        print(f"Error in compute_scores: {e}")
        return df # Return original df or raise, depending on preference. Here returning potentially incomplete df.
