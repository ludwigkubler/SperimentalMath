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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f'x{i}'])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'-x{i}', f'-x{j}', f'x{i+j-1}'])
        return literals, clauses

    def diophantine_system(literals, clauses):
        n = len(literals)
        A = [[0] * (n + 1) for _ in range(n)]
        b = [0] * n
        for clause in clauses:
            if len(clause) == 1:
                i = int(clause[0][1:]) - 1
                A[i][i] = 1
                b[i] = 1 if clause[0][0] != '-' else -1
            elif len(clause) == 2:
                i, j = [int(l[1:]) - 1 for l in clause if l[0] != '-']
                A[i][j] = 1
                A[j][i] = 1
        return A, b

    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n+1)]
                b[j] -= factor * b[i]
        return A, b

    def minimal_order(A):
        n = len(b)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    def sat_clause_subset_complexity(clauses):
        return len(clauses)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        literals, clauses = tseitin_formula(n)
        A, b = diophantine_system(literals, clauses)
        _, _ = gaussian_elimination(A, b)
        minimal_order_value = minimal_order(A)
        sat_complexity = sat_clause_subset_complexity(clauses)
        results.append({
            "n": n,
            "minimal_order": minimal_order_value,
            "sat_complexity": sat_complexity
        })

    mean_order = sum(r["minimal_order"] for r in results) / len(results)
    mean_complexity = sum(r["sat_complexity"] for r in results) / len(results)
    ratio = mean_order / mean_complexity

    conjecture_holds = abs(ratio - 1) <= 0.1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} not within ±10% of 1"

    return {
        "metric_name": "MinimalOrder/SATComplexityRatio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of ±10%\" first_failing_seed={first_failing_seed}")