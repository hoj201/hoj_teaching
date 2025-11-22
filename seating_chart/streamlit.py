import streamlit as st
from hoj_slides import generate, Content, PERIODS
from pathlib import Path
import json
import logging
import os

logger = st.logger.get_logger(__name__)
logger.setLevel(logging.INFO)
logger.info('Streamlit app started')

SCRIPT_DIR = Path(__file__).resolve().parent


st.title("Seating Chart Slide Generator")

st.header("Which blocks")
selected_periods = st.multiselect("Blocks", options=PERIODS, default=PERIODS)


st.header("Content")
with open(f"{SCRIPT_DIR}/default_content.json", "r") as f:
    default_content = json.load(f)

content_string = st.text_area(
    label="content",
    value=json.dumps(default_content, indent=4),
    height=500
)
try:
    content = json.loads(content_string)
except json.decoder.JSONDecodeError as error:
    st.error(error)

try:
    content = Content.from_dict(content)
except Exception as e:
    st.error(e)


exam_mode = st.toggle("exam_mode", value=False, help="Arranges students into individual desks")
if exam_mode:
    max_table_size=1

if st.button("Generate slides"):
    logger.info("Generating slides")
    logger.info(f"Selected periods: {selected_periods}") 
    logger.info(f"Exam mode: {exam_mode}")  
    logger.info(f"Content: {content_string}")
    if len([x for x in os.listdir('.') if x.endswith('.svg')]) >= 4:
        logger.info("removing old svg files")
        [os.remove(x) for x in os.listdir('.') if x.endswith('.svg')]
    tables_by_period, slide_filenames = generate(selected_periods, content, exam_mode)
    for fn in slide_filenames:
        st.image(fn)
    st.json(tables_by_period)
