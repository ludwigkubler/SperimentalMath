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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    rank_matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    rank_matrix = gaussian_elimination(rank_matrix)
    
    rank = sum(1 for row in rank_matrix if any(row))
    return (2**n - rank) / (2**n - 1)

def eta_invariant(f):
    n = int(math.log2(len(f)))
    count = [0] * (2**(n+1))
    for i in range(2**n):
        count[sum(f[j] << j for j in range(n))] += 1
    return sum(count[i] * count[i+1] for i in range(2**n-1)) / len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    rank_variance_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        eta_values.append(eta_invariant(f))
        rank_variance_values.append(communication_complexity_rank_variance(f))
    
    if not eta_values or not rank_variance_values:
        return {
            "metric_name": "eta-invariant vs. communication complexity rank variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_metric"
        }
    
    n = len(eta_values)
    mean_eta = sum(eta_values) / n
    mean_variance = sum(rank_variance_values) / n
    
    covariance = sum((eta_values[i] - mean_eta) * (rank_variance_values[i] - mean_variance) for i in range(n)) / n
    variance_eta = sum((eta_values[i] - mean_eta)**2 for i in range(n)) / n
    variance_variance = sum((rank_variance_values[i] - mean_variance)**2 for i in range(n)) / n
    
    correlation_coefficient = covariance / math.sqrt(variance_eta * variance_variance)
    
    return {
        "metric_name": "eta-invariant vs. communication complexity rank variance",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + random.randint(1, 100) for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")