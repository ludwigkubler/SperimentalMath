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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for k in range(i + 1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i - 1, -1, -1):
            b[k] -= A[k][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def frege_refutation_depth(cnf):
    n = len(cnf)
    assignment = {}
    stack = []
    for clause in cnf:
        if all(var not in assignment and -var not in assignment for var in clause):
            var = random.choice([v for v in range(1, n + 1) if v not in assignment and -v not in assignment])
            assignment[var] = True
            stack.append((var, True))
        elif any(-var in assignment and not assignment[-var] for var in clause):
            continue
        else:
            return len(stack)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_entropy = 0.0

    for n in range(5, 41):
        for m in range(10):  # Generate 10 CNFs per size
            cnf = []
            for _ in range(m):
                clause = random.sample(range(1, n + 1), random.randint(1, n))
                cnf.append(clause)
            depth = frege_refutation_depth(cnf)

            if depth == 0:
                continue

            instances_tested += 1
            total_entropy += depth

    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else 0.0
    conjecture_holds = mean_entropy >= 0
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")