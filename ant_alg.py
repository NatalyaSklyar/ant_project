from typing import List, Dict
import numpy as np
import random
# import json
# from dash import Dash, html
# import dash_cytoscape as cyto
# data = {}


def tolist(np_array: np.ndarray) -> List[List[float]]:
    arr = list()
    for i in np_array:
        arr.append(list(i))
    return arr


def create_distance_matrix(n: int) -> List[List[float]]:
    """создаем матрицу расстояний"""
    distance_matrix = np.random.rand(n, n)
    for i in range(0, n):
        for j in range(i, n):
            if i == j:
                distance_matrix[j][i] = 0
            else:
                distance_matrix[j][i] = distance_matrix[i][j]
    # distance_matrix = tolist(distance_matrix)
    return tolist(distance_matrix)


def create_feromon_matrix(n: int, t0: float) -> List[List[float]]:
    """редактируем матрицу ферамонов"""
    feromon_matrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(i, n):
            if i != j:
                feromon_matrix[i][j] = t0
                feromon_matrix[j][i] = t0
    feromon_matrix = tolist(feromon_matrix)
    return feromon_matrix

# data["feromon"] = feromon_matrix
# data["distance"] = distance_matrix
# with open("data.json", "w") as file:
#     json.dump(data, file)


def choose_with_probability(probabilities: Dict) -> int:
    """выбор ключа словоря с учетом весов значений"""
    keys = list(probabilities.keys())
    probabilities = list(probabilities.values())

    random_number = random.random()

    cumulative_probability = 0
    chosen_key = None

    for key, probability in zip(keys, probabilities):
        cumulative_probability += probability
        if random_number < cumulative_probability:
            chosen_key = key
            break

    return chosen_key


def choose_next_point(
        feromon_matrix: List[List[float]],
        distance_matrix: List[List[float]],
        actual_point: int,
        available_points: List[int],
        alpha: float, beta: float) -> int:
    """выбор следующей вершины"""
    probabilities_dict = {}
    for point in available_points:
        probabilities_dict[point] = feromon_matrix[point][actual_point] ** alpha / (
                distance_matrix[actual_point][point] ** beta)

    total = sum(probabilities_dict.values())

    for point in probabilities_dict:
        probabilities_dict[point] /= total

    return choose_with_probability(probabilities_dict)


def get_path(feromon_matrix: List[List[float]],
             distance_matrix: List[List[float]],
             start_pos: int, alpha: float, beta: float, n: int) -> List[int]:
    """составляет путь из одной вершины"""
    current_pos = start_pos
    actual_path = [start_pos]

    available_points = list(np.arange(0, n))
    available_points.remove(current_pos)

    for _ in range(n - 1):
        current_pos = choose_next_point(feromon_matrix, distance_matrix, current_pos, available_points, alpha, beta)
        actual_path.append(current_pos)
        available_points.remove(current_pos)

    return actual_path


def get_path_length(distance_matrix: List[List[float]], actual_path: List[int], n: int) -> float:
    """длина пути"""
    length = 0

    for i in range(n):
        length += distance_matrix[actual_path[i]][actual_path[(i + 1) % n]]

    return length


def change_feromon(feromon_matrix: List[List[float]], p: float, i: int, j: int):
    """"редактирование количества феромона после прохождения одного круга"""
    feromon_matrix[i][j] = round(feromon_matrix[i][j] * (1 - p), 3)

    if feromon_matrix[i][j] > 10:
        feromon_matrix = [[elem / 2 + 1 for elem in row] for row in feromon_matrix]
    feromon_matrix[j][i] = feromon_matrix[i][j]

    return feromon_matrix


def do_all_ants_circle(feromon_matrix: List[List[float]], distance_matrix: List[List[float]],
                       q: float, p: float, alpha: float, beta: float, n: int) -> List[List[float]]:
    """круг с началом в каждом из городов"""

    paths = []
    for start_pos in range(n):
        paths.append(get_path(feromon_matrix, distance_matrix, start_pos, alpha, beta, n))

    for i in range(n):
        for j in range(i, n):
            feromon_matrix = change_feromon(feromon_matrix, p, i, j)

    for actual_path in paths:
        actual_length = get_path_length(distance_matrix, actual_path, n)

        for i in range(n):
            i1 = actual_path[i]
            i2 = actual_path[(i + 1) % n]
            feromon_matrix[i1][i2] += round(q / actual_length, 3)
            feromon_matrix[i2][i1] = feromon_matrix[i1][i2]

    return feromon_matrix
