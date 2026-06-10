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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        inputs = [(i, j) for i in range(n) for j in range(n)]
        ranks = set()
        for i, j in inputs:
            rank = sum(f[i] ^ f[j])
            ranks.add(rank)
        return max(ranks) - min(ranks)
    
    def p_adic_derivative_rank(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = f[i]
            A[n][i] = 1
        B = [0] * (n + 1)
        B[n] = 1
        
        # Gaussian elimination to find the rank of A
        def gaussian_elimination(A, B):
            n = len(A)
            for i in range(n):
                if A[i][i] == 0:
                    for j in range(i + 1, n):
                        if A[j][i] != 0:
                            A[i], A[j] = A[j], A[i]
                            B[i], B[j] = B[j], B[i]
                            break
                if A[i][i] == 0:
                    return None  # Singular matrix
                for j in range(i + 1, n):
                    factor = -A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] += factor * A[i][k]
                    B[j] += factor * B[i]
            return sum(1 for row in A if any(row))
        
        rank_A = gaussian_elimination(A, B)
        if rank_A is None:
            return None
        return n - rank_A
    
    def pearson_correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mdr_values = []
    delta_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        delta = communication_complexity_rank_variance(f)
        mdr = p_adic_derivative_rank(f)
        
        if mdr is None or delta <= 0:
            return {
                "metric_name": "mdr_vs_delta",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mdr_values.append(mdr)
        delta_values.append(delta)
    
    correlation = pearson_correlation_coefficient(mdr_values, delta_values)
    conjecture_holds = all(0.6 <= r <= 1.2 for r in mdr_values) and correlation >= 0.8
    
    return {
        "metric_name": "mdr_vs_delta",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation < 0.8 or mdr > 1.2 * delta"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8 or mdr > 1.2 * delta\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some seeds produced None for correlation")