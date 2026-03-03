import streamlit as st
import pandas as pd
import random
import time
import base64
import os

st.set_page_config(layout="wide")

# =====================
# تحميل صورة الخلفية
# =====================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

current_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(current_dir, "background.jpg")
background_base64 = get_base64(bg_path)

# =====================
# CSS احترافي بنسبة 16:9
# =====================
st.markdown(f"""
<style>

body, .stApp {{
    margin: 0;
    padding: 0;
    overflow: hidden;
}}

header {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* الكونتينر الأساسي بنسبة 16:9 */
.wrapper {{
    position: relative;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.canvas {{
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 100vw;
    max-height: 100vh;
    aspect-ratio: 16 / 9;
    background-image: url("data:image/jpg;base64,{background_base64}");
    background-size: 100% 100%;
    background-repeat: no-repeat;
}}

/* النص محسوب كنسبة من نفس الخلفية */
.name-box {{
    position: absolute;

    top: 37%;
    left: 6%;

    width: 50%;
    height: 20%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 2.5%;
    font-weight: bold;
    color: black;

    text-align: center;
}}

/* Glow */
@keyframes glow {{
  0% {{ text-shadow: 0 0 5px white; }}
  50% {{ text-shadow: 0 0 25px gold; }}
  100% {{ text-shadow: 0 0 5px white; }}
}}

.winner {{
    animation: glow 1s infinite;
}}

</style>
""", unsafe_allow_html=True)

# =====================
# تحميل البيانات
# =====================
@st.cache_data
def load_data():
    df = pd.read_excel("employees.xlsx")
    return df.to_dict("records")

if "data" not in st.session_state:
    st.session_state.data = load_data()

# =====================
# إنشاء الكونتينر
# =====================
st.markdown('<div class="wrapper"><div class="canvas">', unsafe_allow_html=True)
name_placeholder = st.empty()
st.markdown('</div></div>', unsafe_allow_html=True)

# =====================
# السحب
# =====================
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

        name_placeholder.markdown(f"""
        <div class="name-box">
            {person['Name']} | {id_display}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(speed)

    winner_id = winner['ID']
    winner_id_display = "N/A" if pd.isna(winner_id) else str(int(winner_id))

    name_placeholder.markdown(f"""
    <div class="name-box winner">
        {winner['Name']} | {winner_id_display}
    </div>
    """, unsafe_allow_html=True)

    st.session_state.data.remove(winner)

# =====================
# زر
# =====================
if st.button("START DRAW"):
    animated_draw()
