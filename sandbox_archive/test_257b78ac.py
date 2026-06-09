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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def incidence_complex(cnf):
        vertices = set()
        edges = []
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    edge = (clause[i], clause[j])
                    if edge not in edges and (-edge[0] not in vertices or -edge[1] not in vertices):
                        edges.append(edge)
                        vertices.add(-edge[0])
                        vertices.add(-edge[1])
        return vertices, edges
    
    def gromov_distortion(vertices, edges):
        n = len(vertices)
        if n <= 1:
            return 0
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, v in enumerate(sorted(vertices)):
            for j, u in enumerate(sorted(vertices)):
                if (v, u) in edges or (u, v) in edges:
                    adjacency_matrix[i][j] = 1
        # Compute the diameter of the graph
        max_distance = 0
        for i in range(n):
            for j in range(i + 1, n):
                distance = 0
                visited = [False] * n
                queue = [(i, 0)]
                while queue:
                    node, dist = queue.pop(0)
                    if node == j:
                        max_distance = max(max_distance, dist)
                        break
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in range(n):
                            if adjacency_matrix[node][neighbor] and not visited[neighbor]:
                                queue.append((neighbor, dist + 1))
        return math.log(max_distance) / math.log(n)
    
    def dpll_search_tree_height(cnf):
        n = len(cnf)
        clauses = [set(clause) for clause in cnf]
        variables = set()
        for clause in clauses:
            variables.update(clause)
        stack = [(clauses, variables)]
        height = 0
        while stack:
            clauses, variables = stack.pop()
            if not clauses:
                return height
            literal = next(iter(variables))
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    new_clauses.append(clause - {literal})
                elif -literal in clause:
                    new_clauses.append(clause - {-literal})
            stack.append((new_clauses, variables - {literal}))
            stack.append((new_clauses, variables - {-literal}))
            height += 1
        return height
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    vertices, edges = incidence_complex(cnf)
    distortion = gromov_distortion(vertices, edges)
    height = dpll_search_tree_height(cnf)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": distortion <= 2 * math.log(n) and 0.5 * math.log(n) <= height <= 1.5 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")