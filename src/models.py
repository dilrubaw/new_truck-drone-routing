from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Node:
    id: int
    x: float
    y: float


@dataclass
class ProblemInstance:
    name: str
    nodes: List[Node]
    truck_speed: float
    drone_speed: float
    battery_capacity: float


@dataclass
class Solution:
    node_sequence: List[int]      # pi_s
    resource_types: List[int]     # pi_t: 0 both, 1 drone, 2 truck