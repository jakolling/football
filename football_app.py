import streamlit as st  
import pandas as pd  
import numpy as np  
import plotly.graph_objects as go  
import plotly.express as px  
  
st.set_page_config(page_title="Football Analytics", layout="wide")  
  
# Initialize session state  
if 'df' not in st.session_state:  
    # Sample data  
    np.random.seed(42)  
    n_players = 100  
    st.session_state.df = pd.DataFrame({  
        'Player': [f'Player {i}' for i in range(n_players)],  
        'Team': np.random.choice(['Team A', 'Team B', 'Team C'], n_players),  
        'Position': np.random.choice(['Forward', 'Midfielder', 'Defender'], n_players),  
        'Goals': np.random.randint(0, 30, n_players),  
        'Assists': np.random.randint(0, 20, n_players),  
        'Passes': np.random.randint(500, 2000, n_players),  
        'Pass_Accuracy': np.random.uniform(60, 95, n_players),  
        'Tackles': np.random.randint(10, 100, n_players),  
        'Interceptions': np.random.randint(10, 100, n_players)  
    })  
  
# Sidebar  
st.sidebar.header("Filters")  
uploaded_file = st.sidebar.file_uploader("Upload Data", type=['csv', 'xlsx'])  
  
if uploaded_file is not None:  
    try:  
        if uploaded_file.name.endswith('.csv'):  
            st.session_state.df = pd.read_csv(uploaded_file)  
        else:  
            st.session_state.df = pd.read_excel(uploaded_file)  
    except Exception as e:  
        st.error(f"Error loading file: {str(e)}")  
  
df = st.session_state.df  
  
# Filters  
positions = st.sidebar.multiselect("Positions", df['Position'].unique(), df['Position'].unique())  
teams = st.sidebar.multiselect("Teams", df['Team'].unique(), df['Team'].unique())  
  
filtered_df = df[  
    (df['Position'].isin(positions)) &  
    (df['Team'].isin(teams))  
]  
  
# Main content  
st.title("Football Player Analysis")  
  
tab1, tab2, tab3 = st.tabs(["Player Comparison", "Performance Charts", "Data View"])  
  
with tab1:  
    st.subheader("Player Comparison")  
    col1, col2 = st.columns(2)  
      
    with col1:  
        player1 = st.selectbox("Select Player 1", filtered_df['Player'].unique())  
    with col2:  
        player2 = st.selectbox("Select Player 2", filtered_df['Player'].unique())  
          
    metrics = ['Goals', 'Assists', 'Passes', 'Pass_Accuracy', 'Tackles', 'Interceptions']  
      
    if player1 and player2:  
        p1_data = filtered_df[filtered_df['Player'] == player1][metrics].iloc[0]  
        p2_data = filtered_df[filtered_df['Player'] == player2][metrics].iloc[0]  
          
        fig = go.Figure()  
        fig.add_trace(go.Scatterpolar(r=p1_data.values, theta=metrics, fill='toself', name=player1))  
        fig.add_trace(go.Scatterpolar(r=p2_data.values, theta=metrics, fill='toself', name=player2))  
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(p1_data.max(), p2_data.max())])),  
                         showlegend=True)  
          
        st.plotly_chart(fig, use_container_width=True)  
  
with tab2:  
    st.subheader("Performance Charts")  
    chart_type = st.selectbox("Select Chart Type", ["Bar", "Scatter"])  
      
    if chart_type == "Bar":  
        metric = st.selectbox("Select Metric", metrics)  
        fig = px.bar(filtered_df.nlargest(10, metric),   
                    x='Player', y=metric,  
                    color='Team',  
                    title=f'Top 10 Players by {metric}')  
        st.plotly_chart(fig, use_container_width=True)  
          
    else:  
        x_metric = st.selectbox("X-Axis Metric", metrics)  
        y_metric = st.selectbox("Y-Axis Metric", metrics)  
          
        fig = px.scatter(filtered_df,  
                        x=x_metric, y=y_metric,  
                        color='Team',  
                        hover_data=['Player'],  
                        title=f'{y_metric} vs {x_metric}')  
        st.plotly_chart(fig, use_container_width=True)  
  
with tab3:  
    st.subheader("Data View")  
    st.dataframe(filtered_df)  
      
    ▍
