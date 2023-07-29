import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
    st.session_state['node_title'] = ''
def remove_node():
    del st.session_state['nodes'][st.session_state['node_remove_selected'].replace(' ', '_')]
    
    
        
if __name__ == '__main__':
    if 'code' not in st.session_state:
        st.session_state['code'] = 'flowchart'
    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = {}
    
    if 'edge' not in st.session_state:
        st.session_state['edge'] = {}
            
    if 'subgraphs' not in st.session_state:
        st.session_state['subgraphs'] = {}
        
    st.set_page_config(layout='wide')
    st.title('Mermaid flow chart editor')
    st.write('Help you create Mermaid flow charts in a more manageable and efficient way!')
    col_config, col_display = st.columns([3.5,6])
    with col_config:
        col_node_title, col_node_shape, col_node_add = st.columns([5,2.5,2])
        col_node_title.text_input('title', label_visibility='collapsed', placeholder='node title', on_change=add_node, key='node_title')
        col_node_shape.selectbox('shape', options=['square', 'round', 'container'], label_visibility='collapsed')
        col_node_add.button('add', on_click=add_node, use_container_width=True)
        col_nodes_added, col_node_remove = st.columns([4.95, 4.55])
        col_nodes_added.selectbox('Nodes added', list(st.session_state['nodes'].values())[::-1], label_visibility='collapsed', key='node_remove_selected', placeholder='No nodes ')
        col_node_remove.button('remove an existing node', on_click=remove_node, use_container_width=True)

        st.code(st.session_state['code'], language='mermaid', line_numbers=True)

    with col_display:
        for node_id, node_title in st.session_state['nodes'].items():
            st.session_state['code']+=f'\n{node_id}[{node_title}]'
        st_mermaid(st.session_state['code'], height=500)

