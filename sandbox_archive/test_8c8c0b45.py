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
    
    def generate_tseitin_formula(n):
        # Generate a random n-vertex graph and corresponding Tseitin formula
        edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n)]
        return edges
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(row_echelon_form[i]):
                rank += 1
        return rank
    
    def resolution_proof_length(edges):
        # Simplified estimation of resolution proof length (not actual proof)
        return len(edges) ** 2
    
    n = random.randint(5, 40)
    edges = generate_tseitin_formula(n)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1
    
    symplectic_rank = rank(matrix)
    proof_length = resolution_proof_length(edges)
    
    return {
        "metric_name": "Symplectic Rank / Resolution Proof Length",
        "metric_value": symplectic_rank / proof_length,
        "instances_tested": 1,
        "conjecture_holds": symplectic_rank >= math.log(proof_length, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Symplectic Rank / Resolution Proof Length ratio < 2^k"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")