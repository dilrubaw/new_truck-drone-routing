from pathlib import Path
from models import Node, ProblemInstance


def load_bouman_instance(file_path: str) -> ProblemInstance:
    """
    Gerçek Bouman dataset formatını okur.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Truck speed
    truck_speed = float(lines[1])

    # Drone speed
    drone_speed = float(lines[3])

    # Number of nodes
    node_count = int(lines[5])

    nodes = []

    # Depot line
    depot_parts = lines[7].split()
    depot_x = float(depot_parts[0])
    depot_y = float(depot_parts[1])

    nodes.append(Node(
        id=0,
        x=depot_x,
        y=depot_y
    ))

    # Customer nodes start after:
    # "/*The Locations (x_coor y_coor name)*/"
    start_index = 9

    for idx in range(node_count - 1):
        parts = lines[start_index + idx].split()

        x = float(parts[0])
        y = float(parts[1])

        nodes.append(Node(
            id=idx + 1,
            x=x,
            y=y
        ))

    battery_capacity = calculate_battery_capacity(
        nodes,
        drone_speed
    )

    return ProblemInstance(
        name=path.stem,
        nodes=nodes,
        truck_speed=truck_speed,
        drone_speed=drone_speed,
        battery_capacity=battery_capacity
    )


def calculate_battery_capacity(nodes, drone_speed: float) -> float:
    """
    Paper:
    Q = 2 * average drone travel time
    """

    total_time = 0
    count = 0

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:

                dx = nodes[i].x - nodes[j].x
                dy = nodes[i].y - nodes[j].y

                distance = (dx ** 2 + dy ** 2) ** 0.5

                travel_time = distance * drone_speed

                total_time += travel_time
                count += 1

    average_travel_time = total_time / count

    return 2 * average_travel_time