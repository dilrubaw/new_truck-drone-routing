import math


def euclidean_distance(node_a, node_b):
    dx = node_a.x - node_b.x
    dy = node_a.y - node_b.y

    return math.sqrt(dx ** 2 + dy ** 2)


def compute_distance_matrix(instance):
    node_count = len(instance.nodes)

    matrix = [
        [0.0 for _ in range(node_count)]
        for _ in range(node_count)
    ]

    for i in range(node_count):
        for j in range(node_count):
            if i != j:
                matrix[i][j] = euclidean_distance(
                    instance.nodes[i],
                    instance.nodes[j]
                )

    return matrix


def compute_truck_time_matrix(instance):
    distance_matrix = compute_distance_matrix(instance)

    return [
        [
            distance / instance.truck_speed
            for distance in row
        ]
        for row in distance_matrix
    ]


def compute_drone_time_matrix(instance):
    distance_matrix = compute_distance_matrix(instance)

    return [
        [
            distance * instance.drone_speed
            for distance in row
        ]
        for row in distance_matrix
    ]