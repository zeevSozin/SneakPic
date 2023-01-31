import streamlit as st
from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")

endpointParams = config["endpoint"]
Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]
endpointUri = Host + ":" + Port 


st.set_page_config(page_title="sneakPic ")

st.session_state['current_album'] = None

st.title("SneakPic - Adding Insight to your photo collections")
st.subheader("How does SneakPic works?")
st.text("We are using YOLOv5 engin under the hood,\nby uploading your photos to the album collection \nSneakPic will analize and categorize your photos which allows you \nto search in your picture collection by objects where detected from the pictures ")
st.subheader("How to use SneakPic?")
st.caption("if it is your first time you use SneakPic:")
st.caption("Just navigate to :blue[Album Collection] on the side panel and create your firs album\n then open your album by clicking the :blue[opet album] and add your pictures")
st.caption("Once you have photos in your collection you will be able to see all the photos by navigating to :blue[Picture collection]")
st.caption("Once photos are loaded in your collection you will be able search in your photo collections/albums by navigating to :blue[Search In collection]")
st.subheader("Enjoy using SneakPic :grin: ")



