import streamlit as st

def add_node():
    if st.session_state['node_title'].replace(' ', '') != '':
        if st.session_state['node_title'].replace(' ', '') not in st.session_state['nodes'].values():
            st.session_state['nodes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_title']
            st.session_state['shapes'][st.session_state['node_title'].replace(' ', '_')] = st.session_state['node_shape']
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
        del st.session_state['shapes'][st.session_state['node_remove_selected'].replace(' ', '_')]

        st.toast('Node removed successfully!', icon='🔥')
        update_code()
    else:
        st.toast('No node is selected.', icon='🚨')
        
def add_edge():
    # if node a already has seme edges, we extend the node b set
    if st.session_state['node_a'].replace(' ', '_') in st.session_state['edges'].keys():
        # if the pair is already added before
        if st.session_state['node_b'].replace(' ', '_') not in st.session_state['edges'][st.session_state['node_a'].replace(' ', '_')]:
            st.session_state['edges'][st.session_state['node_a'].replace(' ', '_')].add(st.session_state['node_b'].replace(' ', '_'))
            st.session_state['notes'][st.session_state['node_a'].replace(' ', '_')][st.session_state['node_b'].replace(' ', '_')] = st.session_state['edge_note']
            st.toast('Edge added successfully', icon='🔥')
            st.session_state['edge_note'] = ''
            update_code()
        else:
            st.toast('The edge is already added.', icon='🚨')
    # if node a doesn't have any edges, we create a new set to contain node b
    else:
        st.session_state['edges'][st.session_state['node_a'].replace(' ', '_')] = {st.session_state['node_b'].replace(' ', '_')}
        st.session_state['notes'][st.session_state['node_a'].replace(' ', '_')] = {st.session_state['node_b'].replace(' ', '_') : st.session_state['edge_note']}
        st.toast('Edge added successfully', icon='🔥')
        st.session_state['edge_note'] = ''
        update_code()

def remove_edge():
    # remove the edge 
    if st.session_state['edge_remove'] != '':
        node_a, node_b = st.session_state['edge_remove'].split(' --> ')
        st.session_state['edges'][node_a.replace(' ', '_')].remove(node_b.replace(' ', '_'))
        
        # see if node a still have any connecting nodes left
        if len(st.session_state['edges'][node_a.replace(' ', '_')]) == 0:
            del st.session_state['edges'][node_a.replace(' ', '_')]

        update_code()
        st.toast('Edge removed successfully', icon='🔥')
    else:
        st.toast('No edge is selected.', icon='🚨')

def update_code():
    theme = f"%%{{init: {{'theme':'{st.session_state['theme'].lower()}'}}}}%%"

    direction_map = {'From left to right': 'LR', 'From top to bottom': 'TB'}
    direction = direction_map[st.session_state['chart_direction']]
    st.session_state['code'] = f"{theme}\nflowchart {direction}\n"

    if len(st.session_state['nodes'].items()) > 0:

        # update nodes
        for node_id, node_title in st.session_state['nodes'].items():
                if st.session_state['shapes'][node_title.replace(' ', '_')] == 'rectangle':
                    st.session_state['code'] += f"{node_title.replace(' ', '_')}[{node_title}]\n"
                if st.session_state['shapes'][node_title.replace(' ', '_')] == 'ellipse':
                    st.session_state['code'] += f"{node_title.replace(' ', '_')}([{node_title}])\n"
                if st.session_state['shapes'][node_title.replace(' ', '_')] == 'container':
                    st.session_state['code'] += f"{node_title.replace(' ', '_')}[({node_title})]\n"
            
        # update edges
        for node_a, node_bs in st.session_state['edges'].items():
            for node_b in node_bs:
                note = st.session_state['notes'][node_a][node_b]
                # see if there an edge note attached
                if note == '':
                    st.session_state['code'] += f'\n{node_a}-->{node_b}'
                else:
                    st.session_state['code'] += f'\n{node_a}--{note}-->{node_b}'

        
def get_all_edges():
    edges = []
    for node_a, node_bs in st.session_state['edges'].items():
        for node_b in node_bs:
            edges.append(f"{node_a.replace('_', ' ')} --> {node_b.replace('_', ' ')}")
    return sorted(edges) if edges != [] else ['']

def get_all_nodes():
    nodes = sorted(list(st.session_state['nodes'].values()))
    return nodes if nodes != [] else ['']
    
def set_direction():
    update_code()
    
def set_theme():
    update_code()