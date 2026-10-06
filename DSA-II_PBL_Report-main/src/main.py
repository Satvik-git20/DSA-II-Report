from dijkstra import dijkstra


def build_transport_graph():
    # Example route costs. These are sample values for demonstration only.
    return {
        "Central Station": [
            ("City Mall", 4),
            ("University", 6),
        ],
        "City Mall": [
            ("Central Station", 4),
            ("Bus Depot", 5),
            ("Market", 3),
        ],
        "University": [
            ("Central Station", 6),
            ("Market", 2),
            ("Airport", 9),
        ],
        "Bus Depot": [
            ("City Mall", 5),
            ("Airport", 7),
        ],
        "Market": [
            ("City Mall", 3),
            ("University", 2),
            ("Airport", 6),
        ],
        "Airport": [
            ("University", 9),
            ("Bus Depot", 7),
            ("Market", 6),
        ],
    }


if __name__ == "__main__":
    graph = build_transport_graph()
    source = "Central Station"
    destination = "Airport"

    cost, route = dijkstra(graph, source, destination)

    print("Public Transport Route Scheduling System")
    print("-" * 45)
    print(f"Source      : {source}")
    print(f"Destination : {destination}")

    if route:
        print("Best route  :", " -> ".join(route))
        print("Total cost  :", cost)
    else:
        print("No route found.")
