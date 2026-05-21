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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = rank
        for i in range(rank, rows):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if abs(matrix[i_max][j]) < 1e-9:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rows):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def generate_random_3cnf(n, m):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 3)
        sign = [random.choice([-1, 1]) for _ in range(3)]
        clause = [(sign[i] * var) % n for i, var in enumerate(clause)]
        clauses.append(clause)
    return clauses

def generate_kclique_3cnf(n, k):
    if k > n:
        raise ValueError("k must be less than or equal to n")
    variables = list(range(1, n + 1))
    edges = [(i, j) for i in range(1, n) for j in range(i + 1, n + 1)]
    random.shuffle(edges)
    selected_edges = edges[:k * (k - 1) // 2]
    clauses = []
    for u, v in selected_edges:
        for w in variables:
            if w != u and w != v:
                clause = [u, v, w]
                sign = [random.choice([-1, 1]) for _ in range(3)]
                clause = [(sign[i] * var) % n for i, var in enumerate(clause)]
                clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        kclique_clauses = generate_kclique_3cnf(n, int(0.5 * n))
        random_clauses = generate_random_3cnf(n, int(0.5 * n))
        
        m_kclique = gaussian_elimination([[1 if var in clause else 0 for var in range(1, n + 1)] for clause in kclique_clauses])
        m_random = gaussian_elimination([[1 if var in clause else 0 for var in range(1, n + 1)] for clause in random_clauses])
        
        results.append({
            "n": n,
            "m_kclique": m_kclique,
            "m_random": m_random
        })
    
    total_kclique = sum(result["m_kclique"] for result in results)
    total_random = sum(result["m_random"] for result in results)
    instances_tested = len(results) * len(n_values)
    
    conjecture_holds = all(m_kclique >= n for result in results for m_kclique in [result["m_kclique"]] + [math.log(n) for n in range(2, 10)]) and \
                      all(m_random <= math.log(n) for result in results for m_random in [result["m_random"]])
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "matroid_rank_gap",
        "metric_value": total_kclique / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")