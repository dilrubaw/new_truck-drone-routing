import argparse
from pathlib import Path

from data_loader import load_bouman_instance
from paper8_ig_sa import paper8_ig_sa
from improved_algorithm import hybrid_ig_sa


INSTANCE_BY_NODE_COUNT = {
    5: "data/singlecenter/singlecenter-1-n5.txt",
    10: "data/singlecenter/singlecenter-51-n10.txt",
    20: "data/singlecenter/singlecenter-61-n20.txt",
    50: "data/singlecenter/singlecenter-71-n50.txt",
}


def print_segment_details(result, label):
    print(f"\n{label} segment details:")

    for segment in result.get("segments", []):
        print(
            f"Segment {segment['segment']}: "
            f"{segment['from_node']} -> {segment['to_node']} | "
            f"truck_time={segment['truck_time']:.4f}, "
            f"drone_time={segment['drone_time']:.4f}, "
            f"duration={segment['segment_duration']:.4f}, "
            f"battery_excess={segment['battery_excess']:.4f}"
        )

    print(f"\n{label} battery capacity: {result['battery_capacity']:.4f}")
    print(f"{label} total battery violation: {result['total_battery_violation']:.4f}")


def run_demo(node_count):
    if node_count not in INSTANCE_BY_NODE_COUNT:
        raise ValueError("Supported node counts: 5, 10, 20, 50")

    instance = load_bouman_instance(Path(INSTANCE_BY_NODE_COUNT[node_count]))

    print(f"Instance: {instance.name}")
    print(f"Node count: {len(instance.nodes)}")
    print(f"Truck speed: {instance.truck_speed}")
    print(f"Drone speed factor: {instance.drone_speed}")
    print(f"Battery capacity: {instance.battery_capacity:.4f}")

    print("\nRunning simplified Paper-8-inspired IG-SA baseline...")
    baseline_solution, baseline_result, _ = paper8_ig_sa(
        instance,
        max_iterations=1000,
        initial_temperature=500.0,
        cooling_rate=0.995,
        time_limit_seconds=30
    )

    print("\nRunning Hybrid IG-SA...")
    hybrid_solution, hybrid_result, _ = hybrid_ig_sa(
        instance,
        max_iterations=1000,
        initial_temperature=500.0,
        base_cooling_rate=0.995,
        stagnation_limit=50,
        time_limit_seconds=30
    )

    baseline = baseline_result["makespan"]
    hybrid = hybrid_result["makespan"]

    improvement = ((baseline - hybrid) / baseline) * 100 if baseline else 0.0

    print("\nRESULT COMPARISON")
    print(f"Baseline makespan: {baseline:.4f}")
    print(f"Hybrid makespan:   {hybrid:.4f}")
    print(f"Improvement:       {improvement:.2f}%")
    print(f"Baseline feasible: {baseline_result['feasible']}")
    print(f"Hybrid feasible:   {hybrid_result['feasible']}")

    print("\nBaseline node sequence:")
    print(baseline_solution.node_sequence)

    print("\nBaseline resource types:")
    print(baseline_solution.resource_types)

    print("\nHybrid node sequence:")
    print(hybrid_solution.node_sequence)

    print("\nHybrid resource types:")
    print(hybrid_solution.resource_types)

    print_segment_details(baseline_result, "Baseline")
    print_segment_details(hybrid_result, "Hybrid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=int, required=True)
    args = parser.parse_args()

    run_demo(args.nodes)