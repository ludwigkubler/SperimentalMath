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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    r = 0
    for row in A:
        if any(row):
            r += 1
    return r

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random CNF formula with n variables and m clauses
        m = random.randint(1, n * (n - 1) // 2)
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)

        # Convert CNF to symmetric tensor via clause incidence matrix
        A = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    A[var][var] += 1
                else:
                    A[0][var] += 1

        # Compute symmetric tensor rank using rank decomposition
        tensor_rank = rank(A)

        # Compare with known circuit sizes
        if n <= 40:
            expected_circuit_size = n**2 if any(lit > 0 for lit in random.choice(cnf)) else n
            if tensor_rank < expected_circuit_size:
                conjecture_holds = False
                counterexample = f"n={n}, rank={tensor_rank}, expected={expected_circuit_size}"
                break

        metric_value += tensor_rank / instances_tested

    return {
        "metric_name": "Symmetric Tensor Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")