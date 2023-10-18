from typing import List, Dict, Tuple, Optional

import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


def generate_graf(n: int) -> Graph:
    # G = nx.cycle_graph(n)
    g = nx.complete_graph(n)  # создаём объект графа
    return g


# подписи для ребер (их длина)
def generate_labels(distance_matrix: List[List[float]], n: int) -> Dict[Tuple[int, int], float]:
    edge_labels = {}
    for i in range(n):
        for j in range(i + 1, n):
            edge_labels[(i, j)] = round(distance_matrix[i][j], 3)
    return edge_labels


def generate_graf_width(feromon_matrix: List[List[float]], n: int) -> List[float]:
    """генерирум ширину ребер"""
    edge_width = []
    for i in range(n):
        for j in range(i + 1, n):
            edge_width.append(round(feromon_matrix[i][j], 3) + 1)
    return edge_width


# рисуем граф и отображаем его
def show_graph(graph: Graph, edge_width: List[float], labels: Optional[Dict[Tuple[int, int], float]]):
    pos = nx.circular_layout(graph)
    if labels is None:
        nx.draw(graph, with_labels=True, font_weight='bold', node_color='g', width=edge_width)
    else:
        nx.draw_networkx_edge_labels(graph, pos, labels, font_color='g')
        nx.draw(graph, with_labels=True, font_weight='bold', node_color='g', width=edge_width)
    plt.show(ion=True)
