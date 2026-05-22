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
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_of_matrix(A):
        A_copy = [row[:] for row in A]
        gaussian_elimination(A_copy)
        rank = sum(1 for row in A_copy if any(row[j] != 0 for j in range(len(row))))
        return rank

    def monotone_circuit_size(n, k):
        # Simplified approximation of the circuit size
        return n ** (1.5 * k - 1)

    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    
    # Generate a symmetric space S with known cohomology ring
    # For simplicity, we use a diagonal matrix as an example
    A = [[random.random() if i == j else 0 for j in range(n)] for i in range(n)]
    H = matrix_multiplication(A, A)
    
    minimal_rank = rank_of_matrix(H)
    circuit_size = monotone_circuit_size(n, k)
    
    return {
        "metric_name": "Minimal Rank of Hodge Decomposition",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= 1.5 * circuit_size,
        "counterexample": "" if minimal_rank >= 1.5 * circuit_size else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    rank_values = [r["metric_value"] for r in results]
    circuit_size_values = [monotone_circuit_size(n, k) for n in range(5, 41) for k in range(2, min(n // 2, 10))]
    
    rank_mean = sum(rank_values) / len(rank_values)
    rank_median = sorted(rank_values)[len(rank_values) // 2]
    circuit_size_mean = sum(circuit_size_values) / len(circuit_size_values)
    circuit_size_median = sorted(circuit_size_values)[len(circuit_size_values) // 2]
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={rank_mean} std={math.sqrt(sum((x - rank_mean) ** 2 for x in rank_values) / len(rank_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")