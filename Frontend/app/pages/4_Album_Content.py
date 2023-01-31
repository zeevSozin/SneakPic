import streamlit as st
from configparser import ConfigParser
from models import album_content
from PIL import Image
import base64
from io import BytesIO
from models.picture import Picture
import json



config = ConfigParser()
config.read("config.ini")
endpointParams = config["endpoint"]

Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]

endpointUri = Host + ":" + Port 

def AlbumContentView(model):
    album_name = None
    album_list = list()
    album_names = list()
    pictures = list([Picture])
    album_name = model.Get_AlbumName()
    album_list = model.get_album_names()
    fileTypes = ["png","jpg","jpeg"]

    st.title(album_name)

    album_selection = st.selectbox("Select another album",album_list)
    if album_selection:
        model.Set_album(album_selection)


    pictures = model.Get_pictures()

    st.header("Picture collection")

    def base64_to_byte(payload):
        data = payload
        return BytesIO(base64.b64decode(data))

    
    def Delete_photo(picture_name):
        model.Delete_picture(picture_name)

    for pic in pictures:
        pic_name = pic.get_name()
        st.subheader(pic_name)
        original_photo_b64 = pic.get_Original_photo()
        st.image(base64_to_byte(original_photo_b64))
        metadata = pic.get_metadata()
        jsonMetadata = json.loads(metadata)
        metadataList = list(jsonMetadata.keys())
        columns = st.columns(len(metadataList))
        st.subheader("Objects Detected")
        iterator = 0
        for col in columns:
            col.metric(metadataList[iterator], jsonMetadata[metadataList[iterator]])
            iterator += 1
        st.text_area("metadata", f"Detected objects:{metadata}")
        with st.expander("Processed image"):
            processed_photo_b64 = pic.get_Processed_photo()
            st.image(base64_to_byte(processed_photo_b64))
        with st.expander("Delete image"):
            st.button("Delete image", key = pic_name ,on_click=Delete_photo, args=(pic_name,))
        

    st.sidebar.header("Add picture to album")
    upload_file_expander = st.sidebar.expander("All File")
    with upload_file_expander:
        upload_file_form = st.form("Fill in File info")
        with upload_file_form:
            picture_name = st.text_input("pictureName:")
            uploaded_file = st.file_uploader("Add picture")
            upload_file_form_submit = st.form_submit_button("Submit")
            if upload_file_form_submit:
                if uploaded_file is not None:
                    with st.spinner("Proccessing your file"):
                        result = model.Upload_picture_to_Db(picture_name, {"file": uploaded_file.getvalue()})
                    if result == 200:
                        st.success('You are ready , please refresh the page')
                        st.experimental_rerun()


current_album = st.session_state['current_album']

AlbumContentView(album_content.Album(endpointUri, baseRoute, current_album ))


