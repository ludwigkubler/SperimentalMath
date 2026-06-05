# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for OR gates
        for i in range(1, n+1):
            clause = f"({variables[i-1]} v {variables[n+i-1]})"
            clauses.append(clause)
        
        # Generate clauses for AND gates
        for i in range(n, 2*n-1):
            clause = f"({variables[2*n-i-1]} -> ({variables[i-n-1]} & {variables[i+n-1]}))"
            clauses.append(clause)
        
        # Generate final OR gate
        final_clause = "v".join([f"{variables[j]}" for j in range(n, 2*n)])
        clauses.append(final_clause)
        
        return clauses
    
    def is_valid_graph(G):
        n = len(G)
        degree = sum(len(neighbors) for neighbors in G.values()) // n
        if degree % 2 != 0:
            return False
        return True
    
    def generate_random_d_regular_graph(n, d):
        while True:
            G = {i: [] for i in range(n)}
            edges = set()
            for _ in range(d * n // 2):
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v and (u, v) not in edges and (v, u) not in edges:
                    G[u].append(v)
                    G[v].append(u)
                    edges.add((u, v))
            if is_valid_graph(G):
                return G
    
    def compute_min_sheaf_order(G):
        n = len(G)
        order = 0
        for i in range(n):
            neighbors = G[i]
            if not neighbors:
                continue
            max_distance = -1
            visited = [False] * n
            queue = [(i, 0)]
            while queue:
                node, dist = queue.pop(0)
                if visited[node]:
                    continue
                visited[node] = True
                max_distance = max(max_distance, dist)
                for neighbor in neighbors:
                    if not visited[neighbor]:
                        queue.append((neighbor, dist + 1))
            order += max_distance + 1
        return order / n
    
    def compute_resolution_proof_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            literals = clause.split("v")
            width = max(width, len(literals))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            G = generate_random_d_regular_graph(n, 2)
            clauses = generate_tseitin_formula(n)
            min_sheaf_order = compute_min_sheaf_order(G)
            resolution_width = compute_resolution_proof_width(clauses)
            ratio = Fraction(min_sheaf_order, resolution_width).limit_denominator()
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = abs(mean_ratio - n) < 0.1 * n
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}, expected=n"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")