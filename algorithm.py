import heapq
import time
from collections import deque
import wikipediaapi


def print_links(page):
    return list(page.links.values())


def create_graph(start_page, finish_page, max_nodes):
    G = {}
    visited = set()
    queue = deque([start_page])

    while queue and len(visited) < max_nodes:
        current_page = queue.popleft()
        current_title = current_page.title

        if current_title not in visited:
            visited.add(current_title)
            neighbors = print_links(current_page)


            G[current_title] = []

            for neighbor in neighbors:
                neighbor_title = neighbor.title
                G[current_title].append(neighbor_title)

                if neighbor_title not in G:
                    G[neighbor_title] = []

                if neighbor_title == finish_page.title:
                    return G

            for neighbor in neighbors:
                if neighbor.title not in visited:
                    queue.append(neighbor)

    return G


def bfs_shortest_path(graph, start, finish):
    if start not in graph:
        print(f"Стартовый узел '{start}' отсутствует в графе")
        return None
    if finish not in graph:
        print(f"Целевой узел '{finish}' отсутствует в графе")
        return None

    queue = deque()
    queue.append([start])

    visited = set()
    visited.add(start)

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == finish:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None
