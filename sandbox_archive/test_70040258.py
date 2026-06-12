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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll_width(instance):
    n = len(instance)
    clauses = [set(clause) for clause in instance]
    variables = set()
    for clause in clauses:
        variables.update(clause)
    
    def is_satisfiable(model):
        for clause in clauses:
            if not any(var in model and model[var] == 1 for var in clause):
                return False
        return True
    
    def dpll(model, literals):
        if len(literals) == 0:
            return is_satisfiable(model)
        
        literal = literals[0]
        pos_literal = literal
        neg_literal = -literal
        
        model[pos_literal] = 1
        if dpll(model, literals[1:]):
            return True
        
        del model[pos_literal]
        model[neg_literal] = 0
        if dpll(model, literals[1:]):
            return True
        
        del model[neg_literal]
        return False
    
    max_width = 0
    for literal in variables:
        model = {}
        if dpll(model, [literal]):
            width = len(model)
            if width > max_width:
                max_width = width
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(n)]
        
        m_phi = len(instance) ** 3
        w_phi = dpll_width(instance)
        
        if m_phi < n_max**3 or m_phi > n_max**(3/2):
            continue
        
        metric_values.append(m_phi / (n_max ** 3))
    
    if not metric_values:
        return {
            "metric_name": "m(φ) / n^3",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_shv = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean_shv) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    return {
        "metric_name": "m(φ) / n^3",
        "metric_value": mean_shv,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_shv >= 1 and mean_shv <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_shv = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = (sum((r["metric_value"] - mean_shv) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_shv} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_shv} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")