import matplotlib.pyplot as plt
import networkx as nx

def decorate_modulename(prefix, modulename) -> str:
    return prefix + '.' + modulename

def build_graph(endpoints_dict, caller_dict):
    G = nx.DiGraph()
    for endpoint in endpoints_dict:
        node = decorate_modulename('api', endpoints_dict[endpoint])
        if node not in G.nodes:
            G.add_node(node, group='api')
    for caller in caller_dict:
        node = decorate_modulename('web', caller_dict[caller])
        if node not in G.nodes:
            G.add_node(node, group='web')
        if caller in endpoints_dict:
            G.add_edge(node, decorate_modulename('api', endpoints_dict[caller]))
    return G


def draw_graph(G, size=(12, 12)):
    groups = nx.get_node_attributes(G, 'group')

    api_nodes = [node for node, group in groups.items() if group == 'api']
    web_nodes = [node for node, group in groups.items() if group == 'web']

    pos = nx.spring_layout(G, k=3)

    for node in pos:
        if node in api_nodes:
            pos[node][0] += 0.8
            pos[node][1] += 0.8
        elif node in web_nodes:
            pos[node][0] -= 0.8
            pos[node][1] -= 0.8

    plt.figure(figsize=size)

    nx.draw_networkx_nodes(G, pos, nodelist=api_nodes, node_color='skyblue', label='API modules')
    nx.draw_networkx_nodes(G, pos, nodelist=web_nodes, node_color='lightcoral', label='Web modules')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.axis('off')
    plt.show()