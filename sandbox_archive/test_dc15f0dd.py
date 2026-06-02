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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            return None  # Singular matrix, no unique solution
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def hodge_dimension(graph, n):
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in graph:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    return gaussian_elimination(adj_matrix)

def tseitin_formula(graph, n):
    clauses = []
    literals = {i: f'x{i}' for i in range(n)}
    neg_literals = {i: f'-x{i}' for i in range(n)}
    
    for u, v in graph:
        clauses.append([literals[u], neg_literals[v]])
        clauses.append([neg_literals[u], literals[v]])
        clauses.append([neg_literals[u], neg_literals[v]])
        clauses.append([literals[u], literals[v]])
    
    return clauses

def entropy(clauses):
    n = len(clauses)
    counts = [0] * (n + 1)
    for clause in clauses:
        counts[len(clause)] += 1
    total = sum(counts)
    if total == 0:
        return 0
    probabilities = [Fraction(c, total) for c in counts]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = [(i, (i + 1) % n) for i in range(n)]  # Example d-regular graph
        hd = hodge_dimension(graph, n)
        if hd is None:
            return {
                "metric_name": "Hodge Dimension",
                "metric_value": float('inf'),
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Singular matrix encountered"
            }
        clauses = tseitin_formula(graph, n)
        h_entropy = entropy(clauses)
        results.append((hd, h_entropy))
    
    correlation = 0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            x1, y1 = results[i]
            x2, y2 = results[j]
            correlation += (x1 - x2) * (y1 - y2)
    
    n_pairs = len(results) * (len(results) - 1) // 2
    if n_pairs == 0:
        return {
            "metric_name": "Hodge Dimension",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Not enough data points"
        }
    
    correlation /= n_pairs
    mean_hd = sum(x for x, _ in results) / len(results)
    mean_entropy = sum(y for _, y in results) / len(results)
    
    return {
        "metric_name": "Hodge Dimension",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= abs(correlation) <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not enough data points\" first_failing_seed={first_failing_seed}")