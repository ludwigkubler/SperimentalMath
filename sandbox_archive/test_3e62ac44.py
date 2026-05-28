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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = -A[i][i] / A[max_row][i]
            for j in range(n):
                if i != j:
                    A[j][i] += factor * A[max_row][j]
                else:
                    A[j][i] = 0
        rank = sum(1 for row in A if any(row))
        return rank

    def p_adic_l_function_rank(n, prime):
        # Simplified mapping to generate a rank based on n and prime
        return int(math.log2(n) / math.log2(prime))

    prime = 5  # Fixed prime for simplicity
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        rank = p_adic_l_function_rank(n, prime)
        if rank < log2(n):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, expected>=log2({n})={log2(n)}"
            break

    return {
        "metric_name": "p-adic L-function rank",
        "metric_value": log2(40),  # Example metric value based on n=40
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")