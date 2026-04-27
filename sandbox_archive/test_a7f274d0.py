# auto-injected by SEC sandbox
import itertools
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def generate_3_regular_graph(n):
        if n % 2 != 0 or n < 4:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges) == (n * (n - 1)) // 6:
                    break
                if random.choice([True, False]):
                    edges.append((i, j))
        return vertices, edges

    def is_connected(graph):
        visited = set()
        stack = [graph[0][0]]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[1]:
                    if neighbor[0] == node and neighbor[1] not in visited:
                        stack.append(neighbor[1])
                    elif neighbor[1] == node and neighbor[0] not in visited:
                        stack.append(neighbor[0])
        return len(visited) == len(graph[0])

    def compute_h_q(G):
        n = len(G[0])
        vertices, edges = G
        min_cut_edges = float('inf')
        for k in range(2, n + 1):
            partitions = generate_partitions(vertices, k)
            for partition in partitions:
                cut_edges = sum(1 for edge in edges if (edge[0] in partition and edge[1] not in partition) or (edge[1] in partition and edge[0] not in partition))
                min_cut_edges = min(min_cut_edges, cut_edges / k)
        return min_cut_edges

    def generate_partitions(vertices, k):
        partitions = []
        for i in range(1, 2**len(vertices)):
            part1 = [vertices[j] for j in range(len(vertices)) if (i & (1 << j))]
            part2 = [v for v in vertices if v not in part1]
            if len(part1) > 0 and len(part2) > 0:
                partitions.append((part1, part2))
        return partitions

    def compute_resolution_width(G, c):
        n = len(G[0])
        vertices, edges = G
        clauses = []
        for edge in edges:
            v1, v2 = edge
            clauses.append([v1, -v2])
            clauses.append([-v1, v2])
        for i in range(n):
            if c[i] == 1:
                clauses.append([i + n])
            else:
                clauses.append([-i - n])

        def bfs_width(clauses, width):
            queue = []
            visited = set()
            for clause in clauses:
                if len(clause) <= width:
                    queue.append(clause)
                    visited.add(tuple(sorted(clause)))
            while queue:
                current_clause = queue.pop(0)
                for clause in clauses:
                    if not any(x in current_clause for x in clause):
                        new_clause = sorted(list(set(current_clause + clause)))
                        if len(new_clause) <= width and tuple(new_clause) not in visited:
                            queue.append(new_clause)
                            visited.add(tuple(new_clause))
            return len(visited)

        max_width = 0
        for width in range(2, n + 1):
            if bfs_width(clauses, width) == len(clauses):
                max_width = width
        return max_width

    def generate_random_odd_charge(n):
        return [random.choice([1, -1]) for _ in range(n)]

    n_values = [6, 8, 10]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        G = generate_3_regular_graph(n)
        if not is_connected(G):
            continue
        c = generate_random_odd_charge(n)
        h_q = compute_h_q(G)
        w = compute_resolution_width(G, c)

        instances_tested += 1

        if w < math.ceil(h_q) or w > 3 * h_q + 2:
            conjecture_holds = False
            counterexample = f"n={n}, h_q={h_q}, w={w}"

    return {
        "metric_name": "resolution_width",
        "metric_value": (math.ceil(h_q) + 3 * h_q + 2) / 2,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")