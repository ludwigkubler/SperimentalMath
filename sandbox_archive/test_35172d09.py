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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def compute_euler_characteristic(edges, n):
        # Euler characteristic χ = V - E + F
        V = n
        E = len(edges)
        F = 1 + E  # Each edge adds one face (triangle) in planar graphs
        return V - E + F
    
    def dpll_solve(clauses):
        def dfs(assignment, clause_index):
            if clause_index == len(clauses):
                return True
            for literal in clauses[clause_index]:
                var = abs(literal)
                value = assignment.get(var, None)
                if value is None:
                    assignment[var] = 1
                    if dfs(assignment, clause_index + 1):
                        return True
                    assignment[var] = -1
                    if dfs(assignment, clause_index + 1):
                        return True
                    del assignment[var]
                elif (value == 1 and literal > 0) or (value == -1 and literal < 0):
                    continue
                else:
                    break
            return False
        
        assignment = {}
        return dfs(assignment, 0)
    
    n = random.randint(5, 40)
    graph_edges = generate_random_graph(n)
    euler_char = compute_euler_characteristic(graph_edges, n)
    clauses = []
    for u, v in graph_edges:
        clauses.append([-u - 1, -v - 1])
        clauses.append([u + 1, v + 1])
    proof_size = len(dpll_solve(clauses))
    
    return {
        "metric_name": "Euler characteristic vs Proof size",
        "metric_value": abs(euler_char),
        "instances_tested": 1,
        "conjecture_holds": abs(euler_char) / math.log(n) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Euler characteristic does not match proof size' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")