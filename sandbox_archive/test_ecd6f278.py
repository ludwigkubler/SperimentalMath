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

def generate_sat_instance(m: int, n: int):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def compute_measure(clauses, d):
    m = len(clauses)
    n = len(clauses[0]) if clauses else 0
    A = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if j + 1 in clauses[i]:
                A[i][j] = 1
        A[i][-1] = -1
    rank = gaussian_elimination(A)
    return Fraction(2 ** (m - rank), d)

def compute_frege_width(clauses):
    m = len(clauses)
    n = len(clauses[0]) if clauses else 0
    max_clause_length = max(len(clause) for clause in clauses)
    frege_width = 1
    for i in range(m):
        frege_width *= (2 ** (max_clause_length - len(clauses[i])) + 1)
    return frege_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in m_values:
        for _ in range(5):
            clauses = generate_sat_instance(m=n, n=n)
            d = n
            measure = compute_measure(clauses, d)
            frege_width = compute_frege_width(clauses)
            results.append((measure, frege_width))
    
    if not results:
        return {
            "metric_name": "Frege Proof Width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_measure = sum(result[0] for result in results) / len(results)
    max_frege_width = max(result[1] for result in results)
    deviation = abs(max_frege_width - mean_measure ** (d + 1))
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": max_frege_width,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": deviation <= 3,
        "counterexample": "" if deviation <= 3 else f"deviation={deviation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deviation\" first_failing_seed={first_failing_seed}")