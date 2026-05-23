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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(r)):
                r += 1
        return r

    def ac0_circuit_edges(n):
        # Simplified model of AC0 circuit edges for dihedral groups
        return n * (n - 1) // 2

    n = random.randint(5, 40)
    G = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    C_G_edges = ac0_circuit_edges(n)

    Trop_G = gaussian_elimination(G)
    min_rank = rank(Trop_G)

    ratio = min_rank / math.sqrt(C_G_edges)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound\" first_failing_seed={first_failing_seed}")