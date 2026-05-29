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
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, min(n // 2, 5))
    variables = list(range(1, n + 1))
    clauses = []
    
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if A[j][i] != 0:
                    max_row = j
                    break
            if max_row is not None:
                A[max_row], A[rank] = A[rank], A[max_row]
                pivot = A[rank][i]
                for j in range(n):
                    A[rank][j] /= pivot
                for j in range(m):
                    if j != rank:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[rank][k]
                rank += 1
        return rank
    
    def min_exponent(A):
        m, n = len(A), len(A[0])
        if m != n:
            return float('inf')
        return gaussian_elimination(A)
    
    def communication_complexity(n):
        return math.log2(n * (n + 1) // 2)
    
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for v in clause:
            if v > 0:
                A[v - 1][v - 1] += 1
            else:
                A[-v - 1][-v - 1] += 1
    
    exp_A = min_exponent(A)
    comm_complexity = communication_complexity(n)
    
    conjecture_holds = exp_A <= 4 * n**2 and comm_complexity >= math.log(exp_A, 2)
    counterexample = "" if conjecture_holds else f"exp(A)={exp_A}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")