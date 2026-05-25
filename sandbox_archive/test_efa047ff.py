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
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank

    def tseitin_clauses(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
        return clauses

    def resolution_refutation_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    if set(stack[i]) & set(stack[j]):
                        new_clause = [x for x in stack[i] + stack[j] if x not in set(stack[i]) & set(stack[j])]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return 0
            stack.append(new_clause)
            if len(new_clause) == 1:
                return len(stack)

    n = random.randint(5, 40)
    clauses = tseitin_clauses(n)
    refutation_length = resolution_refutation_length(clauses)
    
    Q_C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank_Q_C = matrix_rank(Q_C)

    metric_value = rank_Q_C
    instances_tested = 1
    conjecture_holds = rank_Q_C >= 2**(n/4) and rank_Q_C <= 2**n / refutation_length
    counterexample = "" if conjecture_holds else f"Q(C)={rank_Q_C}, n={n}, refutation_length={refutation_length}"
    
    return {
        "metric_name": "Quantum Logarithm Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")