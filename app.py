import streamlit as st
from streamlit_mermaid import st_mermaid

def add_new_node(code, id, name):
    print(code)
    code = f'{code}\n{id}[{name}]'
    print(code)

code = '''
    flowchart
    a
    '''
st.markdown('''
            # Mermaid visual editor
            ''')

col_config, col_display = st.columns(2)
with col_config:
    st.markdown('''
            This tool aims to help you create some common diagram supported by Mermaid.
            Currently it can create flowchart.
            ''')
    st.selectbox(label='Please select a diagram type', options=['Flowchart'])
    col_node_id, col_node_name = st.columns(2)
    with col_node_id:
        id = st.text_input('Node id')
    with col_node_name:
        name = st.text_input('Node name')
        
    col_add_node, col_remove_node, col_edit_node = st.columns(3)

    with col_add_node:
        st.button('Add',  use_container_width=True, on_click=add_new_node, kwargs={'code': code, 'id': id, 'name': name})
    with col_remove_node:
        st.button('Remove', use_container_width=True)
    with col_edit_node:
        st.button('Edit',  use_container_width=True)

    connect_node_a, connect_node_b = st.columns(2)
    with connect_node_a:
        st.text_input('Node id (A)')
        st.button('Connect')
    with connect_node_b:
        st.text_input('Node id (B)')
        

with col_display:
    st_mermaid(code, height="500px")
