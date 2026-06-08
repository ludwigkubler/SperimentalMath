# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_algebraic_curve(f):
        n = int(math.log2(len(f)))
        curve = []
        for x in product(range(2), repeat=n):
            y = f[x[0]*2**(n-1) + sum(x[i]*2**(i-1) for i in range(1, n))]
            curve.append([x + (y,) if len(x) == n else None])
        return [point for point in curve if point is not None]
    
    def matrix_rank_variance(A):
        m = len(A)
        n = len(A[0]) if m > 0 else 0
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(m) if A[j][i] == 1), None)
            if pivot is not None:
                rank += 1
                for j in range(m):
                    if j != pivot:
                        factor = Fraction(A[j][i], A[pivot][i])
                        for k in range(n):
                            A[j][k] -= factor * A[pivot][k]
        return m - rank
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        protocol_matrix = []
        for x in product(range(2), repeat=n):
            y = f[x[0]*2**(n-1) + sum(x[i]*2**(i-1) for i in range(1, n))]
            for z in product(range(2), repeat=n):
                if z != x:
                    protocol_matrix.append([x, z, 1])
        return matrix_rank_variance(protocol_matrix)
    
    def min_rank(curve):
        A = []
        for point in curve:
            row = [point[i] for i in range(len(point)-1)]
            A.append(row)
        return matrix_rank_variance(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        curve = construct_algebraic_curve(f)
        rank_var = communication_complexity_rank_variance(f)
        min_r = min_rank(curve)
        results.append({"n": n, "rank_var": rank_var, "min_r": min_r})
    
    correlation_sum = 0
    for i in range(len(n_values)):
        for j in range(i+1, len(n_values)):
            correlation_sum += (results[i]["rank_var"] - results[j]["rank_var"]) * (results[i]["min_r"] - results[j]["min_r"])
    
    n_pairs = len(n_values) * (len(n_values) - 1) // 2
    mean_correlation = correlation_sum / n_pairs
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_correlation) >= 0.8 and all(abs(r["min_r"] - r["rank_var"]) <= 3 for r in results),
        "counterexample": "" if all(abs(r["min_r"] - r["rank_var"]) <= 3 for r in results) else "Rank difference exceeds 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank difference exceeds 3\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")