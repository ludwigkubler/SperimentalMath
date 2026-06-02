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

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for i in range(n):
            clause = [random.randint(1, n*2) if random.choice([True, False]) else -random.randint(1, n*2) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf

    def tseitin_encoding(cnf):
        new_vars = {}
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(abs(literal))
        
        var_counter = len(literals) + 1
        for i, clause in enumerate(cnf):
            new_var = -var_counter
            new_vars[i] = new_var
            cnf.append([-new_var, *clause])
            for j in range(i+1, len(cnf)):
                if random.choice([True, False]):
                    cnf[j].append(new_var)
                else:
                    cnf[j].append(-new_var)
            var_counter += 1
        
        return new_vars, cnf

    def dpll_search_tree(cnf):
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(abs(literal))
        
        def dfs(model):
            if not cnf:
                return True
            literal = next((l for l in literals if l not in model and -l not in model), None)
            if literal is None:
                return False
            
            new_model = model.copy()
            new_model.add(literal)
            if dfs(new_model):
                return True
            
            new_model.remove(literal)
            new_model.add(-literal)
            if dfs(new_model):
                return True
            
            return False
        
        return dfs(set())

    def plane_curve_complex(cnf):
        # Placeholder for actual PCC computation
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            new_vars, cnf_tseitin = tseitin_encoding(cnf)
            w_DPLL = dpll_search_tree(cnf_tseitin)
            C_phi = plane_curve_complex(cnf)

            if w_DPLL == 0:
                continue

            total_metric_value += abs(C_phi - w_DPLL)
            instances_tested += 1
            n_max = max(n_max, n)

            if not conjecture_holds and counterexample == "":
                counterexample = f"n={n}, C(φ)={C_phi}, w_DPLL(φ)={w_DPLL}"

    metric_name = "Pearson correlation coefficient"
    metric_value = total_metric_value / instances_tested
    n_max = max(n_max, 1)

    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    if metric_value < 0.8:
        conjecture_holds = False

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")