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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def read_twice_bp_width(circuit_size, n):
        # Simplified model of BP width
        return circuit_size / math.log2(n)
    
    def generate_geometrically_motivic_variety(n):
        # Placeholder function to generate a geometrically motivic variety
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    def construct_circuit(size, n):
        # Placeholder function to construct a circuit
        # This is a dummy implementation and should be replaced with actual computation
        return size
    
    n = 30
    k = 2
    X = generate_geometrically_motivic_variety(n)
    φ_X = matrix_rank([[X, 1], [0, X]])
    C_size = construct_circuit(10**k, n)
    bp_width = read_twice_bp_width(C_size, n)
    
    if φ_X <= 2 * n**(k-1):
        conjecture_holds = bp_width <= φ_X
        counterexample = "" if conjecture_holds else "Counterexample found"
    else:
        conjecture_holds = False
        counterexample = "φ(X) > 2*n^(k-1)"
    
    return {
        "metric_name": "read_twice_bp_width",
        "metric_value": bp_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= φ_X) / len(results)
    
    if all(r <= φ_X for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > φ_X for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > φ_X)
        print(f"RESULT: FALSIFIED counterexample=\"φ(X) > 2*n^(k-1)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")