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
    if 'groups' not in st.session_state:
        st.session_state['groups'] = {}
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
                    A flowchart has two fundamental elements, nodes and edges which can be created in the corresponding tab on the right.
                    Any number of nodes can be grouped to form a subgraph. An edge can connect a node with another node or group of nodes.
                    
                    ## Experimental features 
                    ''' )
        st.checkbox(':smiling_imp: I want some fun!!!')
        st.checkbox(':turtle: I feel lazy today...')
    # main area
    col_config, col_display, col_code = st.columns([2,3,2])
    
    with col_config:
        tab_all, tab_group, tab_config = st.tabs(['Main', 'Group', 'Configuration'])

        with tab_all:
            # node - add
            st.subheader('Nodes')
            col_node_title, col_node_shape = st.columns([3,2])
            col_node_title.text_input(label='Node title', key='node_title', on_change=add_node, placeholder='Press enter to add it.')
            col_node_shape.selectbox('Node shape', options=['rectangle', 'ellipse', 'container'], key='node_shape')
            # st.button('add a new node', on_click=add_node, use_container_width=True)
            # node - remove
            st.selectbox('Select a node to remove', list(st.session_state['nodes'].values())[::-1], key='node_remove_selected')
            st.button('remove an existing node', on_click=remove_node, use_container_width=True)

            # edge - add
            st.divider()
            st.subheader('Edges')
            col_node_a, col_node_b = st.columns(2)
            col_node_a.selectbox('A (node/group)', options=st.session_state['nodes'], key='node_a')
            col_node_b.selectbox('B (node/group)', options=st.session_state['nodes'], key='node_b')
            col_edge_note, col_edge_type = st.columns(2)
            col_edge_note.text_input('Edge note', placeholder='Can leave as blank')
            col_edge_type.selectbox('Edge type', ['---'])

            st.button('add an edge from A to B', use_container_width=True, on_click=add_edge)
            # edge - remove
            st.selectbox('Select an edge to remove', get_all_edges(), placeholder=' ')
            st.button('remove an existing edge', use_container_width=True, on_click=remove_edge)
        
        with tab_group:
            # group - add
            st.multiselect('Select one/multiple node(s) to group', options=st.session_state['nodes'], key='group_nodes')
            col_group_name, col_group_direction = st.columns([1,1])
            col_group_name.text_input('Group name', key='group_name')
            col_group_direction.selectbox('Group direction', ['From left to right', 'from top to bottom'])
            st.button('group', use_container_width=True, on_click=group_nodes)
            # group - remove
            st.selectbox('Select a group to ungroup', st.session_state['groups'].keys(), key='group_selected')
            st.button('ungroup an existing group', use_container_width=True, on_click=ungroup_nodes)
            
        with tab_config:
            # config
            st.selectbox('Chart direction', ['From left to right', 'from top to bottom'])
            st.selectbox('Chart theme', ['base', 'forest', 'dark'])
        
        
    with col_display:
        if st.session_state['code'] != '':
            st_mermaid(st.session_state['code'], height=500)

    with col_code:
        st.code(st.session_state['code'], language='mermaid', line_numbers=True)
        st.write(st.session_state['nodes'])
        st.write(st.session_state['edges'])
        st.write(st.session_state['groups'])
        st.write(st.session_state['shapes'])