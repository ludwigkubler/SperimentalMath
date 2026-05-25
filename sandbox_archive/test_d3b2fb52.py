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

def generate_kcnf(n, k):
    literals = [f'x{i+1}' for i in range(n)]
    cnf = []
    for _ in range(k):
        clause = random.sample(literals + [-l for l in literals], 3)
        cnf.append(clause)
    return cnf

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        rank += 1
        for j in range(m):
            if j == i:
                continue
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
    return rank

def resolve_clause(clause, assignment):
    return any(lit not in assignment or assignment[lit] == 1 for lit in clause)

def resolution_proof_width(cnf):
    queue = cnf[:]
    assignment = {}
    while queue:
        unit_clause = next((c for c in queue if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            assignment[literal] = 1
            queue.remove(unit_clause)
            queue.extend([c for c in cnf if resolve_clause(c, assignment)])
        else:
            break
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice(range(10, 41))
    k = max(1, n // 3)
    cnf = generate_kcnf(n, k)
    
    t_star = resolution_proof_width(cnf)
    if t_star == 0:
        return {
            "metric_name": "t_star",
            "metric_value": t_star,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_width_is_zero"
        }
    
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    r_F = matrix_rank(matrix)
    
    if r_F == 0:
        return {
            "metric_name": "r_F",
            "metric_value": r_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "matrix_rank_is_zero"
        }
    
    c = Fraction(1, 2)  # Example constant
    phi_n = c * log2(n)
    
    metric_value = (log2(t_star), r_F, phi_n)
    conjecture_holds = log2(t_star) <= r_F and r_F <= phi_n
    
    return {
        "metric_name": "t_star_r_F_phi_n",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def log2(x):
    if x <= 0:
        return float('-inf')
    return Fraction(math.log2(x)).limit_denominator()

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_F = sum(r['metric_value'][1] for r in results) / len(results)
    std_r_F = (sum((r['metric_value'][1] - mean_r_F)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_F} std={std_r_F} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"t_star_r_F_phi_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")