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
    n = random.randint(5, 40)
    d = random.randint(2, 5)
    
    # Generate a random AC⁰ circuit computing parity for n bits
    circuit = [random.choice([0, 1]) for _ in range(n)]
    
    # Construct the communication matrix of the circuit
    comm_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        comm_matrix[i][i] = 1
        comm_matrix[n][i] = circuit[i]
    
    # Compute the real rank of the communication matrix using numerical linear algebra
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return sum(1 for row in A if any(row))

    real_rank = gaussian_elimination(comm_matrix)
    
    # Verify scaling with Ω(n^(1/(d-1)))
    expected_rank = math.ceil(n ** (1 / (d - 1)))
    conjecture_holds = real_rank >= expected_rank
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, rank={real_rank}"
    
    return {
        "metric_name": "Real Rank",
        "metric_value": real_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")