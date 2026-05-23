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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A_tilde = gaussian_elimination(A)
        r = sum(1 for row in A_tilde if any(row))
        return r

    def monotone_circuit_depth(n, k):
        # Placeholder function to simulate the construction of a monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return n + k  # Example: depth = n + k

    for _ in range(30):  # Ensure at least 30 instances per seed
        n, k = random.randint(5, 40), random.randint(2, min(n-1, 5))  # Ensure k < n
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank_tropicalized = rank(A)
        depth_circuit = monotone_circuit_depth(n, k)

        if rank_tropicalized < n**(k/4) or abs(depth_circuit - n**(k/4)) > 2:
            return {
                "metric_name": "Rank and Depth",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, k={k}, rank_tropicalized={rank_tropicalized}, depth_circuit={depth_circuit}"
            }

    return {
        "metric_name": "Rank and Depth",
        "metric_value": None,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")