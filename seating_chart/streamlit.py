import streamlit as st
from hoj_slides import generate
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
import os

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


st.header("Content")
with open(f"{SCRIPT_DIR}/default_content.json", "r") as f:
    default_content = json.load(f)

content_string = st.text_area(
    label="content",
    value=json.dumps(default_content, indent=4)
)
try:
    content = json.loads(content_string)
except json.decoder.JSONDecodeError as error:
    st.error(error)


if st.button("Generate slides"):
    if len([x for x in os.listdir('.') if x.endswith('.svg')]) >= 4:
        logging.info("removing old svg files")
        [os.remove(x) for x in os.listdir('.') if x.endswith('.svg')]
    tables_by_period, slide_filenames = generate(selected_periods, content, seed=seed)
    for fn in slide_filenames:
        st.image(fn)
    st.json(tables_by_period)
