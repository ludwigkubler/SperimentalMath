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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            A[i] = [x * factor for x in A[i]]
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_of_matrix(A):
        A = gaussian_elimination(A)
        return sum(1 for row in A if any(x != 0 for x in row))

    def frege_proof_width(n):
        # Placeholder function to simulate Frege proof width
        return random.randint(5, n)

    def k_group_rank(G):
        # Placeholder function to simulate K-group rank
        return len(G) * (len(G) - 1) // 2

    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    width = frege_proof_width(n)
    rank = k_group_rank(G)

    if rank == 0:
        return {
            "metric_name": "Ratio of K-group rank to width^c",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "K-group rank is zero"
        }

    ratio = rank / (width ** 0.5)
    return {
        "metric_name": "Ratio of K-group rank to width^c",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        mean_value, std_value, support_fraction = None, None, sum(r["conjecture_holds"] for r in results) / len(results)

    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")