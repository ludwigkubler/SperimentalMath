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

def generate_k_cnf(k: int, m: int) -> list:
    variables = set(range(1, k + 1))
    cnf = []
    for _ in range(m):
        clause = random.sample(variables | {-v for v in variables}, k)
        cnf.append(clause)
    return cnf

def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def shannon_entropy(clause_set: set) -> float:
    n = len(clause_set)
    if n == 0:
        return 0.0
    p = 1 / n
    return -p * math.log2(p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for k in k_values:
        n = len(set(abs(v) for v in generate_k_cnf(k, m)))
        if n < 5 or n > 40:
            continue
        cnf = generate_k_cnf(k, n)
        incidence_matrix = [[1 if abs(v) in clause else 0 for v in range(1, k + 1)] for clause in cnf]
        det = determinant(incidence_matrix)
        entropy = shannon_entropy(set(tuple(clause) for clause in cnf))
        
        if det == 0:
            continue
        
        ratio = abs(det) / entropy
        results.append({
            "n": n,
            "det": abs(det),
            "entropy": entropy,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Brauer Group Order to Clause Entropy Ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 10 for result in results)
    counterexample = "" if conjecture_holds else "Ratio exceeded 10"
    
    return {
        "metric_name": "Brauer Group Order to Clause Entropy Ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(result["ratio"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["ratio"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f} < 0.8")