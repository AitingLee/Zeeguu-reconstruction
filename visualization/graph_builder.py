import networkx as nx
import numpy as np
import plotly.graph_objects as go

HOVERED_EDGE_COLOR = 'orange'
HOVERED_EDGE_WIDTH = 2.5
DEFAULT_EDGE_COLOR = 'rgba(180,180,180,0.6)'
DEFAULT_EDGE_WIDTH = 1


def decorate_modulename(prefix, modulename) -> str:
    if not modulename:
        return prefix
    return f"{prefix}.{modulename}"


def top_level_package(module_name, depth):
    if not module_name:
        return ""
    components = module_name.split(".")
    if depth <= 0:
        return components[-1] if components else ""
    return ".".join(components[:depth])


def _adjust_x_position(nodes, pos, initial_x_range, target_x_range):
    adjusted_pos = {}
    min_x_initial, max_x_initial = initial_x_range
    min_x_target, max_x_target = target_x_range

    if not nodes:
        return adjusted_pos

    if min_x_initial == max_x_initial:
        mean_target_x = np.mean(target_x_range)
        for node in nodes:
            adjusted_pos[node] = [mean_target_x, pos[node][1]]
    else:
        for node in nodes:
            normalized_x = (pos[node][0] - min_x_initial) / (max_x_initial - min_x_initial)
            adjusted_pos[node] = [min_x_target + normalized_x * (max_x_target - min_x_target), pos[node][1]]
    return adjusted_pos


def get_node_positions(G):
    if not G.nodes():
        return {}

    pos = nx.spring_layout(G, k=0.6, iterations=80, seed=9)
    groups = nx.get_node_attributes(G, 'group')
    api_nodes = [node for node, group in groups.items() if group == 'api']
    web_nodes = [node for node, group in groups.items() if group == 'web']

    api_x_init = [pos[n][0] for n in api_nodes] if api_nodes else [0]
    web_x_init = [pos[n][0] for n in web_nodes] if web_nodes else [0]

    initial_api_x_range = (min(api_x_init), max(api_x_init))
    initial_web_x_range = (min(web_x_init), max(web_x_init))

    target_web_x_range = (-2.2, -0.6)
    target_api_x_range = (0.6, 2.2)

    adjusted_pos = pos.copy()
    if web_nodes:
        web_adjusted = _adjust_x_position(web_nodes, pos, initial_web_x_range, target_web_x_range)
        adjusted_pos.update(web_adjusted)
    if api_nodes:
        api_adjusted = _adjust_x_position(api_nodes, pos, initial_api_x_range, target_api_x_range)
        adjusted_pos.update(api_adjusted)
    return adjusted_pos


def visualize_with_graph(usage_list, selected_folders, hovered_node_id=None):

    G = nx.DiGraph()
    abstraction_level = 1
    filtered_usage_for_graph = []
    if usage_list:
        for web_original, api_original in usage_list:
            web_top_level_for_filtering = top_level_package(web_original, 1)
            if web_top_level_for_filtering in selected_folders:
                filtered_usage_for_graph.append((web_original, api_original))

    for web_node_original, api_node_original in filtered_usage_for_graph:
        abstract_web_node = top_level_package(web_node_original, abstraction_level)
        abstract_api_node = top_level_package(api_node_original, abstraction_level)

        if not abstract_web_node or not abstract_api_node:
            continue

        web_node_id = decorate_modulename('web', abstract_web_node)
        api_node_id = decorate_modulename('api', abstract_api_node)

        G.add_node(web_node_id, group='web', original_name=abstract_web_node)
        G.add_node(api_node_id, group='api', original_name=abstract_api_node)
        G.add_edge(web_node_id, api_node_id)

    if not G.nodes():
        fig = go.Figure()
        fig.update_layout(title="No Data", xaxis={'visible': False}, yaxis={'visible': False},
                          plot_bgcolor='white')
        return fig

    adjusted_pos = get_node_positions(G)

    edge_x, edge_y, edge_customdata, edge_text = [], [], [], []
    for edge_tuple in G.edges():
        u, v = edge_tuple
        x0, y0 = adjusted_pos[u]
        x1, y1 = adjusted_pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_customdata.extend([None, None, None])
        edge_text.extend(["", "", ""])

    base_edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=DEFAULT_EDGE_WIDTH, color=DEFAULT_EDGE_COLOR),
        hoverinfo='none',
        mode='lines', name='base_edges'
    )

    # Highlighted Edges (connected to hovered_node_id)
    highlighted_edges_x, highlighted_edges_y = [], []
    if hovered_node_id and hovered_node_id in G.nodes():
        for u, v in G.edges():
            if u == hovered_node_id or v == hovered_node_id:
                if u in adjusted_pos and v in adjusted_pos:
                    x0, y0 = adjusted_pos[u]
                    x1, y1 = adjusted_pos[v]
                    highlighted_edges_x.extend([x0, x1, None])
                    highlighted_edges_y.extend([y0, y1, None])

    highlighted_edges_trace = go.Scatter(
        x=highlighted_edges_x, y=highlighted_edges_y,
        line=dict(width=HOVERED_EDGE_WIDTH, color=HOVERED_EDGE_COLOR),
        hoverinfo='skip',
        mode='lines',
        name='highlighted_edges'
    )

    node_x_web, node_y_web, node_text_web, node_custom_web = [], [], [], []
    node_x_api, node_y_api, node_text_api, node_custom_api = [], [], [], []

    for node_id_from_graph in G.nodes():
        x, y = adjusted_pos[node_id_from_graph]
        node_info = G.nodes[node_id_from_graph]
        node_label = node_info.get('original_name', node_id_from_graph)
        group = node_info.get('group')

        if group == 'web':
            node_x_web.append(x)
            node_y_web.append(y)
            node_text_web.append(node_label)
            node_custom_web.append(node_id_from_graph)
        elif group == 'api':
            node_x_api.append(x)
            node_y_api.append(y)
            node_text_api.append(node_label)
            node_custom_api.append(node_id_from_graph)

    web_node_trace = go.Scatter(
        x=node_x_web, y=node_y_web, mode='markers+text',
        marker=dict(symbol='circle', size=18, color='lightcoral', line=dict(width=1, color='DarkSlateGrey')),
        text=node_text_web, textposition="bottom center",
        customdata=node_custom_web,
        hovertemplate='<b>Web Module</b><br>%{text}<extra></extra>',
        name='Web Modules'
    )
    api_node_trace = go.Scatter(
        x=node_x_api, y=node_y_api, mode='markers+text',
        marker=dict(symbol='circle', size=18, color='skyblue', line=dict(width=1, color='DarkSlateGrey')),
        text=node_text_api, textposition="bottom center",
        customdata=node_custom_api,
        hovertemplate='<b>API Module</b><br>%{text}<extra></extra>',
        name='API Modules'
    )

    fig_data = [base_edge_trace, highlighted_edges_trace, web_node_trace, api_node_trace]
    fig = go.Figure(data=fig_data)

    target_web_x_range_max = -0.8
    target_api_x_range_min = 0.8
    has_web_nodes = any(G.nodes[n]['group'] == 'web' for n in G.nodes())
    has_api_nodes = any(G.nodes[n]['group'] == 'api' for n in G.nodes())
    mid_x_val = None
    if has_web_nodes and has_api_nodes:
        mid_x_val = (target_web_x_range_max + target_api_x_range_min) / 2
    elif has_web_nodes:
        mid_x_val = target_web_x_range_max + 0.1
    elif has_api_nodes:
        mid_x_val = target_api_x_range_min - 0.1
    if mid_x_val is not None:
        fig.add_vline(x=mid_x_val, line_width=1, line_dash="dash", line_color="darkgray")

    fig.update_layout(
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2.8, 2.8]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor='white'
    )
    return fig