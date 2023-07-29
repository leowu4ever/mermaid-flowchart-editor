import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    if st.session_state['node_title'].replace(' ', '') != '':
        st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
        st.session_state['node_title'] = ''
        update_code()
    else:
        st.toast('Node title is invalid.')
    
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
        
def group_nodes():
    st.session_state['groups'][st.session_state['group_name']] = set(st.session_state['group_nodes'])
    update_code()
    
def ungroup_nodes():
    if st.session_state['group_selected'] in st.session_state['groups'].keys():
        del st.session_state['groups'][st.session_state['group_selected']]
    update_code()

def update_code():
    st.session_state['code'] = 'flowchart'
    # update group
    for group, nodes in st.session_state['groups'].items():
        st.session_state['code'] += f'\nsubgraph {group}'
        for node in nodes:
            st.session_state['code'] += f"\n{node.replace(' ', '_')}[{node}]"
        st.session_state['code'] += '\nend'

    # update nodes
    for node_id, node_title in st.session_state['nodes'].items():
        st.session_state['code'] += f'\n{node_id}[{node_title}]'
    # update edges
    for node_a, node_bs in st.session_state['edges'].items():
        for node_b in node_bs:
            st.session_state['code'] += f'\n{node_a}-->{node_b}'
    
            
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
        
    st.set_page_config(layout='wide')
    st.title('Mermaid flow chart editor')
    st.write('Create Mermaid flow charts in a more manageable and efficient way.')
        
    col_config, col_display, col_code = st.columns([2.5,3,2])
    with col_config:
        # config
        st.subheader('Config')
        col_direction, col_theme = st.columns(2)
        col_direction.selectbox('Chart direction', ['From left to right', 'from top to bottom'])
        col_theme.selectbox('Chart theme', ['base', 'forest', 'dark'])
        
        # node - add
        st.subheader('Node')
        col_node_title, col_node_shape = st.columns([3,1])
        col_node_title.text_input(label='Title', on_change=add_node, key='node_title')
        col_node_shape.selectbox('Shape', options=['square', 'ellipse', 'container'])
        st.button('add a new node', on_click=add_node, use_container_width=True)
        # node - remove
        st.selectbox('Select a node to remove', list(st.session_state['nodes'].values())[::-1], key='node_remove_selected')
        st.button('remove an existing node', on_click=remove_node, use_container_width=True)

        # edge - add
        st.subheader('Edge')
        col_node_a, col_node_b = st.columns(2)
        col_node_a.selectbox('Node/group A', options=st.session_state['nodes'], key='node_a')
        col_node_b.selectbox('Node/group B', options=st.session_state['nodes'], key='node_b')
        st.button('add an edge', use_container_width=True, on_click=add_edge)
        # edge - remove
        st.selectbox('Select an edge to remove', st.session_state['edges'].items())
        st.button('remove an existing edge', use_container_width=True, on_click=remove_edge)
        
        # group - add
        st.subheader('Group')
        st.multiselect('Select one/multiple node(s) to group', options=st.session_state['nodes'], key='group_nodes')
        col_group_name, col_group_create = st.columns([1,1])
        col_group_name.text_input('group name', label_visibility='collapsed', placeholder='group name', key='group_name')
        col_group_create.button('group', use_container_width=True, on_click=group_nodes)
        # group - remove
        st.selectbox('Select a group to ungroup', st.session_state['groups'].keys(), key='group_selected')
        st.button('ungroup an existing group', use_container_width=True, on_click=ungroup_nodes)
        
    with col_display:
        if st.session_state['code'] != '':
            st_mermaid(st.session_state['code'], height=500)

    with col_code:
        st.code(st.session_state['code'], language='mermaid', line_numbers=True)
    st.write(st.session_state['nodes'])
    st.write(st.session_state['edges'])
    st.write(st.session_state['groups'])
