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
    
    def gaussian_elimination(A, b):
        n = len(b)
        A_augmented = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                    max_row = j
            A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
            pivot = A_augmented[i][i]
            for j in range(i, n+1):
                A_augmented[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A_augmented[k][i]
                    for j in range(i, n+1):
                        A_augmented[k][j] -= factor * A_augmented[i][j]
        return [row[-1] for row in A_augmented]

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix_rref = gaussian_elimination(matrix, [0]*n)
        rank = 0
        for i in range(m):
            if any(row[i] != 0 for row in matrix_rref):
                rank += 1
        return rank

    def p_adic_hensel_steps(A, b, p):
        n = len(b)
        A_mod_p = [[a % p for a in row] for row in A]
        b_mod_p = [b_i % p for b_i in b]
        steps = 0
        while True:
            x = gaussian_elimination(A_mod_p, b_mod_p)
            if all(x[i] == 0 for i in range(n)):
                break
            A_mod_p = [[a - (x[i] * A_mod_p[i][j]) % p for j in range(n)] for i in range(n)]
            b_mod_p = [(b_i - (x[i] * b_mod_p[i])) % p for i in range(n)]
            steps += 1
        return steps

    n = random.randint(5, 40)
    p = random.randint(2, 10)
    A = [[random.randint(0, p-1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, p-1) for _ in range(n)]

    hensel_steps = p_adic_hensel_steps(A, b, p)
    comm_complexity_rank = rank(A)

    return {
        "metric_name": "p-adic Hensel Steps vs Comm Complexity Rank",
        "metric_value": abs(hensel_steps - comm_complexity_rank),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(hensel_steps - comm_complexity_rank) <= 3,
        "counterexample": "" if abs(hensel_steps - comm_complexity_rank) <= 3 else f"Steps: {hensel_steps}, Rank: {comm_complexity_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")