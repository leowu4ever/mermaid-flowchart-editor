import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    if st.session_state['node_title'].replace(' ', '') != '':
        st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
        st.session_state['node_title'] = ''
        st.balloons()
        update_code()
    else:
        st.error('Node title is invalid.')
    
def remove_node():
    if len(st.session_state['nodes'].items()) > 0:
        del st.session_state['nodes'][st.session_state['node_remove_selected'].replace(' ', '_')]
        update_code()
    else:
        st.error('No node is selected.')
        
def add_edge():
    if st.session_state['node_a'] in st.session_state['edges'].keys():
        st.session_state['edges'][st.session_state['node_a']].add(st.session_state['node_b'])
    else:
        st.session_state['edges'][st.session_state['node_a']] = {st.session_state['node_b']}
    print(st.session_state['edges'])
    update_code()
    
def remove_edge():
    if st.session_state['node_a'] in st.session_state['edges'].keys():
        if st.session_state['node_b'] in st.session_state['edges'][st.session_state['node_a']]:
            st.session_state['edges'][st.session_state['node_a']].remove(st.session_state['node_b'])
            if not st.session_state['edges'][st.session_state['node_a']]:
                del st.session_state['edges'][st.session_state['node_a']]
            update_code()
        else:
            st.error('The edge doesn\'t exist')  
    else:
        st.error('The edge doesn\'t exist')
        
    
def update_code():
    st.session_state['code'] = 'flowchart'
    # update nodes
    if len(st.session_state['nodes'].items()) > 0:
        for node_id, node_title in st.session_state['nodes'].items():
            st.session_state['code'] += f'\n{node_id}[{node_title}]'
    # update edges
    if len(st.session_state['edges'].items()) > 0:
        for node_a, node_bs in st.session_state['edges'].items():
            for node_b in node_bs:
                st.session_state['code'] += f'\n{node_a}-->{node_b}'
            
if __name__ == '__main__':
    if 'code' not in st.session_state:
        st.session_state['code'] = ''
    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = {}
    
    if 'edges' not in st.session_state:
        st.session_state['edges'] = {}
            
    if 'subgraphs' not in st.session_state:
        st.session_state['subgraphs'] = {}
        
    st.set_page_config(layout='wide')
    col_config, col_display, col_code = st.columns([2.5,3,2])
    with col_config:
        st.header('Mermaid flow chart editor')
        st.write('Create Mermaid flow charts in a more manageable and efficient way.')
        st.subheader('Node')
        col_node_title, col_node_shape, col_node_add = st.columns([3,1.5, 1.5])
        col_node_title.text_input(label='', placeholder='node title', label_visibility='collapsed', on_change=add_node, key='node_title')
        col_node_shape.selectbox('Shape', label_visibility='collapsed', options=['square', 'round', 'container'])
        col_node_add.button('add', on_click=add_node, use_container_width=True)
        
        col_node_selected, col_node_remove = st.columns([4.5, 1.47])
        col_node_selected.selectbox('All nodes added', list(st.session_state['nodes'].values())[::-1], label_visibility='collapsed', key='node_remove_selected')
        col_node_remove.button('remove', on_click=remove_node, use_container_width=True)

        st.subheader('Edge')
        col_node_a, col_node_b = st.columns(2)
        col_node_a.selectbox('Node A', options=st.session_state['nodes'], key='node_a')
        col_node_b.selectbox('Node B', options=st.session_state['nodes'], key='node_b')
        
        col_edge_add, col_edge_remove = st.columns(2)
        col_edge_add.button('add an edge', use_container_width=True, on_click=add_edge)
        col_edge_remove.button('remove an edge', use_container_width=True, on_click=remove_edge)
        
        st.subheader('Group')
        col_group_selected, col_group_create = st.columns([4.5,1.5])        
        col_group_selected.multiselect('All nodes added', options=st.session_state['nodes'], label_visibility='collapsed')
        col_group_create.button('group', use_container_width=True)
        
    with col_display:
        if st.session_state['code'] != '':
            st_mermaid(st.session_state['code'], height=500)

    with col_code:
        st.code(st.session_state['code'], language='mermaid', line_numbers=True)
    st.write(st.session_state['nodes'])
    st.write(st.session_state['edges'])
