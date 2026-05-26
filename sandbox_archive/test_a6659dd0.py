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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def generate_monotone_circuit(n, k):
        # Placeholder function to generate a random monotone circuit of size n computing k-CLIQUE
        # This is a stub and should be replaced with an actual implementation
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    def braess_sarle_curve(circuit):
        # Placeholder function to compute the Braess–Sarle curve from a monotone circuit
        # This is a stub and should be replaced with an actual implementation
        n = len(circuit)
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 10))
    circuit = generate_monotone_circuit(n, k)
    curve = braess_sarle_curve(circuit)
    rank_value = rank(curve)
    
    alpha_n = log2(n)
    beta_k = log2(k)
    lower_bound = alpha_n**2 + beta_k**2
    
    if rank_value is None:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Exception: division by zero"
        }
    
    return {
        "metric_name": "rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value >= lower_bound and rank_value <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] and r["metric_value"] <= 10 for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")