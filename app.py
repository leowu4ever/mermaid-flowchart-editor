import streamlit as st
from streamlit_mermaid import st_mermaid

def add_node():
    if st.session_state['node_title'].replace(' ', '') != '':
        if st.session_state['node_title'].replace(' ', '') not in st.session_state['nodes'].values():
            st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
            st.session_state['shapes'][st.session_state['node_title']] = st.session_state['node_shape']
            st.session_state['node_title'] = ''
            st.toast('Node added successfully', icon='🔥')
            update_code()
        else:
            st.toast('Node is already exited.', icon='🚨')

    else:
        st.toast('Node title is invalid.', icon='🚨')
    
def remove_node():
    if len(st.session_state['nodes'].items()) > 0:
        del st.session_state['nodes'][st.session_state['node_remove_selected'].replace(' ', '_')]
        del st.session_state['shapes'][st.session_state['node_remove_selected']]

        st.toast('Node removed successfully', icon='🔥')
        update_code()
    else:
        st.toast('No node is selected.', icon='🚨')
        
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
    st.session_state['code'] = '''
                               flowchart
                               '''

    if len(st.session_state['nodes'].items()) > 0:
        st.session_state['code'] = 'flowchart'
        # update group
        for group, titles in st.session_state['groups'].items():
            st.session_state['code'] += f'\nsubgraph {group}'
            for title in titles:
                if st.session_state['shapes'][title] == 'rectangle':
                    st.session_state['code'] += f"\n{title.replace(' ', '_')}[{title}]"
                if st.session_state['shapes'][title] == 'ellipse':
                    st.session_state['code'] += f"\n{title.replace(' ', '_')}([{title}])"
                if st.session_state['shapes'][title] == 'container':
                    st.session_state['code'] += f"\n{title.replace(' ', '_')}[({title})]"
            st.session_state['code'] += '\nend'

        # update nodes
        for node_id, node_title in st.session_state['nodes'].items():
                if st.session_state['shapes'][node_title] == 'rectangle':
                    st.session_state['code'] += f"\n{node_title.replace(' ', '_')}[{node_title}]"
                if st.session_state['shapes'][node_title] == 'ellipse':
                    st.session_state['code'] += f"\n{node_title.replace(' ', '_')}([{node_title}])"
                if st.session_state['shapes'][node_title] == 'container':
                    st.session_state['code'] += f"\n{node_title.replace(' ', '_')}[({node_title})]"
            
        # update edges
        for node_a, node_bs in st.session_state['edges'].items():
            for node_b in node_bs:
                st.session_state['code'] += f'\n{node_a}-->{node_b}'
        
def get_all_edges():
    edges = []
    for node_a, node_bs in st.session_state['edges'].items():
        for node_b in node_bs:
            edges.append(f'{node_a} --> {node_b}')
    return edges

def set_direction():
    pass

def set_theme():
    pass
     
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
                    # Mermaid flow chart editor                    
                    Help you create Mermaid flow charts in a more manageable and efficient way.
                    
                    *Developed by Leo Wu*

                    ## Quick start
                    A flow chart has two fundamental elements, nodes and edges which can be created in the corresponding tab on the right.
                    Any number of nodes can be grouped to form a subgraph. An edge can connect a node with another node or group of nodes.
                    
                    ''' )
        st.subheader('Experimental features')
        st.checkbox(':smiling_imp: I want some fun!!!')
        st.checkbox(':turtle: I feel lazy?!?!')
    # main area
    col_config, col_display, col_code = st.columns([2,3,2])
    with col_config:
        
        tab_node, tab_edge, tab_group, tab_config = st.tabs(['Node', 'Edge', 'Group', 'Configuration'])

        with tab_node:
            # node - add
            col_node_title, col_node_shape = st.columns([3,1])
            col_node_title.text_input(label='Node title', key='node_title', on_change=add_node)
            col_node_shape.selectbox('Node shape', options=['rectangle', 'ellipse', 'container'], key='node_shape')
            st.button('add a new node', on_click=add_node, use_container_width=True)
            # node - remove
            st.selectbox('Select a node to remove', list(st.session_state['nodes'].values())[::-1], key='node_remove_selected')
            st.button('remove an existing node', on_click=remove_node, use_container_width=True)

        with tab_edge:
            # edge - add
            col_node_a, col_node_b = st.columns(2)
            col_node_a.selectbox('A (node/group)', options=st.session_state['nodes'], key='node_a')
            col_node_b.selectbox('B (node/group)', options=st.session_state['nodes'], key='node_b')
            st.text_input('Edge note', placeholder='Can leave as blank')
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
            col_direction, col_theme = st.columns(2)
            col_direction.selectbox('Chart direction', ['From left to right', 'from top to bottom'])
            col_theme.selectbox('Chart theme', ['base', 'forest', 'dark'])
        
        
    with col_display:
        if st.session_state['code'] != '':
            st_mermaid(st.session_state['code'], height=500)

    with col_code:
        st.code(st.session_state['code'], language='mermaid', line_numbers=True)
        st.write(st.session_state['nodes'])
        st.write(st.session_state['edges'])
        st.write(st.session_state['groups'])
        st.write(st.session_state['shapes'])
