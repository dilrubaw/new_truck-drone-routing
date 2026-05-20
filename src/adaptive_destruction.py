import random
import math

from distance_matrix import compute_distance_matrix


def random_destruction(route, d=3):
    if len(route) <= d + 2:
        return route[:], []

    start_idx = random.randint(1, len(route) - d - 1)
    removed = route[start_idx:start_idx + d]
    remaining = route[:start_idx] + route[start_idx + d:]

    return remaining, removed


def worst_position_destruction(route, instance, d=3):
    if len(route) <= d + 2:
        return route[:], []

    distance_matrix = compute_distance_matrix(instance)
    marginal_costs = []

    for i in range(1, len(route) - 1):
        prev_node = route[i - 1]
        node = route[i]
        next_node = route[i + 1]

        marginal_cost = (
            distance_matrix[prev_node][node]
            + distance_matrix[node][next_node]
            - distance_matrix[prev_node][next_node]
        )

        marginal_costs.append((marginal_cost, node))

    marginal_costs.sort(key=lambda x: x[0], reverse=True)

    removed = [node for _, node in marginal_costs[:d]]
    removed_set = set(removed)

    remaining = [node for node in route if node not in removed_set]

    return remaining, removed


def zone_based_destruction(route, instance, d=3):
    if len(route) <= d + 2:
        return route[:], []

    distance_matrix = compute_distance_matrix(instance)

    middle_nodes = route[1:-1]
    center_node = random.choice(middle_nodes)

    distances = []

    for node in middle_nodes:
        distances.append((distance_matrix[center_node][node], node))

    distances.sort(key=lambda x: x[0])

    removed = [node for _, node in distances[:d]]
    removed_set = set(removed)

    remaining = [node for node in route if node not in removed_set]

    return remaining, removed


def reconstruct_route(remaining, removed):
    if not removed:
        return remaining[:]

    insert_pos = random.randint(1, len(remaining) - 1)

    return remaining[:insert_pos] + removed[::-1] + remaining[insert_pos:]


def select_operator(weights):
    total = sum(weights)
    r = random.uniform(0, total)

    cumulative = 0

    for idx, weight in enumerate(weights):
        cumulative += weight

        if cumulative >= r:
            return idx

    return len(weights) - 1


def update_operator_weights(
    weights,
    scores,
    counts,
    reaction_factor=0.1,
    min_weight=0.10
):
    new_weights = list(weights)

    for i in range(len(weights)):
        if counts[i] > 0:
            average_score = scores[i] / counts[i]
            new_weights[i] = (
                (1 - reaction_factor) * weights[i]
                + reaction_factor * average_score
            )

        new_weights[i] = max(new_weights[i], min_weight)

    total = sum(new_weights)

    return [weight / total for weight in new_weights]