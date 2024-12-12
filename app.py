import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
            text-align: center;
        }
        .winner-announcement {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #c41e3a, #008000);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            color: white;
            text-align: center;
            z-index: 1000;
            animation: snow 3s linear infinite;
        }
        .winner-announcement h1 {
            font-size: 2em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        @keyframes snow {
            0% { background-position: 0px 0px; }
            100% { background-position: 500px 500px; }
        }
        .snowflakes {
            position: absolute;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><text y="10" font-size="10">❄</text></svg>');
            animation: snow 10s linear infinite;
        }
    </style>
    """, unsafe_allow_html=True)

def show_winner_announcement(winner, place):
    announcement = f"""
    <div class="winner-announcement">
        <div class="snowflakes"></div>
        <h1>🎄 Congratulations! 🎄</h1>
        <h2>{winner}</h2>
        <h3>comes in {place}!</h3>
        <p>🎅 Ho Ho Ho! 🎅</p>
    </div>
    """
    return announcement

def create_wheel(names, rotation=0):
    colors = ['#c41e3a', '#008000', '#c41e3a', '#008000']
    
    fig = go.Figure(data=[go.Pie(
        values=[1] * len(names),
        rotation=rotation,
        text=names,
        textinfo='text',
        textposition='inside',
        textfont=dict(size=20, color='white'),
        marker=dict(colors=colors[:len(names)]),
        hoverinfo='none',
        hole=0.3
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=400,
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        annotations=[dict(
            text="↓",
            x=0.5,
            y=1.2,
            showarrow=False,
            font=dict(size=24, color="#c41e3a")
        )]
    )
    return fig

def create_spinning_wheel():
    local_css()
    
    # Initialize shared game state
    if 'game_id' not in st.session_state:
        st.session_state.game_id = datetime.now().strftime("%Y%m%d%H%M%S")
    if 'shared_names' not in st.session_state:
        st.session_state.shared_names = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'input'
    if 'places' not in st.session_state:
        st.session_state.places = ["FIRST 🥇", "SECOND 🥈", "THIRD 🥉", "LAST 🎁"]
    if 'place_index' not in st.session_state:
        st.session_state.place_index = 0
    if 'rotation' not in st.session_state:
        st.session_state.rotation = 0
    if 'spinning' not in st.session_state:
        st.session_state.spinning = False
    if 'animation_frame' not in st.session_state:
        st.session_state.animation_frame = 0
    if 'winner_announcement' not in st.session_state:
        st.session_state.winner_announcement = None
    if 'announcement_time' not in st.session_state:
        st.session_state.announcement_time = None

    # Christmas decorations
    st.markdown("🎄 ⭐ 🎅 ⭐ 🎄")
    st.title("Christmas Spinning Wheel")
    st.markdown("🎁 ❄️ 🦌 ❄️ 🎁")

    # Show winner announcement if active and handle auto-close
    if st.session_state.winner_announcement:
        current_time = datetime.now()
        if st.session_state.announcement_time and current_time < st.session_state.announcement_time:
            st.markdown(st.session_state.winner_announcement, unsafe_allow_html=True)
            # Force rerun every 100ms to ensure smooth closing
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.winner_announcement = None
            st.session_state.announcement_time = None
            st.rerun()

    # Input Phase
    if st.session_state.current_step == 'input':
        st.markdown("### Enter 4 Names for the Christmas Draw!")
        
        col1, col2 = st.columns(2)
        with col1:
            for i in range(2):
                name = st.text_input(f"🎄 Participant {i+1}:", key=f"name_{i}")
                if name and name not in st.session_state.shared_names:
                    st.session_state.shared_names = list(dict.fromkeys(
                        [n for n in st.session_state.shared_names if n != name] + [name]
                    ))

        with col2:
            for i in range(2, 4):
                name = st.text_input(f"🎄 Participant {i+1}:", key=f"name_{i}")
                if name and name not in st.session_state.shared_names:
                    st.session_state.shared_names = list(dict.fromkeys(
                        [n for n in st.session_state.shared_names if n != name] + [name]
                    ))

        if len(st.session_state.shared_names) == 4:
            wheel = create_wheel(st.session_state.shared_names)
            st.plotly_chart(wheel, use_container_width=True, key="preview_wheel")
            
            if st.button("🎉 Start Christmas Draw! 🎉", key="start_button"):
                st.session_state.current_step = 'spin'
                st.rerun()

    # Spinning Phase
    elif st.session_state.current_step == 'spin':
        if len(st.session_state.shared_names) > 1:
            # Create a single container for the wheel
            wheel_container = st.container()
            
            with wheel_container:
                if not st.session_state.spinning:
                    wheel = create_wheel(st.session_state.shared_names, st.session_state.rotation)
                    st.plotly_chart(wheel, use_container_width=True, 
                                  key=f"wheel_{st.session_state.place_index}")
                    
                    if st.button("🎲 Spin the Wheel! 🎲", key=f"spin_button_{st.session_state.place_index}"):
                        st.session_state.spinning = True
                        st.session_state.animation_frame = 0
                        st.rerun()

                if st.session_state.spinning:
                    if st.session_state.animation_frame < 30:
                        st.session_state.rotation = (st.session_state.rotation + 30) % 360
                        wheel = create_wheel(st.session_state.shared_names, st.session_state.rotation)
                        st.plotly_chart(wheel, use_container_width=True, 
                                      key=f"wheel_{st.session_state.place_index}_{st.session_state.animation_frame}")
                        st.session_state.animation_frame += 1
                        time.sleep(0.1)
                        st.rerun()
                    else:
                        winner = random.choice(st.session_state.shared_names)
                        
                        # Only show announcement for first three places
                        if st.session_state.place_index < 3:
                            st.session_state.winner_announcement = show_winner_announcement(
                                winner, st.session_state.places[st.session_state.place_index])
                            # Set announcement time to 2 seconds
                            st.session_state.announcement_time = datetime.now() + timedelta(seconds=2)
                        
                        st.session_state.shared_names.remove(winner)
                        st.session_state.place_index += 1
                        st.session_state.spinning = False
                        st.session_state.animation_frame = 0
                        
                        # Handle last person without announcement
                        if len(st.session_state.shared_names) == 1:
                            last_person = st.session_state.shared_names[0]
                            st.markdown(f"""
                            <div class='success'>
                                <h2>🎄 {last_person} comes in {st.session_state.places[st.session_state.place_index]}! 🎄</h2>
                                <h3>🎅 Game Complete! 🎅</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            st.session_state.shared_names = []
                        
                        st.rerun()

        else:
            st.markdown("""
            <div class='success'>
                <h2>🎄 Christmas Draw Complete! 🎄</h2>
                <p>Thank you for participating! Merry Christmas! 🎅</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎮 Play Again 🎮", key="play_again_button"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    create_spinning_wheel()
