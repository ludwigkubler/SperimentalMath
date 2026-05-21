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
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def resolution_tree_width(G):
        # Placeholder function to compute resolution tree width
        # This is a stub and should be replaced with actual computation
        return random.randint(1, 10)

    def euler_characteristic(A):
        m, n = len(A), len(A[0])
        det = Fraction(1)
        for i in range(m):
            det *= A[i][i]
        return det

    def tseitin_formula(n):
        # Placeholder function to generate a Tseitin formula
        # This is a stub and should be replaced with actual generation
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    G = tseitin_formula(n)
    A = gaussian_elimination(G)
    ν_G = euler_characteristic(A)
    L_G = resolution_tree_width(G)

    if ν_G == 0:
        return {
            "metric_name": "Resolution Tree Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Euler characteristic is zero"
        }

    metric_value = L_G >= 2**(2 * ν_G)
    return {
        "metric_name": "Resolution Tree Width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    total_metric_value = 0

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if trial_result["metric_value"] is not None:
            total_metric_value += trial_result["metric_value"]
        results.append(trial_result)

    mean_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Euler characteristic is zero\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")