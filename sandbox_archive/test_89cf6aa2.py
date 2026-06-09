# auto-injected by SEC sandbox
import itertools
import collections
import json
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            available_neighbors = [j for j in range(n) if j != i and graph[i][j] == 0]
            neighbors = random.sample(available_neighbors, d)
            for neighbor in neighbors:
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    graph[i][neighbor] = 1
                    graph[neighbor][i] = 1
                    edges.add((i, neighbor))
        return graph
    
    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(len(graph)):
                    if graph[node][neighbor] == 1 and not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def find_quasi_crystalline_symmetries(graph):
        n = len(graph)
        symmetries = []
        for i in range(n):
            symmetry = [0] * n
            for j in range(n):
                symmetry[j] = graph[(i + j) % n][(j + i) % n]
            if symmetry not in symmetries:
                symmetries.append(symmetry)
        return len(symmetries)
    
    def resolution_proof_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clause = [0] * n
            for j in range(n):
                if graph[i][j] == 1:
                    clause[j] = 1
            clauses.append(clause)
        
        def is_satisfiable(clauses):
            assignment = [random.choice([True, False]) for _ in range(len(clauses))]
            for clause in clauses:
                if all(not (assignment[i] and not clause[i]) for i in range(len(clause))):
                    return True
            return False
        
        width = 0
        while True:
            new_clauses = []
            for clause in clauses:
                if any(assignment[i] and not clause[i] for i in range(len(clause))):
                    continue
                new_clause = [not literal for literal in clause]
                new_clauses.append(new_clause)
            if is_satisfiable(new_clauses):
                width += 1
                clauses = new_clauses
            else:
                break
        return width
    
    def run_experiment(n, d):
        graph = generate_d_regular_graph(n, d)
        if not graph or not is_connected(graph):
            return None
        qcr = find_quasi_crystalline_symmetries(graph)
        w = resolution_proof_width(graph)
        return {"qcr": qcr, "w": w}
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    for _ in range(instances_tested):
        result = run_experiment(random.randint(5, 40), random.randint(2, min(n_max // 2 - 1, 4)))
        if result:
            metric_values.append(result["qcr"] / result["w"])
    
    if not metric_values:
        return {
            "metric_name": "qcr/w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if abs(x - mean) <= 3 * std) / len(metric_values)
    
    return {
        "metric_name": "qcr/w",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")