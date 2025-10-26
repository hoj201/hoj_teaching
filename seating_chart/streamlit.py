import streamlit as st
from hoj_slides import generate
from datetime import datetime, timedelta
from pathlib import Path
import json

SCRIPT_DIR = Path(__file__).resolve().parent
periods = [
    "period_12",
    "period_45",
    "period_78",
    "period_910"
]

st.title("Seating Chart Slide Generator")

st.header("Which blocks")
selected_periods = st.multiselect("Blocks", options=periods)

st.header("Random Seed")
seed = (datetime.now() + timedelta(hours=24)).strftime("%b_%d_%Y")
seed = st.text_input(
    label="seed",
    value=seed
)


st.header("Agenda")
with open(f"{SCRIPT_DIR}/agenda.json", "r") as f:
    default_agenda = json.load(f)

agenda_string = st.text_area(
    label="agenda",
    value=json.dumps(default_agenda, indent=4)
)
try:
    agenda = json.loads(agenda_string)
except json.decoder.JSONDecodeError as error:
    st.error(error)


st.header("Do Nows")
with open(f"{SCRIPT_DIR}/do_now.json", "r") as f:
    default_do_now = json.load(f)

do_now_string = st.text_area(
    label="do_now",
    value=json.dumps(default_do_now, indent=4)
)
try:
    do_now = json.loads(do_now_string)
except json.decoder.JSONDecodeError as error:
    st.error(error)

st.header("Announcements")
with open(f"{SCRIPT_DIR}/announcements.json", "r") as f:
    default_announcement = json.load(f)

announcements_string = st.text_area(
    label="announcements",
    value=json.dumps(default_announcement, indent=4)
)
try:
    announcements = json.loads(announcements_string)
except json.decoder.JSONDecodeError as error:
    st.error(error)

if st.button("Generate slides"):
    tables_by_period, slide_filenames = generate(selected_periods, agenda, announcements, do_now, seed=seed)
    for fn in slide_filenames:
        st.image(fn)
    st.json(tables_by_period)
