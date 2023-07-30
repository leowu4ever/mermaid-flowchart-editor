import streamlit as st

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
    return sorted(edges) if edges != [] else ['']

def get_all_nodes():
    nodes = sorted(list(st.session_state['nodes'].values()))
    return nodes if nodes != [] else ['']
    
def set_direction():
    pass

def set_theme():
    pass