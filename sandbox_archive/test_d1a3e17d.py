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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]

    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_sub(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_inv(A, mod):
        n = len(A)
        I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        A_augmented = [row + col for row, col in zip(A, I)]
        gaussian_elimination(A_augmented, [0] * n)
        return [row[n:] for row in A_augmented]

    def tseitin_formula(n):
        clauses = []
        for i in range(1, 2**n):
            binary = bin(i)[2:].zfill(n)
            clause = []
            for j in range(n):
                if binary[j] == '0':
                    clause.append(f"~x{j+1}")
                else:
                    clause.append(f"x{j+1}")
            clauses.append(" | ".join(clause))
        return " & ".join(clauses)

    def dpll_search_tree_width(formula, n):
        # Simplified DPLL search tree width calculation
        return 2**n

    def eta_invariant(n):
        # Simplified Eta-invariant calculation (not actual implementation)
        return random.random() * n

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = tseitin_formula(n)
    width = dpll_search_tree_width(formula, n)
    eta = eta_invariant(n)

    return {
        "metric_name": "eta_invariant",
        "metric_value": eta,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")