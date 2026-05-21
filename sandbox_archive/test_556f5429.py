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
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def real_rank(A):
        rank = 0
        m, n = len(A), len(A[0])
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2*n):
            clause = random.sample(range(n), 3)
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses, n):
        m = len(clauses)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                A[i][var] = 1
                A[i][-1] += 1
        return A
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    A = clause_indicator_polynomial(clauses, n)
    
    rank = real_rank(A)
    expected_rank = math.log2(n) if n > 1 else 0
    
    metric_name = "real_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = abs(rank - expected_rank) < 1e-5
    counterexample = "" if conjecture_holds else f"n={n}, real_rank={rank}, expected_rank={expected_rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.5f} std={std_metric_value:.5f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.5f} std={std_metric_value:.5f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")