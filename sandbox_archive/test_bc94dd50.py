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
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def hyperbolic_metric(A):
        m, n = len(A), len(A[0])
        sum_dist = 0
        for i in range(m):
            for j in range(i+1, m):
                dist = 0
                for k in range(n):
                    dist += abs(A[i][k] - A[j][k])
                sum_dist += dist
        return sum_dist / (m * (m - 1) // 2)

    def dpll_proof_tree_height(clause_set):
        if not clause_set:
            return 0
        if len(clause_set) == 1:
            return 1
        variable = random.choice(list(clause_set[0]))
        true_clauses = {c for c in clause_set if variable in c}
        false_clauses = {c for c in clause_set if not any(v in c for v in [variable, -variable])}
        return 1 + max(dpll_proof_tree_height(true_clauses), dpll_proof_tree_height(false_clauses))

    n = random.choice([5, 10, 15, 20, 30, 40])
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = set(random.sample(variables + [-v for v in variables], random.randint(1, n)))
        clauses.append(clause)
    
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    hyperbolic_comp = hyperbolic_metric(A)
    
    height = dpll_proof_tree_height(clauses)
    
    return {
        "metric_name": "DPLL Proof Tree Height",
        "metric_value": height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": height <= 10 * hyperbolic_comp,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")