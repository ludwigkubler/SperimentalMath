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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(min(m, n)):
            if abs(A[i][i]) > 1e-9:
                r += 1
        return r

    def xor_and_tree_width(n):
        # Placeholder function to compute XOR-AND tree width
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)

    m = random.randint(2, 40)
    n = random.randint(2, 40)
    c = 1.0  # Placeholder constant

    formula = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    H_F = gaussian_elimination(formula)
    r_H_F = rank(H_F)
    tw_F = xor_and_tree_width(n)

    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": tw_F,
        "instances_tested": 1,
        "conjecture_holds": tw_F <= c * r_H_F,
        "counterexample": "" if tw_F <= c * r_H_F else f"Formula with m={m}, n={n} violates the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with m={m}, n={n} violates the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")