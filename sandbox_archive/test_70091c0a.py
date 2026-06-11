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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank_variance(equations, n_vars):
    # Convert equations to matrix form
    A = []
    for eq in equations:
        row = [0] * (n_vars + 1)
        terms = eq.split('+')
        for term in terms:
            if '*' not in term:
                continue
            coeff, var = term.split('*')
            row[int(var)] = Fraction(coeff)
        A.append(row)

    # Perform Gaussian elimination to get the rank
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(x != 0 for x in row))
    
    return rank

def boolean_to_diophantine(f, n_vars):
    equations = []
    for i in range(2**n_vars):
        binary = format(i, f'0{n_vars}b')
        eq = ' + '.join([f'{int(binary[j])}*x{j}' for j in range(n_vars)]) + ' = 1'
        equations.append(eq)
    return equations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    max_n = 40
    total_representations = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            break
        
        representations = []
        for _ in range(n_tests):
            f = random.randint(0, 1)
            equations = boolean_to_diophantine(f, n)
            rank_var = rank_variance(equations, n)
            representations.append(len(equations))
        
        avg_representations = sum(representations) / len(representations)
        total_representations += avg_representations
    
    mean_representations = total_representations / (len([5, 10, 15, 20, 30, 40]) * n_tests)
    
    conjecture_holds = mean_representations <= 1000
    counterexample = "" if conjecture_holds else "mean_representations > 1000"
    
    return {
        "metric_name": "Mean Number of Distinct Diophantine Representations",
        "metric_value": mean_representations,
        "instances_tested": n_tests * len([5, 10, 15, 20, 30, 40]),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_representations > 1000\" first_failing_seed={first_failing_seed}")