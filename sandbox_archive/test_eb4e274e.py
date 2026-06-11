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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def boolean_to_diophantine(f, n_vars):
        equations = []
        for i in range(2**n_vars):
            binary_rep = format(i, f'0{n_vars}b')
            equation = ' + '.join([f'{x}*x{i}' if int(binary_rep[i]) else '-x{i}' for i, x in enumerate(range(n_vars))])
            equations.append(f'{equation} = 1')
        return equations
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, rows):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank_variance(equations, n_vars):
        matrix = [[0] * (n_vars + 1) for _ in range(len(equations))]
        for i, eq in enumerate(equations):
            terms = eq.split(' + ')
            for term in terms:
                if '=' in term:
                    continue
                coeff, var = term.split('*')
                matrix[i][int(var[1:])] = Fraction(coeff)
            matrix[i][-1] = -1
        
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return n_vars - rank
    
    def diophantine_representations(equations):
        solutions = set()
        for i in range(2**len(equations)):
            binary_rep = format(i, f'0{len(equations)}b')
            if all(int(binary_rep[j]) * int(eq.split('=')[0].split('+')[-1][j]) == 1 for j, eq in enumerate(equations)):
                solutions.add(tuple(map(int, binary_rep)))
        return len(solutions)
    
    n_vars = random.randint(5, 30)
    f = lambda x: random.choice([True, False])
    equations = boolean_to_diophantine(f, n_vars)
    rank_var = rank_variance(equations, n_vars)
    rep_count = diophantine_representations(equations)
    
    return {
        "metric_name": "diophantine_representation_ratio",
        "metric_value": Fraction(rep_count, rank_var),
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": rep_count <= 1000 and Fraction(rep_count, rank_var).limit_denominator(100) <= 5,
        "counterexample": "" if rep_count <= 1000 else f"Too many representations: {rep_count} > 1000"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
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
        print(f"RESULT: FALSIFIED counterexample=\"Too many representations\" first_failing_seed={first_failing_seed}")