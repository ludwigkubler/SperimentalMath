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

def generate_k_cnf(k: int, m: int) -> list:
    variables = set(range(1, k + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, k)
        clauses.append(clause)
    return clauses

def incidence_matrix(clauses: list) -> list:
    n = len(clauses)
    m = max(len(c) for c in clauses)
    matrix = [[0] * m for _ in range(n)]
    for i, clause in enumerate(clauses):
        for j, var in enumerate(clause):
            matrix[i][j] = 1
    return matrix

def determinant(matrix: list) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        det += sign * matrix[0][j] * determinant(submatrix)
    return det

def shannon_entropy(clauses: list) -> float:
    n = len(clauses)
    m = max(len(c) for c in clauses)
    freqs = [sum(1 for c in clauses if i in c) / n for i in range(1, m + 1)]
    entropy = -sum(p * math.log2(p) for p in freqs if p > 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = random.randint(3, 5)  # Number of variables
    m = random.randint(k + 1, 2 * k + 1)  # Number of clauses
    n = len(set(abs(v) for v in generate_k_cnf(k, m)))
    
    if n < 5:
        return {
            "metric_name": "Brauer Group Order / Clause Entropy Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "n_min=5 required"
        }
    
    clauses = generate_k_cnf(k, m)
    matrix = incidence_matrix(clauses)
    det = determinant(matrix)
    entropy = shannon_entropy(clauses)
    
    if entropy == 0:
        return {
            "metric_name": "Brauer Group Order / Clause Entropy Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Entropy is zero"
        }
    
    ratio = abs(det) / entropy
    return {
        "metric_name": "Brauer Group Order / Clause Entropy Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
        sys.exit(0)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if r["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")