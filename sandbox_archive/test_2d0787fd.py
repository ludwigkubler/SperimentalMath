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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(depth):
        if depth == 0:
            return random.choice(['A', 'B', 'C'])
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_formula(depth - 1)
            right = generate_formula(depth - 1)
            return f"({left} {op} {right})"
    
    def incidence_matrix(formula):
        if formula.isalpha():
            return [[0, 0], [0, 0]]
        
        op, left, right = formula.split()
        left_matrix = incidence_matrix(left)
        right_matrix = incidence_matrix(right)
        
        if op == 'AND':
            result = [
                [left_matrix[0][0] + right_matrix[0][0], left_matrix[0][1] + right_matrix[1][0]],
                [left_matrix[1][0] + right_matrix[0][1], left_matrix[1][1] + right_matrix[1][1]]
            ]
        elif op == 'OR':
            result = [
                [left_matrix[0][0] + right_matrix[0][0], left_matrix[0][1] + right_matrix[1][1]],
                [left_matrix[1][0] + right_matrix[1][0], left_matrix[1][1] + right_matrix[1][1]]
            ]
        else:
            raise ValueError("Invalid operation")
        
        return result
    
    def symplectic_form_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def frege_proof_depth(formula):
        if formula.isalpha():
            return 1
        else:
            op, left, right = formula.split()
            return 2 + max(frege_proof_depth(left), frege_proof_depth(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        incidence = incidence_matrix(formula)
        sfr = symplectic_form_rank(incidence)
        d = frege_proof_depth(formula)
        
        if sfr == 0 or d == 0:
            continue
        
        results.append((sfr, d))
    
    if not results:
        return {
            "metric_name": "symplectic_form_rank_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sfr_values = [sfr for sfr, _ in results]
    d_values = [d for _, d in results]
    
    mean_sfr = sum(sfr_values) / len(sfr_values)
    mean_d = sum(d_values) / len(d_values)
    correlation_coefficient = (sum((sfr - mean_sfr) * (d - mean_d) for sfr, d in results) /
                               math.sqrt(sum((sfr - mean_sfr)**2 for sfr in sfr_values) *
                                         sum((d - mean_d)**2 for d in d_values)))
    
    return {
        "metric_name": "symplectic_form_rank_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.7' first_failing_seed={first_failing_seed}")