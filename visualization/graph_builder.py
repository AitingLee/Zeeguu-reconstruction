import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def decorate_modulename(prefix, modulename) -> str:
    if not modulename:
        return prefix
    return f"{prefix}.{modulename}"

def _adjust_x_position(nodes, pos, initial_x_range, target_x_range):
    adjusted_pos = {}
    min_x = initial_x_range[0]
    max_x = initial_x_range[1]

    if min_x != max_x:
        for node in nodes:
            normalized_x = (pos[node][0] - min_x) / (max_x - min_x)
            adjusted_pos[node] = [target_x_range[0] + normalized_x * (target_x_range[1] - target_x_range[0]), pos[node][1]]
    else:
        mean_target_x = np.mean(target_x_range)
        for node in nodes:
            adjusted_pos[node] = [mean_target_x, pos[node][1]]

    return adjusted_pos

def draw_graph(G, size=(12, 12)):
    groups = nx.get_node_attributes(G, 'group')
    api_nodes = [node for node, group in groups.items() if group == 'api']
    web_nodes = [node for node, group in groups.items() if group == 'web']
    pos = nx.spring_layout(G, k=0.3, iterations=50)

    api_x_init = [pos[n][0] for n in api_nodes] if api_nodes else [0]
    web_x_init = [pos[n][0] for n in web_nodes] if web_nodes else [0]

    initial_api_x_range = (min(api_x_init), max(api_x_init))
    initial_web_x_range = (min(web_x_init), max(web_x_init))

    target_web_x_range = (-2, -0.5)
    target_api_x_range = (0.5, 2)

    adjusted_pos = pos.copy()

    if web_nodes:
        adjusted_web_pos = _adjust_x_position(web_nodes, pos, initial_web_x_range, target_web_x_range)
        adjusted_pos.update(adjusted_web_pos)

    if api_nodes:
        adjusted_api_pos = _adjust_x_position(api_nodes, pos, initial_api_x_range, target_api_x_range)
        adjusted_pos.update(adjusted_api_pos)


    plt.figure(figsize=size)

    nx.draw_networkx_nodes(G, adjusted_pos, nodelist=api_nodes, node_color='skyblue', label='API modules', node_size=800)
    nx.draw_networkx_nodes(G, adjusted_pos, nodelist=web_nodes, node_color='lightcoral', label='Web modules', node_size=800)

    nx.draw_networkx_edges(G, adjusted_pos, alpha=0.5, width=1)

    labels = {node: G.nodes[node].get('original_name', node) for node in G.nodes()}
    nx.draw_networkx_labels(G, adjusted_pos, labels=labels, font_size=9)

    if web_nodes and api_nodes:
        mid_x = (target_web_x_range[1] + target_api_x_range[0]) / 2
        plt.axvline(x=mid_x, color='gray', linestyle='--')
    elif web_nodes:
         plt.axvline(x=target_web_x_range[1] + 0.2, color='gray', linestyle='--')
    elif api_nodes:
         plt.axvline(x=target_api_x_range[0] - 0.2, color='gray', linestyle='--')

    plt.title("API and Web Modules Dependency", fontsize=14)
    plt.legend(loc='upper right')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def top_level_package(module_name, depth):
    components = module_name.split(".")
    return ".".join(components[:depth])

def visualize_with_graph(usage_list, abstraction_level):

    G = nx.DiGraph()

    for usage_pairs in usage_list:
        web_node_original, api_node_original = usage_pairs
        abstract_web_node = top_level_package(web_node_original, abstraction_level)
        abstract_api_node = top_level_package(api_node_original, abstraction_level)
        web_node_id = decorate_modulename('web', abstract_web_node)
        api_node_id = decorate_modulename('api', abstract_api_node)
        G.add_node(web_node_id, group='web', original_name=abstract_web_node)
        G.add_node(api_node_id, group='api', original_name=abstract_api_node)
        G.add_edge(web_node_id, api_node_id)
    draw_graph(G)