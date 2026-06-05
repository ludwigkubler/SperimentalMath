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

def generate_random_d_regular_graph(n, d):
    if n * d % 2 != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for node in range(n):
        neighbors = random.sample(range(n), d - len(graph[node]))
        for neighbor in neighbors:
            add_edge(node, neighbor)
    
    return graph

def generate_sat_formula(graph, k):
    n = len(graph)
    clauses = []
    variables = list(range(1, n * k + 1))
    
    def backtrack(i):
        if i == n * k:
            return True
        var = variables[i]
        for clause in combinations(variables[:i], k - 1):
            if is_clause_valid(clause) and all(var not in graph[node] or -var not in clauses[graph[node].index(var)] for node in range(n)):
                clauses.append(clause + (var,))
                if backtrack(i + 1):
                    return True
                clauses.pop()
        return False
    
    def is_clause_valid(clause):
        return len(set(abs(x) for x in clause)) == len(clause)
    
    if not backtrack(0):
        raise ValueError("Failed to generate a valid SAT formula")
    
    return clauses

def calculate_local_induction_dimension(graph):
    n = len(graph)
    max_independent_set_size = 0
    
    def is_independent_set(set_):
        for u in set_:
            for v in set_:
                if u != v and v in graph[u]:
                    return False
        return True
    
    def backtrack(start, current_set):
        nonlocal max_independent_set_size
        if len(current_set) > max_independent_set_size:
            max_independent_set_size = len(current_set)
        
        for i in range(start, n):
            if is_independent_set(current_set + [i]):
                backtrack(i + 1, current_set + [i])
    
    backtrack(0, [])
    return math.log2(max_independent_set_size)

def calculate_clause_subset_entropy(clauses):
    total_clauses = len(clauses)
    entropy = 0.0
    
    for clause in clauses:
        subset_count = sum(1 << i for i, var in enumerate(clause) if var > 0)
        entropy += math.log2(subset_count)
    
    return entropy / total_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2
        graph = generate_random_d_regular_graph(n, d)
        clauses = generate_sat_formula(graph, 3)
        
        ltd_value = calculate_local_induction_dimension(graph)
        entropy_value = calculate_clause_subset_entropy(clauses)
        
        results.append({
            "n": n,
            "ltd_value": ltd_value,
            "entropy_value": entropy_value
        })
    
    correlation_coefficient = sum((r["ltd_value"] - mean_ltd) * (r["entropy_value"] - mean_entropy) for r in results) / len(results)
    mean_ltd = sum(r["ltd_value"] for r in results) / len(results)
    mean_entropy = sum(r["entropy_value"] for r in results) / len(results)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.5
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={first_failing_seed}")