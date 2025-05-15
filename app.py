import streamlit as st
from streamlit_option_menu import option_menu
import base64
import warnings
from view import home
from view import predict

st.set_page_config(page_title="Dashboard Bonbon Ice Cream", page_icon="img/bonbon.png", layout="wide")

warnings.filterwarnings("ignore")

# streamlit run .\dashboard.py --server.port 8888

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("img/bg.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:background/png;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    # Menambahkan styling CSS untuk mengganti warna background sidebar dan option menu
    st.markdown(
        """
        <style>
        .edtmxes8 {  
            background-color: #EC0A0B !important;  
        }
        
        .e14ksaui0 {
            background-color: #EC0A0B !important;  
        }

        .e14ksaui0 a:hover{
            background-color: #ffffff !important;
        }

        .eacrzsi18 {
            background-color: #ffffff !important
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # Sidebar content
    st.sidebar.image("img/bonbon.png", caption="")
    st.sidebar.title("Selamat Datang!")

    # Sidebar menu with option_menu
    with st.sidebar:
        page = option_menu("Main Menu",
                                ["Home", "Model Clusters"],
                                icons=["house", "search"],
                                menu_icon="list",
                                default_index=0,
                                styles={
                                    "menu-title":{
                                        "color":"#EC0A0B !important",
                                    },
                                    "container": {
                                        "padding": "5!important",
                                        "background-color": "#FFFFFFFF"},
                                    "nav-link": {
                                        "font-size": "16px", 
                                        "text-align": "left", 
                                        "margin": "5px",
                                        "--hover-color": "#FDD776",
                                        "border": "2px solid #EC0A0B",
                                        "color":"#EC0A0B !important"
                                    },
                                    "nav-link-selected": {
                                        "background-color":"#ffffff"}
                                })
            
    # Conditional page rendering
    if page == "Home":
        home.main()
    elif page == "Model Clusters":
        predict.main()

if __name__ == '__main__':
    main()