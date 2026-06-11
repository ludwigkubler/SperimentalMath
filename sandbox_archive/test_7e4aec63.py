# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_xor(n):
    literals = [i for i in range(1, n+1)]
    clauses = []
    for i in range(n-1):
        for j in range(i+1, n):
            clause = [-literals[i], -literals[j], literals[n]]
            clauses.append(clause)
            clause = [literals[i], literals[j], -literals[n]]
            clauses.append(clause)
    return literals, clauses

def generate_and(n):
    literals = [i for i in range(1, n+1)]
    clauses = []
    for row in generate_xor(n):
        for i in range(len(row)-1):
            clause = [-row[i], -row[i+1], literals[n]]
            clauses.append(clause)
            clause = [row[i], row[i+1], -literals[n]]
            clauses.append(clause)
    return literals, clauses

def generate_instance():
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return generate_xor(1)
    elif n == 2:
        return generate_and(2)
    else:
        return generate_xor(n)

def mld(phi):
    literals, clauses = phi
    n = len(literals)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        if len(clause) == 3 and clause[2] > 0:
            i = abs(clause[0])
            j = abs(clause[1])
            k = clause[2]
            matrix[i][j] += 1
            matrix[j][i] += 1
    for i in range(1, n + 1):
        matrix[i][n] += 1
        matrix[n][i] += 1
    return sum(matrix[i][j] for i in range(1, n + 1) for j in range(i + 1, n + 1))

def rank_variance(phi):
    literals, clauses = phi
    n = len(literals)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        if len(clause) == 3 and clause[2] > 0:
            i = abs(clause[0])
            j = abs(clause[1])
            k = clause[2]
            matrix[i][j] += 1
            matrix[j][i] += 1
    for i in range(1, n + 1):
        matrix[i][n] += 1
        matrix[n][i] += 1
    return sum(matrix[i][j] for i in range(1, n + 1) for j in range(i + 1, n + 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        phi = generate_instance()
        mld_value = mld(phi)
        r_value = rank_variance(phi)
        if mld_value > 3 * r_value or mld_value < r_value / 3:
            return {
                "metric_name": "mld_vs_r",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": len(phi[0]),
                "conjecture_holds": False,
                "counterexample": "mld(φ) not linearly related to r(φ)"
            }
        results.append(mld_value - r_value)
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    return {
        "metric_name": "mld_vs_r",
        "metric_value": mean,
        "instances_tested": 30,
        "n_max": max(len(phi[0]) for _ in range(30)),
        "conjecture_holds": abs(mean) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if abs(r) <= 3) / len(results)
    
    if all(abs(r) <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r) > 3 for r in results):
        first_failing_seed = seeds[results.index(next(x for x in results if abs(x) > 3))]
        print(f"RESULT: FALSIFIED counterexample='mld(φ) not linearly related to r(φ)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")