import streamlit as st
from configparser import ConfigParser
from models import album
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page



config = ConfigParser()
config.read("config.ini")
endpointParams = config["endpoint"]

Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]

endpointUri = Host + ":" + Port 


def AlbumView(model):
    st.session_state['key'] = False


    def AddAlbum( r_album_name, r_album_description):
        model.Add_album(r_album_name, r_album_description)

    def DeleteAlbum( album_name):
        model.Delete_album(album_name)

    def OpenAlbum(album_name):
        st.session_state.current_album = album_name
        switch_page("album content")

    def Calculate_rows(collection_len, max_items_in_row):
        rows = int(collection_len / max_items_in_row)
        last_row_addition = (collection_len % max_items_in_row)
        return rows , last_row_addition


    st.title("choose album collection")
    st.sidebar.header("Album menu operation")
    sidebar_add_expander = st.sidebar.expander("Add album")
    with sidebar_add_expander:
        with st.form("Add album"):
            r_album_name = st.text_input("Album name:", "my first album")
            r_album_description = st.text_input("Album Description:", "cool album")
            st.form_submit_button("Add album" , on_click= AddAlbum, args = (r_album_name,  r_album_description,))

    st.markdown(
            '''
    <style>
        div[data-testid="column"]  {
            border-radius: 25px;
            border-style: solid;
            border-color: #6C6F73; 
            background-color: #C1D5F0;
            width: fit-content;
            margin: auto;
            text-align: center;
            }
        
    </style>
    '''
    ,unsafe_allow_html=True

    )


    collection_len = len(model.albumList)
    rows, items_in_lasr_row = Calculate_rows(collection_len, 3)

    album_index = 0
    for row_index in range (rows): 
        with st.container():
            container_column_list = st.columns(3)
            for col in container_column_list:
                with col:
                    cont = st.container()
                    with cont:
                        st.markdown(
                            '''
                            <style>
                                div[data-testid="stText"] {
                                    color: #286864;
                                    font-size: 14px;
                                }
                            </style
                            '''
                            ,unsafe_allow_html=True
                        )
                        current_album_name = ( model.albumList[album_index]["name"])
                        current_album_id = (model.albumList[album_index]["id"])
                        st.text(("Album name: " + model.albumList[album_index]["name"]))
                        st.text(("Description: " + model.albumList[album_index]["description"]))
                        st.text(("Pictures count:" + str(model.albumList[album_index]["count"])))
                        btn_open = st.button("Open album",key =(model.albumList[album_index]["id"]+"open_album"))
                        if btn_open:
                            OpenAlbum(current_album_name)

                        st.button("Delet album",key =(model.albumList[album_index]["id"]+"Delete_album"), on_click=DeleteAlbum , args=(current_album_name,))
                        album_index +=1


    if items_in_lasr_row > 0:
        with st.container():
            last_container_columns = st.columns(items_in_lasr_row)
            for col in last_container_columns:
                with col:
                    cont = st.container()
                    with cont:
                        st.markdown(
                            '''
                            <style>
                                div[data-testid="stText"] {
                                    color: #286864;
                                    font-size: 14px;
                                }
                            </style
                            '''
                            ,unsafe_allow_html=True
                        )
                        current_album_name = ( model.albumList[album_index]["name"])
                        current_album_id = (model.albumList[album_index]["id"])
                        key = model.albumList[album_index]["id"]
                        st.text(("Album name: " + model.albumList[album_index]["name"]))
                        st.text(("Description: " + model.albumList[album_index]["description"]))
                        st.text(("Pictures count:" + str(model.albumList[album_index]["count"])))
                        btn_open = st.button("Open album",key =(model.albumList[album_index]["id"]+"open_album"))
                        if btn_open:
                            OpenAlbum(current_album_name)
                        st.button("Delet album",key =(model.albumList[album_index]["id"]+"Delete_album") , on_click=DeleteAlbum , args=(current_album_name,))
                        album_index +=1



AlbumView(album.Albums(endpointUri, baseRoute))
                       



