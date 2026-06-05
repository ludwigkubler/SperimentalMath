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
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(lit == 0 for lit in clause):
            continue
        cnf.append(clause)
    return cnf

def evaluate_cnf(cnf, assignment):
    return any(all(assignment[abs(lit) - 1] * lit > 0 for lit in clause) for clause in cnf)

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if rank < m:
            pivot_row = i + sum(1 for j in range(i, n) if matrix[j][i] != 0)
            if pivot_row == n:
                continue
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                matrix[i][j] /= matrix[i][i]
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    for j in range(m):
                        matrix[k][j] -= matrix[i][j] * matrix[k][i]
            rank += 1
    return rank

def clause_indicator_polynomial(cnf):
    n = len(cnf[0])
    poly = [0] * (2 ** n)
    for assignment in itertools.product([-1, 1], repeat=n):
        if evaluate_cnf(cnf, assignment):
            index = sum(assignment[i] * (2 ** i) for i in range(n))
            poly[index] += 1
    return [x % 2 for x in poly]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(10, n * 2)  # Ensure at least 10 clauses
        cnf = generate_cnf(n, m)
        poly = clause_indicator_polynomial(cnf)
        
        if not poly:
            return {
                "metric_name": "m_lir",
                "metric_value": 0,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "empty_poly"
            }
        
        m_lir = gaussian_elimination([[poly[i ^ (1 << j)] for j in range(n)] for i in range(2 ** n)])
        r_gamma = len(cnf)  # Communication complexity rank is the number of clauses
        
        results.append({
            "n": n,
            "m_lir": m_lir,
            "r_gamma": r_gamma
        })
    
    if not results:
        return {
            "metric_name": "m_lir",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    m_lir_values = [res["m_lir"] for res in results]
    r_gamma_values = [res["r_gamma"] for res in results]
    correlation = sum((m_lir_values[i] - mean(m_lir_values)) * (r_gamma_values[i] - mean(r_gamma_values)) for i in range(len(results))) / math.sqrt(sum((m_lir_values[i] - mean(m_lir_values)) ** 2 for i in range(len(results)))) / math.sqrt(sum((r_gamma_values[i] - mean(r_gamma_values)) ** 2 for i in range(len(results))))
    
    return {
        "metric_name": "m_lir",
        "metric_value": mean(m_lir_values),
        "instances_tested": len(results) * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.9,
        "counterexample": "" if correlation >= 0.9 else f"correlation={correlation:.2f}"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    m_lir_values = [res["metric_value"] for res in results if res["conjecture_holds"]]
    support_fraction = len(m_lir_values) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any(not res["conjecture_holds"] and res["counterexample"] != "" for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"] and res["counterexample"] != "")
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'] and res['counterexample'] != '')]}"
    else:
        RESULT = "INCONCLUSIVE budget_exceeded n_tested=30"
    
    print(f"RESULT: {RESULT} mean={mean(m_lir_values):.2f} std={math.sqrt(sum((x - mean(m_lir_values)) ** 2 for x in m_lir_values) / len(m_lir_values)):.2f} support_fraction={support_fraction:.2f}")