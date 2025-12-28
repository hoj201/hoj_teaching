import streamlit as st
import random
from copy import deepcopy

st.title("Psuedo-random number generation")

seed = st.text_input("seed")
names = [n.strip() for n in st.text_area("names").split("\n")]
names_copy = deepcopy(names)

random.seed(seed)
n=None
if st.button("Generate"):
    n = random.randint(0,10**20)
    st.text(n)
    random.shuffle(names_copy)
    st.text(names_copy)