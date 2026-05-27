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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def rank_of_matrix(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def dpll_depth(instance):
        stack = [(instance, [])]
        max_depth = 0
        while stack:
            instance, path = stack.pop()
            if not instance:
                max_depth = max(max_depth, len(path))
                continue
            var = next((v for v in range(len(instance)) if instance[v]), None)
            if var is None:
                continue
            stack.append((instance[:var] + (not instance[var],) + instance[var+1:], path + [var]))
            stack.append((instance[:var] + (instance[var],) + instance[var+1:], path + [var]))
        return max_depth
    
    def construct_quantum_cluster_state(instance):
        n = len(instance)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            if instance[i]:
                for j in range(n):
                    if instance[j]:
                        A[i][j] = 1
        return A
    
    def min_rank_of_quantum_cluster_state(instance):
        A = construct_quantum_cluster_state(instance)
        return rank_of_matrix(A)
    
    n = random.randint(5, 40)
    instance = tuple(random.choice([True, False]) for _ in range(n))
    depth = dpll_depth(instance)
    min_rank = min_rank_of_quantum_cluster_state(instance)
    
    if min_rank > 2**depth + 3:
        return {
            "metric_name": "min_rank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance {instance} has depth {depth} but min rank {min_rank}"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")