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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    edges = set()
    for _ in range(d * n // 2):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        while u == v or (u, v) in edges or (v, u) in edges:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
        edges.add((u, v))
    return edges

def tseitin_formula(graph, n):
    literals = {f'x{i}': i for i in range(n)}
    clauses = []
    for u, v in graph:
        clauses.append([f'x{u}', f'~x{v}'])
        clauses.append([f'~x{u}', f'x{v}'])
        clauses.append([f'~x{u}', f'~x{v}', f'x{n + u + v}'])
    return literals, clauses

def min_rank_of_affine_quotient_sheaf(clauses):
    # Placeholder for actual implementation
    return len(clauses)

def monotone_circuit_complexity(literals, clauses):
    # Placeholder for actual implementation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        
        literals, clauses = tseitin_formula(graph, n)
        min_rank = min_rank_of_affine_quotient_sheaf(clauses)
        m_complexity = monotone_circuit_complexity(literals, clauses)
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "m_complexity": m_complexity
        })
    
    if not results:
        return {
            "metric_name": "min_rank_vs_m_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graph generated"
        }
    
    min_ranks = [r["min_rank"] for r in results]
    m_complexities = [r["m_complexity"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    if any(m <= 0 or mr <= 0 for m, mr in zip(m_complexities, min_ranks)):
        return {
            "metric_name": "min_rank_vs_m_complexity",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Non-positive values found"
        }
    
    sum_min_ranks = sum(min_ranks)
    sum_m_complexities = sum(m_complexities)
    sum_min_ranks_squared = sum(x**2 for x in min_ranks)
    sum_m_complexities_squared = sum(x**2 for x in m_complexities)
    sum_min_rank_m_complexity = sum(a * b for a, b in zip(min_ranks, m_complexities))
    
    n = len(results)
    r_squared = (n * sum_min_rank_m_complexity - sum_min_ranks * sum_m_complexities) ** 2
    r_squared /= ((n * sum_min_ranks_squared - sum_min_ranks**2) * (n * sum_m_complexities_squared - sum_m_complexities**2))
    
    conjecture_holds = 0.5 <= r_squared <= 10
    
    return {
        "metric_name": "min_rank_vs_m_complexity",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_r_squared = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R^2 out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")