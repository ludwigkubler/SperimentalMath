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
    
    def p_adic_differential(clause, p):
        n = len(clause)
        diff = [0] * (n + 1)
        for i in range(n):
            if clause[i] == '1':
                diff[i+1] += 1
            elif clause[i] == '0':
                diff[i+1] -= 1
        return diff
    
    def min_rank(p_adic_diffs):
        A = [diff[:] for diff in p_adic_diffs]
        rank = 0
        for i in range(len(A)):
            if any(A[j][i] != 0 for j in range(i, len(A))):
                rank += 1
                gaussian_elimination(A)
        return rank
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = ''.join(random.choice('01') for _ in range(n))
            clauses.append(clause)
        return clauses
    
    n = random.randint(5, 40)
    p = 2
    cnf = generate_cnf(n)
    p_adic_diffs = [p_adic_differential(clause, p) for clause in cnf]
    rank = min_rank(p_adic_diffs)
    
    metric_value = rank / n**0.5
    conjecture_holds = 1.5 * (n**0.5) >= rank >= 0.5 * (n**0.5)
    counterexample = "" if conjecture_holds else f"Rank {rank} for n={n}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": metric_value,
        "instances_tested": len(cnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37, 37))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")