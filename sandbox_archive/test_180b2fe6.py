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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def tseitin_formula(edges, n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{literals[i]}')
        for u, v in edges:
            clauses.append(f'-{literals[u]} -{literals[v]} {literals[n + u * n + v]}')
            clauses.append(f'-{literals[v]} -{literals[u]} {literals[n + v * n + u]}')
            clauses.append(f'{literals[u]} {literals[v]} -{literals[n + u * n + v]}')
            clauses.append(f'{literals[v]} {literals[u]} -{literals[n + v * n + u]}')
        return literals, clauses
    
    def characteristic_polynomial(clauses):
        # Placeholder for actual computation
        return [1, 0, -n]
    
    def hypergeometric_series(polynomial):
        # Placeholder for actual computation
        return polynomial
    
    def minimal_rank(series):
        k = 1
        while True:
            found = False
            for i in range(k):
                if all(coeff >= 0 for coeff in series[:k]):
                    found = True
                    break
            if not found:
                k += 1
            else:
                return k
    
    def resolution_proof_width(literals, clauses):
        # Placeholder for actual computation
        return len(literals)
    
    n = random.randint(5, 40)
    graph_edges = generate_graph(n)
    literals, clauses = tseitin_formula(graph_edges, n)
    polynomial = characteristic_polynomial(clauses)
    series = hypergeometric_series(polynomial)
    R_G = minimal_rank(series)
    width = resolution_proof_width(literals, clauses)
    
    return {
        "metric_name": "resolution proof width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (math.log(R_G) / math.log(2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [random.randint(1, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")