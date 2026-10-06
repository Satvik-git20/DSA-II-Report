# Public Transport Route Scheduling System

A Data Structures and Algorithms II project for modeling public transport networks
and finding efficient routes using graph-based shortest-path techniques.

## Project Information
- Course: Data Structure and Algorithms II
- Course Code: CCSE0301
- Program: B.Tech CSE-A
- Assignment: Individual
- Student: Adityaraj Singh
- Project: Public Transport Route Scheduling System
- SDGs: SDG 9 and SDG 11

## Problem
Public transport systems can suffer from inefficient route planning, delays,
longer passenger waiting times, traffic congestion, and poor vehicle utilization.

## Objectives
- Model transport networks using graphs.
- Apply shortest-path algorithms.
- Reduce route-selection cost.
- Demonstrate practical DSA concepts.
- Prepare the foundation for a route scheduling module.

## Current Implementation
The repository contains a clean Python prototype of Dijkstra's shortest-path
algorithm. It uses a weighted graph and returns both the route and total cost.

## Repository Structure
```text
public_transport_route_scheduling_system/
├── src/
│   ├── dijkstra.py
│   └── main.py
├── data/
│   └── sample_routes.csv
├── docs/
│   └── Descriptive_Project_Report.docx
├── requirements.txt
├── .gitignore
└── README.md
```

## Run
Python 3.10+ is recommended.

```bash
python src/main.py
```

No external Python packages are required.

## Example
The demo creates a small transport network and finds the lowest-cost route
from Central Station to Airport.

## Future Work
- Graph-based transport network input
- Route scheduling module
- Queue and priority-queue integration
- BFS/DFS comparison
- A* Search comparison
- Realistic transport datasets
- Testing and performance analysis
- Optional GUI/web interface

## Academic Note
This repository represents the project direction and the planned next-review
implementation. It should be extended with the student's own tested results,
datasets, screenshots, and analysis as development progresses.
