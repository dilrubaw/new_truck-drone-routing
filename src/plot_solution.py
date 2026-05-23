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

    sync_positions = [i for i, t in enumerate(types) if t == 0]

    truck_path = []
    drone_paths = []

    for idx in range(len(sync_positions) - 1):
        start_pos = sync_positions[idx]
        end_pos = sync_positions[idx + 1]

        segment_nodes = seq[start_pos:end_pos + 1]
        segment_types = types[start_pos:end_pos + 1]

        start_node = segment_nodes[0]
        end_node = segment_nodes[-1]

        if not truck_path:
            truck_path.append(start_node)

        truck_path.append(end_node)

        drone_path = [start_node]
        has_drone_flight = False

        for node, resource_type in zip(segment_nodes[1:-1], segment_types[1:-1]):
            if resource_type == 1:
                drone_path.append(node)
                has_drone_flight = True

        if has_drone_flight:
            drone_path.append(end_node)
            drone_paths.append(drone_path)

    return truck_path, drone_paths


def plot_solution(instance, solution, result, output_path):
    node_map = {node.id: node for node in instance.nodes}
    truck_path, drone_paths = build_paths_from_solution(solution)

    plt.figure(figsize=(12, 8))

    # Drone paths first, so truck stays visible on top
    for path in drone_paths:
        xs = [node_map[node_id].x for node_id in path]
        ys = [node_map[node_id].y for node_id in path]

        plt.plot(
            xs,
            ys,
            "r--",
            linewidth=1.5,
            alpha=0.65,
            label="Drone path",
            zorder=1
        )

    # Truck path drawn last and thick
    truck_xs = [node_map[node_id].x for node_id in truck_path]
    truck_ys = [node_map[node_id].y for node_id in truck_path]

    plt.plot(
        truck_xs,
        truck_ys,
        "b-",
        linewidth=4.0,
        alpha=0.95,
        label="Truck path",
        zorder=4
    )

    # Nodes
    for node in instance.nodes:
        plt.scatter(
            node.x,
            node.y,
            color="black",
            s=28,
            zorder=6
        )
        plt.text(
            node.x + 0.8,
            node.y + 0.8,
            str(node.id),
            fontsize=8,
            color="black",
            zorder=7
        )

    plt.title(
        f"Hybrid IG-SA Solution | "
        f"{instance.name} | "
        f"Makespan: {result['makespan']:.4f} | "
        f"Feasible: {result['feasible']}"
    )

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, alpha=0.3)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys())

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=250)
    plt.close()

    print(f"Saved solution plot to: {output_path}")
    print(f"Truck path: {truck_path}")
    print(f"Drone paths: {drone_paths}")


def main(node_count):
    if node_count not in INSTANCE_BY_NODE_COUNT:
        raise ValueError("Supported node counts: 5, 10, 20, 50")

    instance = load_bouman_instance(Path(INSTANCE_BY_NODE_COUNT[node_count]))

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