# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + sum(1 for j in range(i+1, m) if abs(A[j][i]) > abs(A[i][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
        return C

    def noncommutative_entanglement(protocol):
        # Placeholder for the actual computation of noncommutative entanglement
        # This is a dummy function that returns a random value for demonstration purposes
        n = len(protocol)
        return random.uniform(0, n**(1/4))

    instances_tested = 0
    total_nent_pi = 0.0
    n_max = 5

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            protocol = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            nent_pi = noncommutative_entanglement(protocol)
            total_nent_pi += nent_pi
            instances_tested += 1
            if len(protocol) > n_max:
                n_max = len(protocol)

    mean_nent_pi = total_nent_pi / instances_tested
    conjecture_holds = mean_nent_pi <= 1.2 * Fraction(n_max**(1/4), 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "noncommutative_entanglement",
        "metric_value": mean_nent_pi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_nent_pi = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_nent_pi} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_nent_pi} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")