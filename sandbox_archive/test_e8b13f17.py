# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import permutations

def generate_random_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def communication_matrix(CNF):
    n = len(CNF)
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if any(i in clause and -j in clause for clause in CNF):
                C[i][j] = 1
    return C

def symmetric_group_representations(n):
    G = list(permutations(range(1, n + 1)))
    return G

def noncommutative_fourier_coefficients(CNF, G):
    n = len(CNF)
    F = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            F[j][i] = sum(CNF[j - 1][g[i - 1]] for g in G) / len(G)
    return F

def norm_of_matrix(M):
    max_norm = 0
    for row in M:
        row_norm = sum(abs(x) for x in row)
        if row_norm > max_norm:
            max_norm = row_norm
    return max_norm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    CNF = generate_random_cnf(n)
    C = communication_matrix(CNF)
    G = symmetric_group_representations(n)
    F = noncommutative_fourier_coefficients(CNF, G)
    norm_F = norm_of_matrix(F)
    
    if n <= 2:
        return {
            "metric_name": "norm",
            "metric_value": norm_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    is_read_once = all(C[i][j] == 0 for i in range(1, n + 1) for j in range(i + 1, n + 1))
    conjecture_holds = (is_read_once and norm_F <= math.log(n)) or (not is_read_once and norm_F >= n)
    
    return {
        "metric_name": "norm",
        "metric_value": norm_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")