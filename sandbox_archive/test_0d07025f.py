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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == f[i]:
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            found = False
            for j in range(i, n):
                if sum(matrix[j]) > 0:
                    found = True
                    break
            if not found:
                continue
            pivot_row = [matrix[j][i] for j in range(i, n)]
            for j in range(n):
                if i != j:
                    factor = matrix[j][i] / pivot_row[i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * pivot_row[k]
            rank += 1
        return (n - rank) ** 2
    
    def formal_group_order(f):
        n = int(math.log2(len(f)))
        G = set()
        for i in range(2**n):
            if f[i] == 0:
                continue
            for j in range(i, 2**n):
                if f[j] == 1 and f[i ^ j] == 0:
                    G.add((i, j))
        return len(G)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            matrix = communication_matrix(f)
            variance = rank_variance(matrix)
            order = formal_group_order(f)
            results.append((order, variance))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders = [r[0] for r in results]
    variances = [r[1] for r in results]
    correlation = sum((orders[i] - sum(orders) / len(orders)) * (variances[i] - sum(variances) / len(variances)) for i in range(len(results))) / (len(results) * sum((orders[i] - sum(orders) / len(orders)) ** 2 for i in range(len(results))) ** 0.5 * sum((variances[i] - sum(variances) / len(variances)) ** 2 for i in range(len(results))) ** 0.5)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and all(abs(c) < 0.8 for c in results),
        "counterexample": "" if abs(correlation) >= 0.8 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < -0.8 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < -0.8)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_negative\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")