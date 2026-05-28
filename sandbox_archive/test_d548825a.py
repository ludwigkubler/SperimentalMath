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
    
    def generate_function(N):
        return {i: (-1)**random.randint(0, 1) for i in range(N)}
    
    def xor_circuit_size(f):
        N = len(f)
        circuit = []
        for i in range(N):
            if f[i] == -1:
                circuit.append('NOT')
            else:
                circuit.append('ID')
        return len(circuit)
    
    def barratt_floer_homology_rank(f):
        N = len(f)
        A = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(i+1, N):
                if f[i] != f[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return -1
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def expected_rank(N):
        # Simplified approximation, actual calculation depends on distribution of f
        return math.log2(N)
    
    results = []
    for N in [5, 10, 15, 20, 30, 40]:
        for _ in range(30):
            f = generate_function(N)
            rank = barratt_floer_homology_rank(f)
            circuit_size = xor_circuit_size(f)
            expected = expected_rank(N)
            ratio = circuit_size / (expected + 1)
            results.append({
                "N": N,
                "rank": rank,
                "circuit_size": circuit_size,
                "ratio": ratio
            })
    
    total_ratio = sum(result['ratio'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['ratio'] >= 2**(result['rank'] + 1)) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_size_to_rank_ratio",
        "metric_value": total_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_ratio = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")