import streamlit as st
from streamlit_mermaid import st_mermaid
from flowchart import *

if __name__ == '__main__':
    # init session state
    if 'code' not in st.session_state:
        st.session_state['code'] = ''
    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = {}
    if 'edges' not in st.session_state:
        st.session_state['edges'] = {}
    if 'shapes' not in st.session_state:
        st.session_state['shapes'] = {}
    if 'notes' not in st.session_state:
        st.session_state['notes'] = {}
        
    st.set_page_config(layout='wide')
    # tab area
    with st.sidebar:

        st.markdown('''
                    # Mermaid flowchart editor                  
                    *Help you create Mermaid flowcharts in a more manageable and efficient way.*
                    
                    **:heart: Developed by Leo Wu :heart:** 

                    ## Quick start
                    A flowchart has two fundamental elements, nodes and edges which can be created via the mian tab on the right.
                    An edge can connect a node with another node or group of nodes.
                    
                    ''' )

        tab_mermaid = '''
                         flowchart LR
                         node1[I'm node 1]
                         node2[(I'm node 2)]
                         node1--I'm an edge-->node2
                         node2-->node2
                      '''
        st_mermaid(tab_mermaid, height=150)
        st.markdown('''
                    ## Experimental features 
                    ''' )
        st.checkbox(':smiling_imp: I want some fun!!!')
    # main area
    col_config, col_display = st.columns([1,3])
    
    with col_config:
        tab_all, tab_config, tab_code = st.tabs(['💻 Main', '🚀 Configuration', '🌠 Show me the code!!!'])

        with tab_all:
            # node - add
            st.subheader('Nodes')
            col_node_title, col_node_shape = st.columns([3,2])
            col_node_title.text_input(label='Node title', key='node_title')
            st.button('add a new node', on_click=add_node, use_container_width=True)
            col_node_shape.selectbox('Node shape', options=['rectangle', 'ellipse', 'container'], key='node_shape')
            # st.button('add a new node', on_click=add_node, use_container_width=True)
            # node - remove
            st.selectbox('Select a node to remove', get_all_nodes(), key='node_remove_selected')
            st.button('remove the selected node', on_click=remove_node, use_container_width=True)

            # edge - add
            st.divider()
            st.subheader('Edges')
            col_node_a, col_node_b = st.columns(2)
            col_node_a.selectbox('A (node/group)', options=get_all_nodes(), key='node_a')
            col_node_b.selectbox('B (node/group)', options=get_all_nodes()  , key='node_b')
            st.text_input('Edge note', placeholder='Can leave blank', key='edge_note')

            st.button('add an edge from A to B', use_container_width=True, on_click=add_edge)
            # edge - remove
            st.selectbox('Select an edge to remove', get_all_edges(), key='edge_remove')
            st.button('remove an existing edge', use_container_width=True, on_click=remove_edge)
        
        with tab_config:
            # config
            st.selectbox('Chart direction', ['From left to right', 'From top to bottom'], key='chart_direction', on_change=set_direction)
            st.selectbox('Chart theme', ['Default', 'Neutral', 'Base', 'Forest', 'Dark'], key='theme', on_change=set_theme)
        
        with tab_code:
            st.code(st.session_state['code'], language='mermaid', line_numbers=True)

    with col_display:
        if st.session_state['code'] != '':
            st_mermaid(st.session_state['code'], height=500)