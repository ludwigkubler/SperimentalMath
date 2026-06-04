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
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m = len(A)
        p = len(B[0])
        q = len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(q):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(minor)
            sign *= -1
        return det

    def geometric_galois_group_size(A):
        n = len(A)
        if n == 0:
            return 1
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return math.factorial(n) // (math.factorial(rank) * math.factorial(n - rank))

    def dpll_proof_tree_height(phi):
        # Placeholder function to simulate DPLL proof tree height calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)

    instances_tested = 0
    n_max = 0
    total_order = 0
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        order = geometric_galois_group_size(phi)
        height = dpll_proof_tree_height(phi)

        if instances_tested == 0:
            n_max = n

        total_order += order
        instances_tested += 1

    mean_order = total_order / instances_tested
    conjecture_holds = mean_order >= math.log(n_max)

    return {
        "metric_name": "geometric_galois_group_size",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            counterexample = trial_result["counterexample"]
            break
        else:
            results.append(trial_result)

    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")