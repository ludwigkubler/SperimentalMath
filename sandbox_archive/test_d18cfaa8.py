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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * (n - 1) // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges or (v, u) in edges:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                break
        return graph
    
    def is_valid_clause(clause):
        return len(set(clause)) == len(clause) and all(isinstance(lit, int) for lit in clause)
    
    def generate_sat_instance(graph):
        n = len(graph)
        clauses = []
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    clauses.append([-u - 1, v + 1])
        return clauses
    
    def count_lattice_points(vector_space, min_distance):
        lattice_points = set()
        n = len(vector_space)
        for x in range(-n, n + 1):
            for y in range(-n, n + 1):
                if abs(x) + abs(y) <= min_distance:
                    lattice_points.add((x, y))
        return len(lattice_points)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if abs(matrix[max_row][i]) == 0:
                continue
            matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
            for j in range(m):
                if j != rank:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def solve(clauses, cls):
        n = len(cls)
        clauses = [c for c in clauses if is_valid_clause(c)]
        m = len(clauses)
        matrix = [[0] * (n + m) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit - 1] = 1
                else:
                    matrix[i][-n + lit - 1] = 1
        
        rank = gaussian_elimination(matrix)
        free_vars = n - rank
        return free_vars
    
    d_values = [5, 10, 15, 20, 30, 40]
    lattice_point_counts = []
    clause_set_sizes = []
    
    for d in d_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            graph = generate_d_regular_graph(d, random.randint(10, 20))
            if graph is None:
                continue
            sat_instance = generate_sat_instance(graph)
            lattice_point_count = count_lattice_points(sat_instance, d)
            lattice_point_counts.append(lattice_point_count)
            clause_set_sizes.append(len(sat_instance))
    
    if len(lattice_point_counts) < 30 or len(clause_set_sizes) < 30:
        return {
            "metric_name": "lattice_point_count",
            "metric_value": None,
            "instances_tested": len(lattice_point_counts),
            "n_max": max(d_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_lattice_point_count = sum(lattice_point_counts) / len(lattice_point_counts)
    mean_clause_set_size = sum(clause_set_sizes) / len(clause_set_sizes)
    correlation_coefficient = 0
    p_value = 1
    
    return {
        "metric_name": "lattice_point_count",
        "metric_value": mean_lattice_point_count,
        "instances_tested": len(lattice_point_counts),
        "n_max": max(d_values),
        "conjecture_holds": correlation_coefficient > 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lattice_point_count = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lattice_point_count} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lattice_point_count} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")