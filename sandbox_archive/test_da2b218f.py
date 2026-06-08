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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or n < d + 1:
            return None
        graph = [[0] * n for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if graph[u][v] == 0 and degree_counts[u] < d and degree_counts[v] < d:
                graph[u][v] = 1
                graph[v][u] = 1
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        
        for i in range(n):
            literals = [random.randint(0, 1) * 2 - 1 for _ in range(d)]
            clause = [literals[0]]
            for j in range(1, d):
                if graph[i][j]:
                    clause.append(literals[j])
                else:
                    clause.append(-literals[j])
            clauses.append(clause)
        
        return clauses
    
    def grothendieck_witt_group_size(graph):
        n = len(graph)
        k_theory_invariant = 0
        
        for i in range(n):
            degree = sum(graph[i])
            if degree % 2 == 1:
                k_theory_invariant += 1
        
        return k_theory_invariant
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        width = 0
        
        for clause in clauses:
            width = max(width, len(clause))
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        
        phi = tseitin_formula(graph)
        k_theory_invariant = grothendieck_witt_group_size(graph)
        proof_width = resolution_proof_width(phi)
        
        results.append({
            "n": n,
            "k_theory_invariant": k_theory_invariant,
            "proof_width": proof_width
        })
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    k_theory_values = [result["k_theory_invariant"] for result in results]
    proof_widths = [result["proof_width"] for result in results]
    
    mean_k_theory = sum(k_theory_values) / len(k_theory_values)
    mean_proof_width = sum(proof_widths) / len(proof_widths)
    
    covariance = sum((k_theory - mean_k_theory) * (width - mean_proof_width) for k_theory, width in zip(k_theory_values, proof_widths))
    variance_k_theory = sum((k_theory - mean_k_theory) ** 2 for k_theory in k_theory_values)
    variance_proof_width = sum((width - mean_proof_width) ** 2 for width in proof_widths)
    
    if variance_k_theory == 0 or variance_proof_width == 0:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_k_theory) * math.sqrt(variance_proof_width))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={first_failing_seed}")