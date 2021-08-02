import streamlit as st
import pandas as pd
import numpy as np

import community_profiles
import contact
import costcalc
import maps
import main


PAGES = {
    "Home": main,
    "Maps": maps,
    "Community Profiles": community_profiles,
    "Energy Cost Calculator": costcalc,
    "Contact us": contact
}
st.sidebar.title('Menu')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
