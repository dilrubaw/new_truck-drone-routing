# New Truck-Drone Routing

This project implements and compares heuristic optimization algorithms for the Truck-Drone Team Logistics (TDTL) problem using Bouman single-center benchmark instances.

The project is based on Paper 8:

> Truck-Drone Team Logistics: A Heuristic Approach to Multi-Drop Route Planning

The main objective is to minimize total completion time (makespan) while satisfying synchronization and drone battery constraints.

---

# Project Overview

The system considers:

- One truck
- One drone
- Open-route structure
- Truck-drone synchronization points
- Drone battery limitations
- Multi-drop drone trips
- Euclidean distance-based travel times

The truck acts as both a delivery vehicle and a mobile synchronization platform for the drone.

The drone can serve customers independently between synchronization points as long as its battery constraint is satisfied.

---

# Academic Goal

The project requirements include:

1. Understanding the optimization problem from the assigned academic paper
2. Implementing the baseline algorithm from the paper
3. Developing an improved version of the algorithm
4. Running benchmark experiments
5. Comparing results
6. Producing graphs and evaluation outputs
7. Preparing a final runnable demonstration

---

# Team Contributions

The project was divided into three main development areas.

| Area | Main Responsibility |
|---|---|
| Core infrastructure | Dataset loading, evaluation, feasibility checking |
| Baseline algorithm | Paper 8 IG-SA implementation |
| Improved algorithm | Hybrid improvements, benchmarking, visualization |

---

# Baseline Algorithm

The baseline implementation follows the logic described in Paper 8.

Main components include:

- Initial solution generation
- Route improvement
- Synchronization construction
- Iterated Greedy destruction and reconstruction
- Simulated Annealing acceptance

The baseline algorithm is used as the comparison reference for all experiments.

---

# Improved Hybrid IG-SA Algorithm

The improved algorithm extends the baseline approach using additional optimization mechanisms.

Main improvements:

| Improvement | Purpose |
|---|---|
| Adaptive destruction | Increase diversification |
| Or-Opt local search | Improve route quality |
| Adaptive cooling | Improve exploration during stagnation |

The hybrid method keeps the original Paper 8 structure while introducing adaptive search behavior.

---

# Adaptive Destruction

Three destruction operators are used:

| Operator | Description |
|---|---|
| Random destruction | Removes random route segments |
| Worst-position destruction | Removes costly nodes |
| Zone-based destruction | Removes geographically close nodes |

Operator weights are updated dynamically according to performance.

---

# Or-Opt Local Search

Or-Opt relocates consecutive blocks of nodes within the route.

Tested block sizes:

```text
1-node
2-node
3-node
```

The goal is to improve the route structure before rebuilding synchronization points.

---

# Adaptive Cooling

Adaptive cooling dynamically modifies the Simulated Annealing cooling schedule.

If improvement stagnates, cooling slows down to allow additional exploration.

---

# Benchmark Structure

The benchmark compares:

| Algorithm | Description |
|---|---|
| Paper 8 IG-SA | Original baseline method |
| Hybrid IG-SA | Improved method |

Tested benchmark instances:

| Instance | Node Count |
|---|---:|
| singlecenter-1-n5 | 5 |
| singlecenter-51-n10 | 10 |
| singlecenter-61-n20 | 20 |
| singlecenter-71-n50 | 50 |

Each algorithm is executed multiple times for each instance.

---

# Benchmark Results

| Instance | Nodes | Baseline Makespan | Hybrid Makespan | Improvement |
|---|---:|---:|---:|---:|
| singlecenter-1-n5 | 5 | 385.1449 | 385.1449 | 0.00% |
| singlecenter-51-n10 | 10 | 697.4780 | 697.4780 | 0.00% |
| singlecenter-61-n20 | 20 | 1085.1319 | 1085.1319 | 0.00% |
| singlecenter-71-n50 | 50 | 1326.5556 | 1318.5634 | 0.60% |

---

# Result Interpretation

The baseline algorithm already produces strong solutions for smaller instances.

Because of this:

- n=5
- n=10
- n=20

show little or no improvement.

The Hybrid IG-SA method becomes more useful for larger and more complex instances such as:

```text
n = 50
```

The hybrid method also increases runtime because it applies additional adaptive and local search operations.

---

# Generated Outputs

The project generates:

| Output | Description |
|---|---|
| Comparison CSV | Baseline vs hybrid results |
| Makespan graph | Makespan comparison |
| Runtime graph | Runtime comparison |
| Improvement graph | Improvement percentage |

Generated visualization files:

```text
results/hybrid_vs_baseline_makespan.png
results/hybrid_vs_baseline_runtime.png
results/hybrid_improvement_percent.png
```

---

# Final Demo

A runnable demo is included.

Supported node counts:

```text
5
10
20
50
```

Example:

```bash
python src/run_demo.py --nodes 50
```

The demo:

1. Runs the Paper 8 baseline
2. Runs the Hybrid IG-SA algorithm
3. Compares results
4. Displays feasibility status
5. Displays best route information

---

# Installation

## macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# Requirements

Main libraries used:

```text
pandas
numpy
matplotlib
networkx
```

---

# How to Run

## Run Demo

```bash
python src/run_demo.py --nodes 5
python src/run_demo.py --nodes 10
python src/run_demo.py --nodes 20
python src/run_demo.py --nodes 50
```

## Run Full Benchmark

```bash
python src/experiment_runner.py
```

## Generate Graphs

```bash
python src/visualization.py
```

---

# Feasibility Validation

Solutions are validated according to:

- Synchronization correctness
- Drone battery capacity
- Route structure
- Travel times
- Battery violations

A solution is feasible when:

```text
total_battery_violation = 0
```

---

# Cross-Platform Compatibility

The project is compatible with:

- macOS
- Windows

The repository uses:

- relative paths
- portable project structure
- virtual environment support
- dependency management with `requirements.txt`

---

# Repository Structure

```text
new_truck-drone-routing/
│
├── data/
├── results/
├── src/
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Final Status

| Component | Status |
|---|---:|
| Dataset loading | Completed |
| Evaluator | Completed |
| Paper 8 baseline | Completed |
| Adaptive destruction | Completed |
| Or-Opt local search | Completed |
| Adaptive cooling | Completed |
| Hybrid IG-SA | Completed |
| Benchmark comparison | Completed |
| Visualization pipeline | Completed |
| Final demo | Completed |

---

# Quick Commands

```bash
python src/run_demo.py --nodes 50

python src/experiment_runner.py

python src/visualization.py
```
