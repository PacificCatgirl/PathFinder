import heapq
import time
from collections import deque
import wikipediaapi


def print_links(page):
    time.sleep(0.3)
    return list(page.links.values())


def create_graph(start_page, finish_page,  max_nodes):
    G = {}
    visited = set()
    queue = [start_page]

    while queue and len(visited) < max_nodes:
        current_page = queue.pop(0)
        current_title = current_page.title

        if current_title not in visited:
            visited.add(current_title)
            neighbors = print_links(current_page)


            G[current_title] = {}
            for neighbor in neighbors:
                neighbor_title = neighbor.title
                G[current_title][neighbor_title] = 1
                if neighbor_title not in G:
                    G[neighbor_title] = {}
                if neighbor_title == finish_page.title:
                    return G



            for neighbor in neighbors:
                if neighbor.title not in visited:
                    queue.append(neighbor)
    return G


def dijkstra(graph, start, finish):
    if start not in graph:
        print(f"Стартовый узел '{start}' отсутствует в графе")
        return None
    if finish not in graph:
        print(f"Целевой узел '{finish}' отсутствует в графе")
        return None

    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == finish:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            if neighbor not in graph:
                continue

            new_dist = current_distance + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (new_dist, neighbor))

    path = []
    current = finish
    while current is not None:
        path.append(current)
        current = previous_nodes.get(current)

    path.reverse()

    return path if path and path[0] == start else None