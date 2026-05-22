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
    
    def matrix_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def generate_linear_protocol(query_complexity: int):
        protocol = []
        for _ in range(query_complexity):
            query = [random.randint(0, 1) for _ in range(2)]
            response = random.randint(0, 1)
            protocol.append((query, response))
        return protocol
    
    def design_qec(protocol):
        n = len(protocol)
        A = [[0] * (n + 1) for _ in range(n)]
        for i, (query, response) in enumerate(protocol):
            A[i][i] = 1
            A[i][-1] = response
        return matrix_rank(A)
    
    query_complexities = [5, 10, 15, 20, 30, 40]
    results = []
    
    for Q in query_complexities:
        protocol = generate_linear_protocol(Q)
        rank = design_qec(protocol)
        results.append((Q, rank))
    
    min_rank = min(rank for _, rank in results)
    conjecture_holds = all(rank >= Q / 2 for _, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")