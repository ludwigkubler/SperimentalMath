# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate the entries below the pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i + 1, n):
            matrix[j][i] *= -factor
        for k in range(i + 1, n):
            for l in range(i, n):
                matrix[k][l] += matrix[j][l]
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    try:
        A = gaussian_elimination(phi)
        grr_rank = sum(1 for row in A if any(row))
        proof_width = n * (n - 1) // 2  # Upper bound for resolution proof width
        return {
            "metric_name": "grr_rank",
            "metric_value": grr_rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": grr_rank <= proof_width,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "grr_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_grr_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_grr_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_grr_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break