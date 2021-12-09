# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 21:46:00 2021

@author: davis
"""

import CDS_302_DATABASE_UI
import CDS_302_DATABASE_VISUALIZATION
import streamlit as st
PAGES = {
    "Database search...": CDS_302_DATABASE_UI,
    "Database visualization": CDS_302_DATABASE_VISUALIZATION
}
st.sidebar.title('Navigation')
add_selectbox = st.sidebar.selectbox(
    "Choose page!",
    list(PAGES.keys())
)

page = PAGES[add_selectbox]
page.app()