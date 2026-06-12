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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        cnf.append(clause)
    return cnf

def incidence_matrix(cnf):
    n = max(abs(lit) for lit in sum(cnf, []))
    m = len(cnf)
    M = [[0] * m for _ in range(n)]
    for i, clause in enumerate(cnf):
        for lit in clause:
            M[abs(lit) - 1][i] = 1 if lit > 0 else -1
    return M

def trace(M):
    n = len(M)
    return sum(M[i][i] for i in range(n))

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            if j != i:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    r_q_values = []
    w_c_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, int(n * (n - 1) / 4))
            M = incidence_matrix(cnf)
            r_q = trace(M)
            w_c = len(cnf)
            
            n_max = max(n_max, n)
            instances_tested += 1
            r_q_values.append(r_q)
            w_c_values.append(w_c)
    
    if not r_q_values or not w_c_values:
        return {
            "metric_name": "r_q vs w_c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_r_q = sum(r_q_values) / len(r_q_values)
    mean_w_c = sum(w_c_values) / len(w_c_values)
    variance_r_q = sum((x - mean_r_q) ** 2 for x in r_q_values) / len(r_q_values)
    variance_w_c = sum((x - mean_w_c) ** 2 for x in w_c_values) / len(w_c_values)
    
    cov = sum((r_q_values[i] - mean_r_q) * (w_c_values[i] - mean_w_c) for i in range(len(r_q_values))) / len(r_q_values)
    correlation_coefficient = Fraction(cov, math.sqrt(variance_r_q * variance_w_c))
    
    return {
        "metric_name": "r_q vs w_c",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")