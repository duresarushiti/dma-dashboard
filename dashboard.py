import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scoring import compute_scores, dimensions
import os

# Set page config
st.set_page_config(page_title="Digital Maturity Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        if not os.path.exists('data/rawdma_before.xlsx') or not os.path.exists('data/rawdma_after.xlsx'):
            st.error("Data files not found in data/ directory. Please run data_generator.py first.")
            return None, None
            
        df_before = pd.read_excel('data/rawdma_before.xlsx')
        df_after = pd.read_excel('data/rawdma_after.xlsx')
        df_before = compute_scores(df_before)
        df_after = compute_scores(df_after)
        return df_before, df_after
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df_before, df_after = load_data()

if df_before is not None and df_after is not None:
    # Title
    st.title("Digital Maturity Assessment Dashboard")

    # Layout: Top metrics
    col1, col2, col3 = st.columns(3)
    
    avg_maturity = df_after['Overall_Maturity'].mean()
    avg_improvement = (df_after['Overall_Maturity'] - df_before['Overall_Maturity']).mean()
    
    with col1:
        st.metric("Avg Maturity Score", f"{avg_maturity:.1f}")
    with col2:
        st.metric("Avg Improvement", f"+{avg_improvement:.1f}")
    with col3:
        st.metric("Companies Assessed", len(df_after))

    # Overall maturity gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_maturity,
        title={'text': "Average Overall Maturity"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Main interaction area
    st.subheader("Company Analysis")
    
    companies = df_after['Company_ID'].tolist()
    selected_company = st.selectbox("Select Company ID to View Detail", companies)

    if selected_company:
        row = df_after[df_after['Company_ID'] == selected_company]
        
        # Radar chart
        scores = [row[f'{dim}_score'].values[0] for dim in dimensions.keys()]
        labels = list(dimensions.keys())

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=labels,
            fill='toself'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title=f"Maturity Profile: Company {selected_company}"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Advanced Analysis
    st.markdown("---")
    st.subheader("Strategic Insights")
    
    col_hz1, col_hz2 = st.columns(2)
    
    with col_hz1:
        # Correlation heatmap
        dim_cols = [f'{dim}_score' for dim in dimensions.keys()]
        corr = df_after[dim_cols].corr()
        fig_heatmap = px.imshow(corr, text_auto=True, title="Dimension Correlations")
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
    with col_hz2:
        # Regression / Impact info
        st.info("Regression Analysis shows equal contribution from all dimensions due to the averaging scoring model. In real-world scenarios, this would highlight which dimensions drive overall maturity most.")

    # Leaderboards
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 Top 10 Performers")
        top10_best = df_after.nlargest(10, 'Overall_Maturity')[['Company_ID', 'Overall_Maturity']]
        st.dataframe(top10_best, hide_index=True)
        
    with c2:
        st.subheader("⚠️ Bottom 10 Performers")
        top10_worst = df_after.nsmallest(10, 'Overall_Maturity')[['Company_ID', 'Overall_Maturity']]
        st.dataframe(top10_worst, hide_index=True)
