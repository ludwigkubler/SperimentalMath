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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def matrix_rank(A):
    rank = 0
    A_rref = gaussian_elimination(A)
    for row in A_rref:
        if any(row):
            rank += 1
    return rank

def dpll_search_tree_height(formula):
    if formula == "True" or formula == "False":
        return 0
    elif "and" not in formula and "or" not in formula:
        return 1
    else:
        subformulas = []
        if "and" in formula:
            subformulas.extend(formula.split("and"))
        elif "or" in formula:
            subformulas.extend(formula.split("or"))
        
        max_height = 0
        for subformula in subformulas:
            height = dpll_search_tree_height(subformula.strip())
            if height > max_height:
                max_height = height
        
        return 1 + max_height

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    
    mrank_values = []
    h_phi_values = []
    
    for _ in range(instances_tested):
        num_vars = random.randint(5, 40)
        formula = ""
        for _ in range(num_vars):
            var = f"x{random.randint(1, num_vars)}"
            if random.choice([True, False]):
                formula += f"{var} and "
            else:
                formula += f"{var} or "
        formula = formula.rstrip(" and ").rstrip(" or ")
        
        mrank_phi = matrix_rank([[1 if var in clause else 0 for var in set(formula.split())] for clause in formula.split() if "and" in clause])
        h_phi = dpll_search_tree_height(formula)
        
        mrank_values.append(mrank_phi)
        h_phi_values.append(h_phi)
    
    correlation_coefficient = sum((mrank - sum(mrank_values) / len(mrank_values)) * (h_phi - sum(h_phi_values) / len(h_phi_values)) for mrank, h_phi in zip(mrank_values, h_phi_values)) / ((sum((mrank - sum(mrank_values) / len(mrank_values)) ** 2 for mrank in mrank_values) * sum((h_phi - sum(h_phi_values) / len(h_phi_values)) ** 2 for h_phi in h_phi_values)) ** 0.5)
    p_value = 1.0  # Placeholder, actual calculation would be complex
    
    conjecture_holds = correlation_coefficient >= 0.95 and p_value <= 0.01
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> p_value=<{}>".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))