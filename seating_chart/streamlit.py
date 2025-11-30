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

st.write("If you do not specify seating tables, default seating will be used. To randomize seating, provide 'seeds' and 'max_table_size' in the content JSON.")
st.json({
    "seeds": {
        "period_12": "labubu",
        "period_45": "67",
        "period_78": "41",
        "period_910": "1234randomness"
    },
    "max_table_size": 5}
)

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
    logger.error("JSON decode error in content input")
    st.error(error)

if "agenda" not in content or "do_now" not in content or "announcements" not in content:
    st.error("Content must include 'agenda', 'do_now', and 'announcements' sections.")

if "tables" not in content:
    st.warning("No 'tables' section found in content; default tables will be used if seeds are provided.")
    if "seeds" not in content:
        st.warning("No 'tables' or 'seeds' provided; using default seating.")

try:
    content = Content.from_dict(content)
except Exception as e:
    logger.error("Error creating Content from dict")
    st.error(e)
    raise e


printable = st.toggle("printable", value=False, help="Makes slides suitable for printing.")

if st.button("Generate slides"):
    logger.info("Generating slides")
    logger.info(f"Selected periods: {selected_periods}") 
    logger.info(f"Content: {content_string}")
    if len([x for x in os.listdir('.') if x.endswith('.svg')]) >= 4:
        logger.info("removing old svg files")
        [os.remove(x) for x in os.listdir('.') if x.endswith('.svg')]
    tables_by_period, slide_filenames = generate(selected_periods, content, printable)
    st.header("Generated Slides")
    for fn in slide_filenames:
        st.image(fn)
    st.code(json.dumps(tables_by_period, indent=4), language='json')
    logger.info("Slides generated successfully")
