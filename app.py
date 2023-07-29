import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    st.session_state['nodes'][st.session_state['node_title']] = st.session_state['node_title']
    st.session_state['node_title'] = ''
        
if __name__ == '__main__':
    # Initialization
    if 'code' not in st.session_state:
        st.session_state['code'] = 'flowchart'
    
    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = {}
    
    if 'edge' not in st.session_state:
        st.session_state['edge'] = {}
            
    if 'subgraphs' not in st.session_state:
        st.session_state['subgraphs'] = {}
        
    st.set_page_config(layout='wide')
    st.title('Mermaid visual editor')

    col_config, col_display = st.columns([3.5,6])
    with col_config:
        st.markdown('''
                    This tool aims to help you create some common diagrams supported by Mermaid.
                    Currently it can create flow chart.
                    ''')
        st.selectbox(label='Please select a diagram type', options=['Flow chart', 'Class chart', 'Gantt chart'])

        col_node_title, col_node_shape, col_node_add = st.columns([5,2.5,2.5])
        col_node_title.text_input('title', label_visibility='collapsed', placeholder='node title', on_change=add_node, key='node_title')
        col_node_shape.selectbox('shape', options=['square', 'round', 'container'], label_visibility='collapsed')
        col_node_add.button('add', on_click=add_node, use_container_width=True)
        col_nodes_added, col_node_remove, col_node_edit = st.columns([5,1.5,1.5])
        col_nodes_added.selectbox('Nodes added', st.session_state['nodes'].values(), label_visibility='collapsed')
        col_node_remove.button('remove', use_container_width=True)
        col_node_edit.button('edit', use_container_width=True)

        st.code(st.session_state['code'], language='mermaid', line_numbers=True)

    with col_display:
        st_mermaid(st.session_state['code'], height=1000)
        
    with col_code:
        st.subheader('Code generated')
