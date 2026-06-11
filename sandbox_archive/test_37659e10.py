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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graphical_matroid(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def automorphism_group_order(edges):
        n = len(set(u for u, v in edges) | set(v for u, v in edges))
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = -1
                for j in range(rank, rows):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for j in range(rows):
                    if j != rank - 1:
                        factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
            return rank
        
        return n ** (n - gaussian_elimination(adj_matrix))
    
    def resolution_proof_width(edges, n):
        if not edges:
            return 0
        max_clause_length = max(len(u) + len(v) for u, v in edges)
        return max_clause_length
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        matroid = generate_graphical_matroid(n)
        ord_aut_M = automorphism_group_order(matroid)
        w_M = resolution_proof_width(matroid, n)
        results.append((n, ord_aut_M, w_M))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, ord_aut_M_values, w_M_values = zip(*results)
    mean_ord_aut_M = sum(ord_aut_M_values) / len(ord_aut_M_values)
    mean_w_M = sum(w_M_values) / len(w_M_values)
    
    if len(n_values) < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    covariance = sum((ord_aut_M - mean_ord_aut_M) * (w_M - mean_w_M) for ord_aut_M, w_M in zip(ord_aut_M_values, w_M_values))
    variance_ord_aut_M = sum((ord_aut_M - mean_ord_aut_M) ** 2 for ord_aut_M in ord_aut_M_values)
    variance_w_M = sum((w_M - mean_w_M) ** 2 for w_M in w_M_values)
    
    if variance_ord_aut_M == 0 or variance_w_M == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    pearsons_correlation_coefficient = covariance / (math.sqrt(variance_ord_aut_M) * math.sqrt(variance_w_M))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": pearsons_correlation_coefficient >= 0.7,
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
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")