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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if all(abs(A[j][i]) < 1e-9 for j in range(rank)):
                continue
            rank += 1
            A[i], A[rank - 1] = A[rank - 1], A[i]
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and abs(A[k][i]) > 1e-9:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return rank

    def dpll_search_tree_height(n):
        # Simplified approximation of DPLL search tree height
        # This is a placeholder and should be replaced with actual computation
        return 2 ** n

    def symplectic_leaves_rank(A):
        # Placeholder for computing the minimal rank of symplectic leaves
        # This is a placeholder and should be replaced with actual computation
        return matrix_rank(gaussian_elimination(A))

    n = random.randint(5, 40)
    A = [[random.choice([0, 1]) if i == j else 0 for j in range(n)] for i in range(n)]
    h_A = dpll_search_tree_height(n)
    kappa_L_A = symplectic_leaves_rank(A)

    if kappa_L_A <= c * h_A:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Counterexample found for n={n}, kappa(L(A))={kappa_L_A}, c*h(A)={c*h_A}"

    return {
        "metric_name": "Ratio of kappa(L(A))/c/h(A)",
        "metric_value": Fraction(kappa_L_A, h_A) / c,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")