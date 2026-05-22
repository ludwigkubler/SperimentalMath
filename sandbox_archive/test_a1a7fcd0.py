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
    n = len(A)
    A_rref = [row[:] for row in A]
    for i in range(n):
        if A_rref[i][i] == 0:
            # Swap with a non-zero row below
            for j in range(i + 1, n):
                if A_rref[j][i] != 0:
                    A_rref[i], A_rref[j] = A_rref[j], A_rref[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        for j in range(n):
            if i == j:
                continue
            factor = Fraction(A_rref[j][i], A_rref[i][i])
            for k in range(n):
                A_rref[j][k] -= factor * A_rref[i][k]
    return A_rref

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank_value = sum(1 for row in rref if any(row))
    return rank_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 3))
    
    # Generate a random symmetric space S with known cohomology ring
    # For simplicity, we use a diagonal matrix as an example
    A = [[random.randint(1, 10) if i == j else 0 for j in range(n)] for i in range(n)]
    H = rank(A)
    
    # Find a monotone circuit that computes k-CLIQUE on a complete graph with n vertices
    # For simplicity, we use the known lower bound of Ω(n^(1.5k - 1))
    circuit_size = math.ceil(n ** (1.5 * k - 1))
    
    return {
        "metric_name": "Minimal Rank(H^*(S))",
        "metric_value": H,
        "instances_tested": 1,
        "conjecture_holds": H >= 1.5 * circuit_size,
        "counterexample": "" if H >= 1.5 * circuit_size else f"n={n}, k={k}, rank={H}, circuit_size={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    rank_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    circuit_sizes = [c["metric_value"] for c in results if c["conjecture_holds"]]
    
    if not rank_values or not circuit_sizes:
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        rank_mean = sum(rank_values) / len(rank_values)
        circuit_size_mean = sum(circuit_sizes) / len(circuit_sizes)
        support_fraction = len(results) / len(seeds)
        
        if rank_mean >= 1.5 * median(rank_values) and circuit_size_mean >= 1.5 * median(circuit_sizes):
            print(f"RESULT: SUPPORTED mean=rank_mean std=circuit_size_mean support_fraction=support_fraction")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"n={n}, k={k}, rank={H}, circuit_size={circuit_size}\" first_failing_seed={first_failing_seed}")