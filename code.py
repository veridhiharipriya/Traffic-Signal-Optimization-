from dataclasses import dataclass
from collections import deque
import heapq

# =====================================
# AI TRAFFIC SIGNAL OPTIMIZATION SYSTEM
# =====================================

@dataclass
class Road:
    name: str
    vehicles: int


roads = {
    "North": Road("North", 0),
    "South": Road("South", 0),
    "East": Road("East", 0),
    "West": Road("West", 0)
}

# =====================================
# CO1 - Knowledge Representation
# =====================================

traffic_graph = {
    "Junction": ["North", "South", "East", "West"],
    "North": ["Junction"],
    "South": ["Junction"],
    "East": ["Junction"],
    "West": ["Junction"]
}

weighted_graph = {
    "Junction": [("North", 3), ("South", 2),
                 ("East", 4), ("West", 5)],
    "North": [("Junction", 3)],
    "South": [("Junction", 2)],
    "East": [("Junction", 4)],
    "West": [("Junction", 5)]
}

heuristic = {
    "Junction": 4,
    "North": 0,
    "South": 1,
    "East": 2,
    "West": 3
}

# =====================================
# CO2 - BFS
# =====================================

def bfs(start, goal):

    queue = deque([[start]])
    visited = set()

    while queue:

        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:

            visited.add(node)

            for neighbor in traffic_graph[node]:
                queue.append(path + [neighbor])

    return None

# =====================================
# CO2 - DFS
# =====================================

def dfs(node, goal, visited=None, path=None):

    if visited is None:
        visited = set()

    if path is None:
        path = []

    visited.add(node)
    path.append(node)

    if node == goal:
        return path

    for neighbor in traffic_graph[node]:

        if neighbor not in visited:

            result = dfs(
                neighbor,
                goal,
                visited,
                path.copy()
            )

            if result:
                return result

    return None

# =====================================
# CO2 - UCS
# =====================================

def ucs(start, goal):

    pq = [(0, start, [start])]
    visited = set()

    while pq:

        cost, node, path = heapq.heappop(pq)

        if node == goal:
            return cost, path

        if node not in visited:

            visited.add(node)

            for neighbor, weight in weighted_graph[node]:

                heapq.heappush(
                    pq,
                    (
                        cost + weight,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None

# =====================================
# CO2 - A*
# =====================================

def astar(start, goal):

    pq = [(0, start, [start])]
    visited = set()

    while pq:

        f, node, path = heapq.heappop(pq)

        if node == goal:
            return path

        if node not in visited:

            visited.add(node)

            for neighbor, weight in weighted_graph[node]:

                g = len(path)
                h = heuristic[neighbor]

                heapq.heappush(
                    pq,
                    (
                        g + h + weight,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None

# =====================================
# CO3 - CSP SIGNAL ALLOCATION
# =====================================

def signal_scheduler():

    max_vehicles = -1
    selected_road = None

    for road in roads.values():

        if road.vehicles > max_vehicles:

            max_vehicles = road.vehicles
            selected_road = road.name

    return selected_road

# =====================================
# CO3 - Explain Constraint Failure
# =====================================

def explain_constraint():

    busy = []

    for road in roads.values():

        if road.vehicles > 30:
            busy.append(road.name)

    if len(busy) > 1:

        print("\nConstraint Notice:")
        print("Multiple roads have heavy traffic.")
        print("Cannot give green signal to all roads simultaneously.")
        print("Priority given to highest congestion road.")

# =====================================
# CO4 - Utility Function
# =====================================

def utility(vehicles):

    return vehicles * 10

# =====================================
# CO4 - Minimax
# =====================================

def minimax(depth, maximizing):

    if depth == 0:
        return 10

    if maximizing:

        return max(
            minimax(depth - 1, False),
            minimax(depth - 1, False)
        )

    return min(
        minimax(depth - 1, True),
        minimax(depth - 1, True)
    )

# =====================================
# CO5 - Bayesian Congestion Prediction
# =====================================

def congestion_probability(vehicle_count):

    if vehicle_count > 40:
        prior = 0.8

    elif vehicle_count > 20:
        prior = 0.6

    else:
        prior = 0.3

    likelihood = 0.7
    evidence = 0.5

    probability = (
        likelihood * prior
    ) / evidence

    return round(probability, 2)

# =====================================
# CO5 - Expected Utility
# =====================================

def expected_utility(prob):

    benefit = 100

    return round(
        prob * benefit,
        2
    )

# =====================================
# INPUT TRAFFIC
# =====================================

def enter_traffic():

    print("\nEnter Vehicle Counts")

    for road in roads:

        count = int(
            input(
                f"{road}: "
            )
        )

        roads[road].vehicles = count

    print("\nTraffic Updated Successfully")

# =====================================
# TRAFFIC REPORT
# =====================================

def traffic_report():

    print("\n===== TRAFFIC REPORT =====")

    for road in roads.values():

        if road.vehicles > 40:
            status = "High"

        elif road.vehicles > 20:
            status = "Medium"

        else:
            status = "Low"

        print(
            road.name,
            "->",
            road.vehicles,
            "vehicles",
            "|",
            status,
            "Congestion"
        )

# =====================================
# SIGNAL OPTIMIZATION
# =====================================

def optimize_signal():

    road = signal_scheduler()

    vehicles = roads[road].vehicles

    if vehicles > 40:
        duration = 60

    elif vehicles > 20:
        duration = 40

    else:
        duration = 20

    print("\n===== AI SIGNAL DECISION =====")
    print("Green Signal:", road)
    print("Duration:", duration, "seconds")

    explain_constraint()

# =====================================
# EMERGENCY VEHICLE PRIORITY
# =====================================

def emergency_vehicle():

    road = input(
        "Emergency Vehicle Road: "
    )

    print("\nEMERGENCY MODE ACTIVATED")
    print("Green Signal Assigned To:", road)
    print("Other Roads Temporarily Blocked")

# =====================================
# FULL AI WORKFLOW
# =====================================

def full_ai_workflow():

    print("\n===== AI REASONING TRACE =====")

    traffic_report()

    selected = signal_scheduler()

    print(
        "\nSelected Road:",
        selected
    )

    prob = congestion_probability(
        roads[selected].vehicles
    )

    print(
        "Congestion Probability:",
        prob
    )

    score = minimax(
        3,
        True
    )

    print(
        "Decision Score:",
        score
    )

    eu = expected_utility(prob)

    print(
        "Expected Utility:",
        eu
    )

    optimize_signal()

# =====================================
# MAIN MENU
# =====================================

while True:

    print("\n")
    print("===== TRAFFIC SIGNAL OPTIMIZATION =====")
    print("1. Enter Traffic Data")
    print("2. Traffic Report")
    print("3. BFS Route")
    print("4. DFS Route")
    print("5. UCS Route")
    print("6. A* Route")
    print("7. Optimize Signal")
    print("8. Emergency Vehicle")
    print("9. Congestion Prediction")
    print("10. Full AI Workflow")
    print("11. Exit")

    choice = input(
        "Enter Choice: "
    )

    if choice == "1":

        enter_traffic()

    elif choice == "2":

        traffic_report()

    elif choice == "3":

        print(
            bfs(
                "Junction",
                "North"
            )
        )

    elif choice == "4":

        print(
            dfs(
                "Junction",
                "North"
            )
        )

    elif choice == "5":

        print(
            ucs(
                "Junction",
                "North"
            )
        )

    elif choice == "6":

        print(
            astar(
                "Junction",
                "North"
            )
        )

    elif choice == "7":

        optimize_signal()

    elif choice == "8":

        emergency_vehicle()

    elif choice == "9":

        count = int(
            input(
                "Vehicle Count: "
            )
        )

        print(
            "Congestion Probability:",
            congestion_probability(count)
        )

    elif choice == "10":

        full_ai_workflow()

    elif choice == "11":

        print("Thank You")
        break

    else:

        print("Invalid Choice")