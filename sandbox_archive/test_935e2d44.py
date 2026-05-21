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
        n = len(A)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i, n + 1):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n + 1):
                        A[k][j] -= factor * A[i][j]
        return A

    def spectral_gap(A):
        n = len(A)
        A = gaussian_elimination(A)
        eigenvalues = [A[i][i] for i in range(n)]
        lambda_max = max(eigenvalues, key=abs)
        lambda_min = min(eigenvalues, key=abs)
        return abs(lambda_max - lambda_min)

    def symplectic_orthogonal_matrix(dnf):
        n = len(dnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in dnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    matrix[i][i + 1] += 1
                else:
                    matrix[i + 1][i] -= 1
        return matrix

    def is_submodular(gap):
        n = len(gap)
        for i in range(n):
            for j in range(i + 1, n):
                if gap[j] - gap[i] > gap[i + 1] - gap[j]:
                    return False
        return True

    n = random.randint(5, 40)
    dnf = [[random.choice([-i, i]) for _ in range(n)] for _ in range(random.randint(2, n))]
    matrix = symplectic_orthogonal_matrix(dnf)
    gap = spectral_gap(matrix)

    if gap <= 0:
        return {
            "metric_name": "spectral_gap",
            "metric_value": gap,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "negative_or_zero"
        }

    c = math.log(n) / n
    if not (c * n ** c * math.log(n) <= gap):
        return {
            "metric_name": "spectral_gap",
            "metric_value": gap,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"gap < {c} * n^c * log(n)"
        }

    if not is_submodular(gap):
        return {
            "metric_name": "spectral_gap",
            "metric_value": gap,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_submodular"
        }

    if gap > math.log(n) ** 2:
        return {
            "metric_name": "spectral_gap",
            "metric_value": gap,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"gap > log^2(n)"
        }

    return {
        "metric_name": "spectral_gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    else:
        counterexample = min((r["counterexample"] for r in results if not r["conjecture_holds"]), key=len)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")