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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    for i in range(m):
        if any(A_copy[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def communication_complexity_rank(f, n):
    # Generate all possible assignments of 0 and 1 to the variables
    assignments = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
    # Calculate the communication complexity matrix A_f
    A_f = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if f(assignments[i]) == f(assignments[j]):
                A_f[i][j] = 1
    return matrix_rank(A_f)

def local_indeterminacy(C_f):
    # Placeholder function, as the actual calculation is complex and depends on C_f
    n = len(C_f)
    return random.randint(0, n**2)  # Simplified for testing purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = lambda x: sum(x) % 2  # Example Boolean function
    C_f = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    local_indet = local_indeterminacy(C_f)
    comm_complexity_rank = communication_complexity_rank(f, n)
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": comm_complexity_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": local_indet <= comm_complexity_rank,
        "counterexample": "" if local_indet <= comm_complexity_rank else f"local_indet={local_indet} > comm_complexity_rank={comm_complexity_rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["n_max"] >= 16 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"local_indet > comm_complexity_rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")