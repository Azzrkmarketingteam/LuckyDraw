import streamlit as st
import pandas as pd
import random
import time
import base64
import os

st.set_page_config(layout="wide")

# Load background
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

current_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(current_dir, "background.jpg")
background_base64 = get_base64(bg_path)

# CSS with exact rectangle positioning
st.markdown(f"""
<style>

body, .stApp {{
    margin: 0;
    padding: 0;
    overflow: hidden;
}}

[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{background_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

header {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* animation glow for winner */
@keyframes glow {{
  0% {{ text-shadow: 0 0 0.2em white; }}
  50% {{ text-shadow: 0 0 1em gold; }}
  100% {{ text-shadow: 0 0 0.2em white; }}
}}

/* Name box exactly in your rectangle */
.name-box {{
    position: absolute;
    top: 44.6%;
    left: 9.4%;

    width: 49.8%;
    height: 20.4%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 3vw; /* scales with viewport */
    font-weight: bold;
    color: black;
    text-align: center;
}}

.winner {{
    animation: glow 1s infinite;
}}

</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("employees.xlsx")
    return df.to_dict("records")

if "data" not in st.session_state:
    st.session_state.data = load_data()

name_placeholder = st.empty()

# Animated draw
def animated_draw():
    if len(st.session_state.data) == 0:
        return

    winner = random.choice(st.session_state.data)
    total_duration = 20
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= total_duration:
            break

        progress = elapsed / total_duration
        speed = 0.03 + (0.22 * progress)

        person = random.choice(st.session_state.data)
        id_value = person['ID']
        id_display = "N/A" if pd.isna(id_value) else str(int(id_value))

        # name during draw
        name_placeholder.markdown(f"""
        <div class="name-box">
            {person['Name']} | {id_display}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(speed)

    # Winner with glow
    winner_id = winner['ID']
    winner_id_display = "N/A" if pd.isna(winner_id) else str(int(winner_id))

    name_placeholder.markdown(f"""
    <div class="name-box winner">
        {winner['Name']} | {winner_id_display}
    </div>
    """, unsafe_allow_html=True)

    st.session_state.data.remove(winner)

if st.button("START DRAW"):
    animated_draw()
