#this will be the homepage, don't change the filename as it is needed by streamlit to acess. Other Classes etc. please add those to separate files and import them.

import streamlit as st
from api import spoonacular as sp
from streamlit.logger import get_logger

def run():
    st.set_page_config(
        page_title="Foodplanner",
        page_icon="👋",
    )

    st.title('Foodplanner in the works')
    st.subheader('this will be awesome!')

    sp.run()

if __name__ == "__main__":
    run()