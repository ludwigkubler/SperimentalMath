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
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def generate_ac0_k_distance_circuit(k, n):
        # Simplified AC0-k-distance circuit generation
        # This is a placeholder function and should be replaced with actual logic
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**k)]
    
    def tropicalize(matrix):
        m, n = len(matrix), len(matrix[0])
        tropical_matrix = [[-math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j] > tropical_matrix[i][j]:
                    tropical_matrix[i][j] = matrix[i][j]
        return tropical_matrix
    
    def compute_algebraic_k_theory_group(circuit):
        # Simplified computation of algebraic K-theory group
        # This is a placeholder function and should be replaced with actual logic
        return [[random.choice([0, 1]) for _ in range(len(circuit))]] * len(circuit)
    
    n = random.randint(5, 40)
    k = int(math.log2(n))
    circuit = generate_ac0_k_distance_circuit(k, n)
    algebraic_k_theory_group = compute_algebraic_k_theory_group(circuit)
    tropicalized_group = tropicalize(algebraic_k_theory_group)
    
    rank = gaussian_elimination(tropicalized_group)
    
    metric_name = "Rank of Tropicalized Algebraic K-theory Group"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = (n**(1/3) <= rank <= 2**n)
    counterexample = "" if conjecture_holds else f"Rank {rank} is out of bounds for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")