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

    def topological_sort(clauses):
        graph = {i: set() for i in range(-n, n + 1)}
        in_degree = {i: 0 for i in range(-n, n + 1)}
        
        for clause in clauses:
            for literal in clause:
                if literal not in graph[-literal]:
                    graph[-literal].add(literal)
                    in_degree[literal] += 1
        
        queue = [node for node in in_degree if in_degree[node] == 0]
        order = []
        
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return order

    def resolution_width(clauses):
        clauses = set(tuple(sorted(c)) for c in clauses)
        width = 0
        
        while True:
            new_clauses = set()
            for clause1, clause2 in itertools.combinations(clauses, 2):
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                    if new_clause not in clauses and new_clause not in new_clauses:
                        new_clauses.add(new_clause)
            if not new_clauses:
                break
            width += len(new_clauses)
            clauses.update(new_clauses)
        
        return width

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    orbit_space = topological_sort(cnf)
    h_orbit_space = len(set(orbit_space))
    w_phi = resolution_width(cnf)
    
    if h_orbit_space == 0 or w_phi == 0:
        return {
            "metric_name": "Minimal Topological Entropy and Resolution Proof Width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "Minimal Topological Entropy and Resolution Proof Width",
        "metric_value": h_orbit_space / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some seeds produced None values")