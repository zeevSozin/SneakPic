import streamlit as st
from models import tags
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



def SearchContentView(model):
    taglist = list()
    filterList = list()
    pictures = list()


    def Get_tag_list():
        return model.get_tag_list()

    def get_pictures_By_filter():
        return model.get_pictures_by_filter(filterList)


    def Calculate_rows(collection_len, max_items_in_row):
        rows = int(collection_len / max_items_in_row)
        last_row_addition = (collection_len % max_items_in_row)
        return rows , last_row_addition

    def base64_to_byte(payload):
        data = payload
        return BytesIO(base64.b64decode(data))

    taglist = Get_tag_list()



    collection_len = (len(taglist))
    rows, items_in_lasr_row = Calculate_rows(collection_len, 4)

    st.title("Filter your images by choosing the tags")

    i = 0
    for row_index in range (rows): 
        with st.container():
            container_column_list = st.columns(4)
            for col in container_column_list:
                with col:
                    tag_name = taglist[i]
                    tag_check = st.checkbox(tag_name, key = tag_name)
                    if tag_check:
                        filterList.append(tag_name)
                    i+= 1



    if items_in_lasr_row > 0:
            with st.container():
                container_column_list = st.columns(items_in_lasr_row)
                for col in container_column_list:
                    with col:
                        tag_name = taglist[i]
                        tag_check = st.checkbox(tag_name, key = tag_name)
                        if tag_check:
                            filterList.append(tag_name)
                        i += 1
           
    btn_filter = st.button("filter")

    if btn_filter:
        pictures = get_pictures_By_filter()
        print(pictures)

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

    st.sidebar.header("Total pictures found")
    st.sidebar.metric("pictures" , len(pictures))

SearchContentView(tags.Tags(endpointUri, baseRoute))

