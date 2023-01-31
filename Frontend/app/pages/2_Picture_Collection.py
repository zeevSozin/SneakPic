import streamlit as st
from models import pictures
from configparser import ConfigParser
import json
import base64
from io import BytesIO

config = ConfigParser()
config.read("config.ini")
endpointParams = config["endpoint"]

Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]

endpointUri = Host + ":" + Port 

def PictureContentView(model):
    pictures = list()
    

    def Get_picture_list():
        return model.get_all_pictures()

    def base64_to_byte(payload):
        data = payload
        return BytesIO(base64.b64decode(data))

    pictures = Get_picture_list()

    st.sidebar.header("Total pictures in collection")
    st.sidebar.metric("pictures" , len(pictures))

    st.title("All the pictures")
    if pictures:

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
        

PictureContentView(pictures.Pictures(endpointUri, baseRoute))