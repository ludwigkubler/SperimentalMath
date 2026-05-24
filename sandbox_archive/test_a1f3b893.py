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
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if all(abs(A[j][i]) < 1e-9 for j in range(i, m)):
                continue
            pivot_row = next((j for j in range(i, m) if abs(A[j][i]) > 1e-9), None)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(m):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            rank += 1
        return rank
    
    def commutator(A, B):
        return matrix_multiply(matrix_multiply(A, B), -matrix_multiply(B, A))
    
    def minimal_index_of_noncommutativity(channel):
        n = len(channel)
        identity = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        comm = commutator(identity, channel)
        return matrix_rank(comm)
    
    def read_twice_branching_program_size(channel):
        n = len(channel)
        size = 2 * (n - 1)
        for i in range(1, n):
            size += 2 ** i
        return size
    
    def generate_quantum_channel(n):
        channel = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            channel[i][i] -= sum(channel[i][j] for j in range(i) if i != j)
        return channel
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        channel = generate_quantum_channel(n)
        rho = minimal_index_of_noncommutativity(channel)
        bp_size = read_twice_branching_program_size(channel)
        log_bp_size = math.log(bp_size)
        
        results.append({
            "n": n,
            "rho": rho,
            "log_bp_size": log_bp_size
        })
    
    mean_rho = sum(result["rho"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["rho"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if n_values[0] <= result["n"] <= n_values[-1]) / len(results)
    
    conjecture_holds = all(n_values[0] <= result["n"] <= n_values[-1] and mean_rho - 3 * std_rho <= result["rho"] <= mean_rho + 3 * std_rho for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_index_of_noncommutativity",
        "metric_value": mean_rho,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")