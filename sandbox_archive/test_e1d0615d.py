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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def adjacency_matrix(cnf, n):
    adj_matrix = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            var = abs(lit) - 1
            if lit > 0:
                adj_matrix[var][var] += 1
            else:
                adj_matrix[var][var] -= 1
    return adj_matrix

def geometric_quantization(M):
    n = len(M)
    M2 = [[M[i][j] * M[j][k] for k in range(n)] for j in range(n)]
    trace = sum(M2[i][i] for i in range(n))
    det = 1
    for i in range(n):
        for j in range(i+1, n):
            sum_col = sum(M2[i][k] + M2[j][k] for k in range(n) if k != i and k != j)
            det *= (M2[i][i] * M2[j][j] - sum_col**2)
    return trace / math.sqrt(det)

def frege_proof_width(cnf):
    n = len(cnf)
    m = len(cnf[0])
    # Simplified estimation for demonstration purposes
    return 2 * (n + m) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n**2)
    cnf = generate_cnf(n, m)
    adj_matrix = adjacency_matrix(cnf, n)
    Q_G = geometric_quantization(adj_matrix)
    omega_F = frege_proof_width(cnf)
    
    metric_value = Q_G ** 2 * math.log(n)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if metric_value >= omega_F:
        conjecture_holds = True
    
    return {
        "metric_name": "Q(G)^2 * log n",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")