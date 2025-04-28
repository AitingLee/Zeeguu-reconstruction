
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_grouped_graph(G):
    # 1. 為節點添加分組屬性
    node_groups = {}
    for node in G.nodes:
        if node.startswith('web.'):
            node_groups[node] = 'web'
        elif node.startswith('/'):
            node_groups[node] = 'route'
        elif node.startswith('db.'):
            node_groups[node] = 'db'
        else:
            node_groups[node] = 'other'  # 處理其他未分類的節點

    nx.set_node_attributes(G, node_groups, 'group')

    # 2. 獲取唯一的群組
    unique_groups = sorted(list(set(node_groups.values())))
    group_map = {group: i for i, group in enumerate(unique_groups)}
    node_colors = [plt.cm.get_cmap('viridis')(group_map[G.nodes[node]['group']] / len(unique_groups)) for node in G.nodes()]

    # 3. 使用佈局演算法計算初始位置
    pos = nx.spring_layout(G, seed=42)

    # 4. 根據分組調整節點位置 (簡單的平移)
    group_centers = {group: np.array([0.0, 0.0]) for group in unique_groups}
    group_counts = {group: 0 for group in unique_groups}
    for node, p in pos.items():
        group = G.nodes[node]['group']
        group_centers[group] += p
        group_counts[group] += 1

    for group in unique_groups:
        if group_counts[group] > 0:
            group_centers[group] /= group_counts[group]

    for node in G.nodes:
        group = G.nodes[node]['group']
        displacement = (group_centers[group] - pos[node]) * 0.1
        pos[node] += displacement

    # 5. 繪製圖形
    fig, ax = plt.subplots(figsize=(8, 6))

    for group in unique_groups:
        nodelist = [node for node in G.nodes if G.nodes[node]['group'] == group]
        nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_color=[plt.cm.get_cmap('viridis')(group_map[group] / len(unique_groups))] * len(nodelist), label=group)

    nx.draw_networkx_edges(G, pos, arrows=True, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Module Dependencies Grouped by Prefix")
    plt.legend()
    plt.axis('off')
    plt.show()

G = nx.DiGraph()
G.add_node('web.userArticle')
G.add_node('/article_opened')
G.add_node('db.UserArticle')
G.add_node('db.Article')
G.add_node('db.User')

G.add_node('web.student')
G.add_node('/join_cohort')
G.add_node('db.Cohort')
G.add_node('db.User')

G.add_edge('web.userArticle','/article_opened')
G.add_edge('/article_opened','db.UserArticle')
G.add_edge('/article_opened','db.Article')
G.add_edge('/article_opened','db.User')

G.add_edge('web.student','/join_cohort')
G.add_edge('/join_cohort','db.Cohort')
G.add_edge('/join_cohort','db.User')


draw_grouped_graph(G)