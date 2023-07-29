import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
    st.session_state['node_title'] = ''
    st.snow()
    update_code()
    
def remove_node():
    if len(st.session_state['nodes'].items()) > 0:    
        del st.session_state['nodes'][st.session_state['node_remove_selected'].replace(' ', '_')]
        update_code()
    else:
        st.toast('no node is selected')
    
def update_code():
    st.session_state['code'] = '''
                               flowchart
                               '''
    if len(st.session_state['nodes'].items()) > 0:
        for node_id, node_title in st.session_state['nodes'].items():
            st.session_state['code']+=f'\n{node_id}[{node_title}]'
            
if __name__ == '__main__':
    if 'code' not in st.session_state:
        st.session_state['code'] = '''
                                   flowchart
                                   '''
    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = {}
    
    if 'edge' not in st.session_state:
        st.session_state['edge'] = {}
            
    if 'subgraphs' not in st.session_state:
        st.session_state['subgraphs'] = {}
        
    st.set_page_config(layout='wide')
    st.title('Mermaid flow chart editor')
    st.write('Help you create Mermaid flow charts in a more manageable and efficient way!')
    col_config, col_display, col_code = st.columns([2,3,2])
    with col_config:
        st.subheader('Node')
        col_node_title, col_node_shape = st.columns([3,1])
        col_node_title.text_input('Node title', placeholder='don\'t repeat node title ', on_change=add_node, key='node_title')
        col_node_shape.selectbox('shape', options=['square', 'round', 'container'])
        st.button('add a new node', on_click=add_node, use_container_width=True)
        st.selectbox('All nodes added', list(st.session_state['nodes'].values())[::-1], key='node_remove_selected')
        st.button('remove an existing node', on_click=remove_node, use_container_width=True)

        st.subheader('Edge')
        st.subheader('Group')
        
    with col_display:
        st_mermaid(st.session_state['code'], height=500)

    with col_code:
        st.code(st.session_state['code'], language='mermaid', line_numbers=True)
