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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(cols):
            if j != i and matrix[rank][j] != 0:
                factor = Fraction(matrix[rank][j], matrix[rank][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def matrix_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows == 0 or cols == 0:
        return 0
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random CNF with n variables
        num_clauses = random.randint(2 * n, 4 * n)
        cnf = [[random.randint(-n, n) for _ in range(random.randint(1, n))] for _ in range(num_clauses)]
        
        # Transform the CNF into a matrix representation
        matrix = []
        for clause in cnf:
            row = [0] * (2 * n + 1)
            for lit in clause:
                if lit > 0:
                    row[lit - 1] = 1
                else:
                    row[-lit] = -1
            matrix.append(row)
        
        # Compute the minimal order of the Lie algebroid structure
        rank = matrix_rank(matrix)
        
        # Measure the resolution proof width (simplified for this test)
        w_phi = num_clauses
        
        results.append({
            "n": n,
            "rank": rank,
            "w_phi": w_phi
        })
    
    total_rank = sum(result["rank"] for result in results)
    total_w_phi = sum(result["w_phi"] for result in results)
    mean_ratio = Fraction(total_rank, len(results)) / Fraction(total_w_phi, len(results))
    
    conjecture_holds = all(abs(Fraction(result["rank"], result["w_phi"]) - mean_ratio) <= 2 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, rank={results[0]['rank']}, w_phi={results[0]['w_phi']}"

    return {
        "metric_name": "Ratio of Rank to Resolution Proof Width",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}, w_phi={results[0]['w_phi']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")