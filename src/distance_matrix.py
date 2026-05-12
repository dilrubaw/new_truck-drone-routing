import numpy as np
from models import ProblemInstance


def compute_distance_matrix(instance: ProblemInstance) -> np.ndarray:
    nodes = instance.nodes
    n = len(nodes)

    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dx = nodes[i].x - nodes[j].x
            dy = nodes[i].y - nodes[j].y
            matrix[i][j] = (dx ** 2 + dy ** 2) ** 0.5

    return matrix


def compute_truck_time_matrix(instance: ProblemInstance) -> np.ndarray:
    distance_matrix = compute_distance_matrix(instance)
    return distance_matrix / instance.truck_speed


def compute_drone_time_matrix(instance: ProblemInstance) -> np.ndarray:
    distance_matrix = compute_distance_matrix(instance)
    return distance_matrix / instance.drone_speed