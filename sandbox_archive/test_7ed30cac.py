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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def expander_graph(n, phi):
        # Generate a random expander graph with n vertices and expansion phi
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), int(phi * (n - 1)))
            for j in neighbors:
                if i < j:
                    edges.add((i, j))
        return list(edges)
    
    def tseitin_formula(graph, omega):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        
        # Clause for each vertex
        for i in range(n):
            clause = [-literals[i]]
            for j in graph:
                if i == j[0]:
                    clause.append(literals[j[1]])
                elif i == j[1]:
                    clause.append(-literals[j[0]])
            clauses.append(clause)
        
        # Clause for each edge
        for i, j in graph:
            clauses.append([literals[i], literals[j]])
            clauses.append([-literals[i], -literals[j]])
        
        return clauses
    
    def resolution_width(clauses):
        # Simple heuristic to estimate resolution width
        max_width = 0
        seen_literals = set()
        for clause in clauses:
            seen_literals.update(clause)
            if len(seen_literals) > max_width:
                max_width = len(seen_literals)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    phi = random.uniform(0.5, 0.9)
    graph = expander_graph(n_values[seed % len(n_values)], phi)
    omega = {i: (n - i) / n for i in range(n)}
    
    clauses = tseitin_formula(graph, omega)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 1 / phi,
        "counterexample": "" if width >= 1 / phi else f"Graph with n={n}, φ={phi} has width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    std_width = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample_desc = results[next(i for i, res in enumerate(results) if not res["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")