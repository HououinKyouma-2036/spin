import streamlit as st
import time
import random

def create_spinning_wheel():
    if 'names' not in st.session_state:
        st.session_state.names = []
        st.session_state.current_step = 'input'
        st.session_state.places = ["FIRST", "SECOND", "THIRD", "LAST"]
        st.session_state.place_index = 0

    if st.session_state.current_step == 'input':
        st.title("Spinning Wheel Game")
        
        # Name inputs
        for i in range(4):
            name = st.text_input(f"Enter name {i+1}:", key=f"name_{i}")
            if name:
                if name not in st.session_state.names:
                    st.session_state.names.append(name)

        if len(st.session_state.names) == 4:
            if st.button("Start Game!"):
                st.session_state.current_step = 'spin'
                st.experimental_rerun()

    elif st.session_state.current_step == 'spin':
        st.title("Spinning Wheel Game")
        
        if len(st.session_state.names) > 0:
            if st.button("Spin the Wheel!"):
                # Spinning animation
                with st.empty():
                    for _ in range(10):
                        names_display = "\n".join(st.session_state.names)
                        st.text(f"Spinning...\n\n↓\n{names_display}")
                        time.sleep(0.2)
                        st.empty()
                    
                    # Select winner
                    winner = random.choice(st.session_state.names)
                    st.success(f"🎉 {winner} comes in {st.session_state.places[st.session_state.place_index]} place! 🎉")
                    
                    # Remove winner and update
                    st.session_state.names.remove(winner)
                    st.session_state.place_index += 1
                    
                    if st.session_state.names:
                        st.write(f"Remaining contestants: {', '.join(st.session_state.names)}")
        else:
            st.success("Game Over! Thanks for playing!")
            if st.button("Play Again"):
                st.session_state.clear()
                st.experimental_rerun()

if __name__ == "__main__":
    create_spinning_wheel()
