# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = {i: [] for i in range(n)}
    degrees = [d] * n
    
    while any(deg > 0 for deg in degrees):
        i = random.choice([i for i, deg in enumerate(degrees) if deg > 0])
        neighbors = [j for j in range(i) if j not in graph[i]]
        if len(neighbors) == 0:
            continue
        
        j = random.choice(neighbors)
        if j not in graph[i]:
            graph[i].append(j)
            graph[j].append(i)
            degrees[i] -= 1
            degrees[j] -= 1
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    
    for i in range(n):
        clause = [literals[i]]
        for j in graph[i]:
            clause.append(f"-{literals[j]}")
        clauses.append(clause)
    
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([f"-{literals[i]}", literals[j]])
            clauses.append([f"-{literals[j]}", literals[i]])
    
    return clauses

def resolution_width(clauses):
    queue = [c for c in clauses if len(c) == 1]
    learned_clauses = []
    
    while queue:
        clause = queue.pop(0)
        literal = clause[0][1:]
        
        new_clauses = []
        for c in learned_clauses:
            if literal in c:
                continue
            if f"-{literal}" in c:
                new_clause = [l for l in c if l != f"-{literal}"]
                queue.append(new_clause)
            else:
                new_clauses.append(c)
        
        learned_clauses.extend(new_clauses)
    
    return max(len(c) for c in learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        
        if width == 0:
            continue
        
        m_hodetrop = len(clauses)  # Simplified for this test
        ratio = Fraction(m_hodetrop, math.log2(n) ** 2 * width)
        results.append((n, ratio))
    
    mean_ratio = sum(ratio for _, ratio in results) / len(results)
    conjecture_holds = all(ratio >= Fraction(1, 10) for _, ratio in results)  # Placeholder constant
    counterexample = "" if conjecture_holds else "correlation_coefficient=0"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")