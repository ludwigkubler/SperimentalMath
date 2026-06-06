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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    def matrix_representation(vertices, edges):
        n = len(vertices)
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] = M[v][u] = 1
        return M
    
    def frobenius_quotient(M):
        n = len(M)
        det = determinant(M)
        if det == 0:
            return None
        trace = sum(M[i][i] for i in range(n))
        return Fraction(trace, n * det).limit_denominator()
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += sign * M[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def communication_complexity_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[j][i] != 0 for j in range(i, n)):
                rank += 1
        return rank
    
    def log2(x):
        if x <= 0:
            return None
        return Fraction(math.log2(x)).limit_denominator()
    
    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    n_max = 0
    
    for k in k_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            vertices, edges = generate_k_clique(n_max + 1, k)
            if vertices is None:
                continue
            M = matrix_representation(vertices, edges)
            fq = frobenius_quotient(M)
            if fq is not None:
                rank = communication_complexity_rank(M)
                if rank > 0:
                    results.append((log2(fq), log2(rank)))
    
    if len(results) < 30:
        return {
            "metric_name": "Frobenius Quotient vs Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few instances"
        }
    
    log_fq = [x[0] for x in results]
    log_rank = [x[1] for x in results]
    
    mean_log_fq = sum(log_fq) / len(log_fq)
    mean_log_rank = sum(log_rank) / len(log_rank)
    correlation = sum((log_fq[i] - mean_log_fq) * (log_rank[i] - mean_log_rank) for i in range(len(log_fq))) / len(log_fq)
    
    return {
        "metric_name": "Frobenius Quotient vs Communication Complexity Rank",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = (sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if x["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(x["conjecture_holds"] for x in results) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data")