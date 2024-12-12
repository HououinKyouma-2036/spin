import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config and CSS
st.set_page_config(page_title="Christmas Spinning Wheel", page_icon="🎄")

# Initialize game state in a persistent way
if 'game_states' not in st.session_state:
    st.session_state.game_states = {
        'active_game': None,
        'players': set(),
        'names': [],
        'current_step': 'waiting',
        'places': ["FIRST 🥇", "SECOND 🥈", "THIRD 🥉", "LAST 🎁"],
        'place_index': 0,
        'rotation': 0,
        'spinning': False,
        'animation_frame': 0,
        'winner_announcement': None,
        'announcement_time': None
    }

# Get unique user ID
if 'user_id' not in st.session_state:
    st.session_state.user_id = get_script_run_ctx().session_id

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
    
    # Christmas decorations
    st.markdown("🎄 ⭐ 🎅 ⭐ 🎄")
    st.title("Christmas Spinning Wheel")
    st.markdown("🎁 ❄️ 🦌 ❄️ 🎁")

    # Show winner announcement if active
    if st.session_state.game_states['winner_announcement']:
        current_time = datetime.now()
        if (st.session_state.game_states['announcement_time'] and 
            current_time < st.session_state.game_states['announcement_time']):
            st.markdown(st.session_state.game_states['winner_announcement'], unsafe_allow_html=True)
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.game_states['winner_announcement'] = None
            st.session_state.game_states['announcement_time'] = None
            st.rerun()

    # Waiting Room / Player Join Phase
    if st.session_state.game_states['current_step'] == 'waiting':
        st.markdown("### Join the Christmas Draw! 🎄")
        
        player_name = st.text_input("Enter your name:", key="player_name")
        
        if player_name and st.button("Join Game! 🎅"):
            if len(st.session_state.game_states['players']) < 4:
                st.session_state.game_states['players'].add(player_name)
                st.session_state.game_states['names'].append(player_name)
                st.rerun()
            else:
                st.error("Game is full! Please wait for the next round.")

        # Show current players
        st.markdown("### Current Players:")
        for idx, player in enumerate(st.session_state.game_states['names'], 1):
            st.markdown(f"{idx}. {player} 🎁")

        # Start game when 4 players have joined
        if len(st.session_state.game_states['players']) == 4:
            st.success("All players have joined! Starting the game...")
            st.session_state.game_states['current_step'] = 'spin'
            wheel = create_wheel(st.session_state.game_states['names'])
            st.plotly_chart(wheel, use_container_width=True, key="initial_wheel")
            time.sleep(2)
            st.rerun()

    # Spinning Phase
    elif st.session_state.game_states['current_step'] == 'spin':
        if len(st.session_state.game_states['names']) > 1:
            wheel_container = st.container()
            
            with wheel_container:
                if not st.session_state.game_states['spinning']:
                    wheel = create_wheel(st.session_state.game_states['names'], 
                                      st.session_state.game_states['rotation'])
                    st.plotly_chart(wheel, use_container_width=True, 
                                  key=f"wheel_{st.session_state.game_states['place_index']}")
                    
                    if st.button("🎲 Spin the Wheel! 🎲", 
                               key=f"spin_button_{st.session_state.game_states['place_index']}"):
                        st.session_state.game_states['spinning'] = True
                        st.session_state.game_states['animation_frame'] = 0
                        st.rerun()

                if st.session_state.game_states['spinning']:
                    if st.session_state.game_states['animation_frame'] < 30:
                        st.session_state.game_states['rotation'] = (
                            st.session_state.game_states['rotation'] + 30) % 360
                        wheel = create_wheel(st.session_state.game_states['names'], 
                                          st.session_state.game_states['rotation'])
                        st.plotly_chart(wheel, use_container_width=True, 
                                      key=f"wheel_{st.session_state.game_states['place_index']}_{st.session_state.game_states['animation_frame']}")
                        st.session_state.game_states['animation_frame'] += 1
                        time.sleep(0.1)
                        st.rerun()
                    else:
                        winner = random.choice(st.session_state.game_states['names'])
                        
                        if st.session_state.game_states['place_index'] < 3:
                            st.session_state.game_states['winner_announcement'] = show_winner_announcement(
                                winner, st.session_state.game_states['places'][st.session_state.game_states['place_index']])
                            st.session_state.game_states['announcement_time'] = datetime.now() + timedelta(seconds=2)
                        
                        st.session_state.game_states['names'].remove(winner)
                        st.session_state.game_states['place_index'] += 1
                        st.session_state.game_states['spinning'] = False
                        st.session_state.game_states['animation_frame'] = 0
                        
                        if len(st.session_state.game_states['names']) == 1:
                            last_person = st.session_state.game_states['names'][0]
                            st.markdown(f"""
                            <div class='success'>
                                <h2>🎄 {last_person} comes in {st.session_state.game_states['places'][st.session_state.game_states['place_index']]}! 🎄</h2>
                                <h3>🎅 Game Complete! 🎅</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            st.session_state.game_states['names'] = []
                        
                        st.rerun()

        else:
            st.markdown("""
            <div class='success'>
                <h2>🎄 Christmas Draw Complete! 🎄</h2>
                <p>Thank you for participating! Merry Christmas! 🎅</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎮 Start New Game 🎮", key="new_game_button"):
                # Reset game state
                st.session_state.game_states = {
                    'active_game': None,
                    'players': set(),
                    'names': [],
                    'current_step': 'waiting',
                    'places': ["FIRST 🥇", "SECOND 🥈", "THIRD 🥉", "LAST 🎁"],
                    'place_index': 0,
                    'rotation': 0,
                    'spinning': False,
                    'animation_frame': 0,
                    'winner_announcement': None,
                    'announcement_time': None
                }
                st.rerun()

if __name__ == "__main__":
    create_spinning_wheel()
