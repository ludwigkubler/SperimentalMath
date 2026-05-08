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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[i:] for row in A]

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        return sum(1 for row in reduced_matrix if any(row))

    def is_monotone_dnf(dnf):
        n = len(dnf[0])
        for clause in dnf:
            if not all(x == 0 or x == 1 for x in clause):
                return False
        return True

    def generate_k_clique_dnf(n, k):
        clauses = []
        for i in range(1 << n):
            if bin(i).count('1') == k:
                clause = [1 if (i >> j) & 1 else 0 for j in range(n)]
                clauses.append(clause)
        return clauses

    def dnf_size(dnf):
        return len(dnf)

    def spread(dnf):
        n = len(dnf[0])
        rank_function = [rank([clause[:i] + clause[i+1:] for clause in dnf]) for i in range(n)]
        return max(rank_function) - min(rank_function)

    n = 20
    k = random.randint(5, 10)
    dnf = generate_k_clique_dnf(n, k)
    
    if not is_monotone_dnf(dnf):
        return {
            "metric_name": "spread",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    spread_value = spread(dnf)
    dnf_size_value = dnf_size(dnf)

    return {
        "metric_name": "spread",
        "metric_value": spread_value,
        "instances_tested": 1,
        "conjecture_holds": spread_value >= k**(1/4) * math.log(n) and dnf_size_value >= n**(k**(1/4)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    spread_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(spread_values)/len(spread_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(spread_values)/len(spread_values)} std={math.sqrt(sum((x - sum(spread_values)/len(spread_values))**2 for x in spread_values) / len(spread_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"spread does not meet the conjectured bound\" first_failing_seed={first_failing_seed + 2}")  # Adjust seed index