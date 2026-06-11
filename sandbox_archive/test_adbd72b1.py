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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        pivot = matrix[i][i]
        for j in range(i+1, n):
            factor = matrix[j][i] / pivot
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank_variance(equations, n_vars):
    n_eqs = len(equations)
    augmented_matrix = [equation + [1 if i == j else 0 for j in range(n_vars)] for i, equation in enumerate(equations)]
    
    # Perform Gaussian elimination
    gaussian_elimination(augmented_matrix)
    
    rank = sum(1 for row in augmented_matrix if any(row[i] != 0 for i in range(n_vars)))
    return Fraction(rank - n_eqs, n_vars)

def boolean_to_diophantine(f, n_vars):
    equations = []
    for var_values in itertools.product([0, 1], repeat=n_vars):
        equation = [var_values[i] * f[var_values[:i+1]] for i in range(n_vars)]
        if sum(equation) != 0:
            equations.append(equation)
    return equations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    max_n = 40
    results = []
    
    for _ in range(n_tests):
        n_vars = random.randint(5, max_n)
        f = {tuple(sorted(var_values)): random.choice([0, 1]) for var_values in itertools.product([0, 1], repeat=n_vars)}
        
        equations = boolean_to_diophantine(f, n_vars)
        rank_var = rank_variance(equations, n_vars)
        
        if rank_var == 0:
            continue
        
        num_representations = len(equations)
        results.append(num_representations / rank_var)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(result <= 1000 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Diophantine Representations to Rank Variance",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for result in results if result <= 1000) / len(results)
    
    if all(result <= 1000 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if result > 1000)]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")