import streamlit as st
import time
import random
import math
import pandas as pd
import plotly.graph_objects as go

# Set page config and CSS
st.set_page_config(page_title="Christmas Spinning Wheel", page_icon="🎄")

def local_css():
    st.markdown("""
    <style>
        .stTitle {
            color: #c41e3a !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .stButton>button {
            background-color: #c41e3a;
            color: white;
            border-radius: 20px;
            padding: 10px 25px;
            border: 2px solid #008000;
        }
        .stButton>button:hover {
            background-color: #008000;
            border: 2px solid #c41e3a;
        }
        .stTextInput>div>div>input {
            border: 2px solid #c41e3a;
            border-radius: 10px;
            padding: 10px;
        }
        .success {
            background-color: rgba(0,128,0,0.1);
            border: 2px solid #008000;
            border-radius: 10px;
            padding: 20px;
            color: #008000;
        }
    </style>
    """, unsafe_allow_html=True)

def create_wheel(names):
    colors = ['#c41e3a', '#008000', '#c41e3a', '#008000']
    
    fig = go.Figure()
    
    # Calculate the size of each sector
    sector_size = 360 / len(names)
    
    for i, name in enumerate(names):
        # Calculate the start and end angle for each sector
        start_angle = i * sector_size
        end_angle = (i + 1) * sector_size
        
        # Add sector
        fig.add_trace(go.Pie(
            values=[1],
            rotation=90,
            name=name,
            text=[name],
            textinfo='text',
            textposition='inside',
            textfont=dict(size=20, color='white'),
            marker=dict(colors=[colors[i % len(colors)]]),
            hoverinfo='none',
            hole=0.3
        ))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=400,
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def create_spinning_wheel():
    local_css()
    
    if 'names' not in st.session_state:
        st.session_state.names = []
        st.session_state.current_step = 'input'
        st.session_state.places = ["FIRST 🥇", "SECOND 🥈", "THIRD 🥉", "LAST 🎁"]
        st.session_state.place_index = 0
        st.session_state.rotation = 0

    # Christmas decorations
    st.markdown("🎄 ⭐ 🎅 ⭐ 🎄")
    st.title("Christmas Spinning Wheel")
    st.markdown("🎁 ❄️ 🦌 ❄️ 🎁")

    if st.session_state.current_step == 'input':
        st.markdown("### Enter 4 Names for the Christmas Draw!")
        
        col1, col2 = st.columns(2)
        with col1:
            for i in range(2):
                name = st.text_input(f"🎄 Participant {i+1}:", key=f"name_{i}")
                if name and name not in st.session_state.names:
                    st.session_state.names.append(name)
        
        with col2:
            for i in range(2, 4):
                name = st.text_input(f"🎄 Participant {i+1}:", key=f"name_{i}")
                if name and name not in st.session_state.names:
                    st.session_state.names.append(name)

        if len(st.session_state.names) == 4:
            st.markdown("---")
            st.button("🎉 Start Christmas Draw! 🎉", key="start")
            if st.session_state.get("start"):
                st.session_state.current_step = 'spin'
                st.rerun()

    elif st.session_state.current_step == 'spin':
        if len(st.session_state.names) > 0:
            wheel = create_wheel(st.session_state.names)
            wheel_placeholder = st.empty()

if __name__ == "__main__":
    create_spinning_wheel()
