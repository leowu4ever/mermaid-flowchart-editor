import streamlit as st
from streamlit_mermaid import st_mermaid
   
def add_new_node(ref, name):
    global code
    code += f'\n{ref}[{name}]'
        
if __name__ == '__main__':
    code = '''
           flowchart
           '''
    st.set_page_config(layout='wide')
    st.title('Mermaid visual editor')

    col_config, col_display, col_code = st.columns([3,4,2])
    with col_config:
        st.markdown('''
                    This tool aims to help you create some common diagrams supported by Mermaid.
                    Currently it can create flow chart.
                    ''')
        st.selectbox(label='Please select a diagram type', options=['Flow chart', 'Class chart', 'Gantt chart'])
        col_node_ref, col_node_name = st.columns(2)
        with col_node_ref:
            ref = st.text_input('Node reference')
        with col_node_name:
            name = st.text_input('Node name')
        
       
        col_add_node, col_remove_node, col_edit_node = st.columns(3)
        with col_add_node:
            btn_add_node = st.button('Add a node',  use_container_width=True)
            if btn_add_node:
                code += f'\n{ref}[{name}]'
                
        with col_remove_node:
            st.button('Remove a node', use_container_width=True)
        with col_edit_node:
            st.button('Edit a node',  use_container_width=True)

        col_node_a, col_node_b = st.columns(2)
        with col_node_a:
            st.text_input('Node id (A)')
        with col_node_b:
            st.text_input('Node id (B)')    

        col_add_edge, col_remove_edge, col_edit_edge = st.columns(3)
        with col_add_edge:
            st.button('Add an edge', use_container_width=True)
        with col_remove_edge:
            st.button('Remove an edge', use_container_width=True)
        with col_edit_edge:
            st.button('Edit an edge', use_container_width=True)
        
    with col_display:
        st.subheader('Chart generated')
        st_mermaid(code, height=1000)
        
    with col_code:
        st.subheader('Code generated')
        code_block = st.code(code, language='mermaid', line_numbers=True)
