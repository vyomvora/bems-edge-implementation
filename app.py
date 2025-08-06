import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import time
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cloud.read_data_azure import AzureDataReader

st.set_page_config(page_title="BEMS-Edge Dashboard", layout="wide")

# Initialize Azure reader
@st.cache_resource
def init_azure_reader():
    return AzureDataReader("connection_string")

reader = init_azure_reader()

st.title("BEMS-Edge: Building Energy Management System")
st.subheader("Real time Hotspot Detection using Edge Computing")

# Get real data
data = reader.get_latest_data()
df = pd.DataFrame(data)

# Create metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    hotspots = df[df['is_hotspot'] == True].shape[0]
    st.metric("Active Hotspots", hotspots)

with col2:
    avg_edge_time = df['edge_processing_time_ms'].mean()
    st.metric("Average Edge Time", f"{avg_edge_time:.1f}ms")

with col3:
    avg_cloud_time = df['cloud_processing_time_ms'].mean()
    st.metric("Average Cloud Time", f"{avg_cloud_time:.0f}ms")

with col4:
    data_reduction = (1 - hotspots/len(df)) * 100
    st.metric("Data Reduction", f"{data_reduction:.0f}%")

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Real time Temperature Monitoring")
    
    # Create temperature chart
    fig = go.Figure()
    
    for _, row in df.iterrows():
        color = 'red' if row['is_hotspot'] else 'lightblue'
        fig.add_trace(go.Bar(
            x=[f"Room {row['room_id']}"], 
            y=[row['temperature']],
            name=f"Room {row['room_id']}",
            marker_color=color,
            text=f"{row['temperature']}°C",
            textposition='auto'
        ))
    
    # Add threshold line
    fig.add_hline(y=27, line_dash="dash", line_color="orange", 
                  annotation_text="Hotspot Threshold (27°C)")
    
    fig.update_layout(
        showlegend=False, 
        height=400,
        title="Current Room Temperatures",
        yaxis_title="Temperature (°C)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Room Status Table")
    
    # Create status dataframe
    status_df = df.copy()
    status_df['Room'] = 'Room ' + status_df['room_id'].astype(str)
    status_df['Temperature'] = status_df['temperature'].astype(str) + '°C'
    status_df['Status'] = status_df['is_hotspot'].apply(
        lambda x: 'Hotspot' if x else 'Normal'
    )
    status_df['Edge Time'] = status_df['edge_processing_time_ms'].astype(str) + 'ms'
    
    display_df = status_df[['Room', 'Temperature', 'Status', 'Edge Time']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# Performance comparison
st.subheader("Edge vs Cloud Performance Comparison")

col1, col2 = st.columns(2)

with col1:
    # Processing time comparison
    comparison_data = {
        'Processing Type': ['Edge Computing', 'Cloud Computing'],
        'Average Time (ms)': [avg_edge_time, avg_cloud_time],
        'Color': ['green', 'red']
    }
    
    fig_comp = px.bar(comparison_data, 
                      x='Processing Type', 
                      y='Average Time (ms)',
                      color='Color',
                      color_discrete_map={'green': 'lightgreen', 'red': 'lightcoral'},
                      title="Processing Time Comparison")
    
    st.plotly_chart(fig_comp, use_container_width=True)

with col2:
    st.write(f"• **{((avg_cloud_time-avg_edge_time)/avg_cloud_time*100):.0f}% faster** processing")
    st.write(f"• **{data_reduction:.0f}% less** data to cloud")

# Auto-refresh every 10 seconds
st.write("")
time.sleep(1)
st.rerun()