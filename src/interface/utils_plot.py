import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os # Library to auto-dectect the tab files automatically
from streamlit_theme import st_theme

def plot_durations(df_set):
    # Ensure the data is sorted by POLICY and DATETIME for proper processing
    df_set['DATETIME'] = pd.to_datetime(df_set['DATETIME'])
    df_set = df_set.sort_values(by=['POLICY', 'DATETIME'])

    # Group by POLICY and detect consecutive leaks
    df_set['LEAK_GROUP'] = (df_set['LEAK'] != df_set['LEAK'].shift()).cumsum()  # Identify groups of leaks
    leak_groups = df_set[df_set['LEAK'] == 1].groupby(['POLICY', 'LEAK_GROUP']).agg({
        'DATETIME': ['min', 'max'],  # Leak start and end
        'LEAK': 'size'  # Leak duration
    }).reset_index()

    # Flatten the multi-level columns after aggregation
    leak_groups.columns = ['POLICY', 'LEAK_GROUP', 'START_DATETIME', 'END_DATETIME', 'DURATION']
    leak_groups['DURATION'] += 3

    # Create a summary of leaks by duration
    leak_summary = leak_groups.groupby('DURATION').size().reset_index(name='NUM_LEAKS')
    leak_summary['NORM'] = leak_summary['DURATION'] ** 0.1

    dark = os.path.abspath(os.path.join(os.path.dirname(__file__), 'aiguastyle.mplstyle'))
    light = os.path.abspath(os.path.join(os.path.dirname(__file__), 'classic.mplstyle'))
    # Use dark theme from matplotlib
    theme = st_theme()
    print(theme['base'])
    # Set matplotlib style based on theme
    if theme['base'] == 'dark':
        plt.style.use(dark)  # Use dark theme
    else:
        plt.style.use(light)  # Use default light theme
    

    # Create a figure for multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(20, 16), facecolor='#0e1117')  # Adjust the size for more plots
    axes = axes.flatten()  # Flatten axes array for easy indexing



    # Plot 1: Histogram of Leak Durations
    sns.barplot(x='DURATION', y='NUM_LEAKS', data=leak_summary, hue='NORM', palette='Blues_d', dodge=False, legend=False, ax=axes[0])
    axes[0].set_xlabel('Leak Duration (Number of Rows)', fontsize=12)
    axes[0].set_ylabel('Number of Leaks', fontsize=12)
    axes[0].set_title('Histogram of Leak Durations', fontsize=14)
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Bar chart of leaks by start hour
    leak_start_hours = df_set[df_set['LEAK'] == 1].groupby(['START_HOUR']).size().reset_index(name='NUM_LEAKS')
    sns.barplot(x='START_HOUR', y='NUM_LEAKS', data=leak_start_hours, color='skyblue', edgecolor='black', ax=axes[1])
    axes[1].set_xlabel('Start Hour', fontsize=12)
    axes[1].set_ylabel('Number of Leaks', fontsize=12)
    axes[1].set_title('Number of Leaks by Start Hour', fontsize=14)
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 3: Pie chart of leaks by Usage
    leak_usage = df_set[df_set['LEAK'] == 1].groupby(['USAGE']).size().reset_index(name='NUM_LEAKS')
    cmap = plt.cm.Blues
    start_color = 0.9
    end_color = 0.5
    axes[2].pie(leak_usage['NUM_LEAKS'], labels=leak_usage['USAGE'], autopct="%1.1f%%", startangle=140, colors=cmap(np.linspace(start_color, end_color, len(leak_usage))))
    axes[2].axis('equal')
    axes[2].set_title('Number of Leaks by Usage', fontsize=14)

    # Plot 4: Pie chart of leaks by Housing
    leak_housing = df_set[df_set['LEAK'] == 1].groupby(['HOUSING']).size().reset_index(name='NUM_LEAKS')
    axes[3].pie(leak_housing['NUM_LEAKS'], labels=leak_housing['HOUSING'], autopct="%1.1f%%", startangle=140, colors=cmap(np.linspace(start_color, end_color, len(leak_housing))))
    axes[3].axis('equal')
    axes[3].set_title('Number of Leaks by Housing', fontsize=14)

    # Adjust layout and show the figure
    plt.tight_layout()
    # Display the figure in Streamlit
    st.pyplot(fig)
