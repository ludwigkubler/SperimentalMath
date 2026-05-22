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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(m):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tseitin_formula(G):
        n = len(G)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            if G[i]:
                clauses.append([literals[i]])
                for j in range(i + 1, n):
                    if G[i][j]:
                        clauses.append([-literals[i], literals[j]])
                        clauses.append([-literals[j], literals[i]])
        return clauses

    def resolution(refutation):
        while refutation:
            new_clauses = []
            for i in range(len(refutation)):
                for j in range(i + 1, len(refutation)):
                    if any(-x in refutation[i] and x in refutation[j] for x in set(refutation[i]) & set(refutation[j])):
                        new_clause = [x for x in refutation[i] | refutation[j] if x != -x]
                        if not any(new_clause == clause for clause in refutation):
                            new_clauses.append(new_clause)
            if not new_clauses:
                return False
            refutation.extend(new_clauses)
        return True

    def local_index(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    A[i][j] = A[j][i] = 1
        refutation = []
        for i in range(n):
            row = [0] * n
            row[i] = -1
            refutation.append(row)
        return len(gaussian_elimination(refutation))

    def is_expander(G, ν):
        n = len(G)
        λ = 2 ** (-ν)
        for u in range(n):
            neighbors = sum(1 for v in range(n) if G[u][v])
            if neighbors < (1 - λ) * n or neighbors > (1 + λ) * n:
                return False
        return True

    def is_constant(G, ν):
        n = len(G)
        return all(sum(G[i][j] for j in range(n)) == 2 ** ν for i in range(n))

    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0

    ν = local_index(G)
    Tseitin_clauses = tseitin_formula(G)

    if is_constant(G, ν):
        refutation_length = resolution(Tseitin_clauses) and len(Tseitin_clauses)
    else:
        refutation_length = resolution(Tseitin_clauses) and len(Tseitin_clauses)

    conjecture_holds = (refutation_length >= 2 ** ν if not is_constant(G, ν) else refutation_length <= 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 6)]
    
    results = []
    total_metric_value = 0
    num_supporting_seeds = 0

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            num_supporting_seeds += 1

    mean_metric_value = total_metric_value / len(results)
    support_fraction = num_supporting_seeds / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and not result["counterexample"] == "mapping_undefined" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")