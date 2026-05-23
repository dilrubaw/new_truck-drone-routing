from pathlib import Path
import argparse
import matplotlib.pyplot as plt

from data_loader import load_bouman_instance
from hybrid_solver import hybrid_ig_sa


INSTANCE_BY_NODE_COUNT = {
    5: "data/singlecenter/singlecenter-1-n5.txt",
    10: "data/singlecenter/singlecenter-51-n10.txt",
    20: "data/singlecenter/singlecenter-61-n20.txt",
    50: "data/singlecenter/singlecenter-71-n50.txt",
}


def build_paths_from_solution(solution):
    seq = solution.node_sequence
    types = solution.resource_types

    sync_positions = [
        i for i, resource_type in enumerate(types)
        if resource_type == 0
    ]

    truck_paths = []
    drone_paths = []

    for idx in range(len(sync_positions) - 1):
        start_pos = sync_positions[idx]
        end_pos = sync_positions[idx + 1]

        segment_nodes = seq[start_pos:end_pos + 1]
        segment_types = types[start_pos:end_pos + 1]

        truck_path = [segment_nodes[0]]
        drone_path = [segment_nodes[0]]

        for node, resource_type in zip(segment_nodes[1:-1], segment_types[1:-1]):
            if resource_type == 1:
                drone_path.append(node)
            elif resource_type == 2:
                truck_path.append(node)
            elif resource_type == 0:
                truck_path.append(node)
                drone_path.append(node)

                truck_path.append(segment_nodes[-1])
        truck_paths.append(truck_path)

        has_drone_flight = any(
            resource_type == 1
            for resource_type in segment_types[1:-1]
        )

        if has_drone_flight:
            drone_path.append(segment_nodes[-1])
            drone_paths.append(drone_path)

    return truck_paths, drone_paths


def plot_solution(instance, solution, result, output_path):
    node_map = {node.id: node for node in instance.nodes}

    truck_paths, drone_paths = build_paths_from_solution(solution)

    plt.figure(figsize=(11, 7))

    for node in instance.nodes:
        plt.scatter(
            node.x,
            node.y,
            color="black",
            s=25,
            zorder=3
        )
        plt.text(
            node.x + 0.8,
            node.y + 0.8,
            str(node.id),
            fontsize=8,
            color="black"
        )

    for path in truck_paths:
        xs = [node_map[node_id].x for node_id in path]
        ys = [node_map[node_id].y for node_id in path]

        plt.plot(
            xs,
            ys,
            color="blue",
            linewidth=2.5,
            label="Truck path",
            zorder=2
        )

    for path in drone_paths:
        xs = [node_map[node_id].x for node_id in path]
        ys = [node_map[node_id].y for node_id in path]

        plt.plot(
            xs,
            ys,
            color="red",
            linestyle="--",
            linewidth=1.8,
            label="Drone path",
            zorder=1
        )

    plt.title(
        f"Hybrid IG-SA Truck-Drone Solution | "
        f"Instance: {instance.name} | "
        f"Makespan: {result['makespan']:.4f}"
    )

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, alpha=0.4)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys())

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved solution plot to: {output_path}")


def main(node_count):
    if node_count not in INSTANCE_BY_NODE_COUNT:
        raise ValueError("Supported node counts: 5, 10, 20, 50")

    instance_path = Path(INSTANCE_BY_NODE_COUNT[node_count])
    instance = load_bouman_instance(instance_path)

    best_solution, best_result, _ = hybrid_ig_sa(
        instance,
        max_iterations=1000,
        initial_temperature=500.0,
        base_cooling_rate=0.995,
        stagnation_limit=50,
        time_limit_seconds=30
    )

    output_path = Path(f"results/hybrid_solution_plot_n{node_count}.png")

    plot_solution(instance, best_solution, best_result, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=int, required=True)
    args = parser.parse_args()

    main(args.nodes)