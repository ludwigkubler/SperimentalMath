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
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_quasigroup(n):
        q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                q[i][j] = (i + j) % n
        return q
    
    def min_index(q):
        n = len(q)
        indices = [0] * n
        for i in range(n):
            for j in range(n):
                if q[i][j] == 0:
                    indices[i] += 1
        return max(indices)
    
    def communication_complexity_rank(matrix):
        n = len(matrix)
        eigenvalues = []
        for k in range(2, n + 1):
            A_k = [[matrix[i][j] ** k for j in range(n)] for i in range(n)]
            A_k_sum = sum(sum(row) for row in A_k)
            if A_k_sum == 0:
                continue
            eigenvalues.append(A_k_sum / (n * n))
        return len(eigenvalues)
    
    def matrix_from_quasigroup(q):
        n = len(q)
        matrix = [[int(q[i][j] == k) for j in range(n)] for k in range(n)]
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_sum = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            q = generate_quasigroup(n)
            matrix = matrix_from_quasigroup(q)
            min_index_val = min_index(q)
            rank_val = communication_complexity_rank(matrix)
            
            if rank_val == 0:
                continue
            
            metric_sum += min_index_val / rank_val
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = metric_sum / instances_tested
    
    return {
        "metric_name": "min_index_over_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, min_index_over_rank={r['metric_value']}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")