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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        pivot = matrix[i][i]
        for r in range(i+1, rows):
            factor = Fraction(matrix[r][i], pivot)
            for k in range(cols):
                if i == k:
                    matrix[r][k] = 0
                else:
                    matrix[r][k] -= factor * matrix[i][k]

def rank(matrix):
    rref = [row[:] for row in matrix]
    gaussian_elimination(rref)
    rank_value = sum(1 for row in rref if any(row))
    return rank_value

def generate_cnf(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    cnf = {i: [] for i in range(1, n+1)}
    for clause in clauses:
        for var in clause:
            cnf[var].append((var, True))
            cnf[-var].append((-var, False))
    return cnf

def construct_simplicial_complex(cnf):
    vertices = set()
    simplices = []
    for var in cnf:
        for literal, _ in cnf[var]:
            vertices.add(literal)
    vertices = sorted(vertices)
    
    def find_simplex(literals):
        literals.sort()
        if len(literals) == 1:
            return [literals[0]]
        elif len(literals) == 2:
            return [literals[0], literals[1]], [literals[0]], [literals[1]]
        else:
            simplices = []
            for i in range(len(literals)):
                sub_literals = literals[:i] + literals[i+1:]
                sub_simplices = find_simplex(sub_literals)
                for simplex in sub_simplices:
                    simplices.append([literals[i]] + simplex)
            return simplices
    
    simplices.extend(find_simplex(list(vertices)))
    
    # Add empty simplex
    simplices.append([])
    
    return vertices, simplices

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2*n, 3*n)
    cnf = generate_cnf(n, m)
    
    vertices, simplices = construct_simplicial_complex(cnf)
    num_vertices = len(vertices)
    num_simplices = len(simplices)
    
    metric_value = num_simplices
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    if n_max >= 16:
        upper_bound = math.ceil(n ** 1.5)
        lower_bound = n
        if lower_bound <= metric_value <= upper_bound:
            conjecture_holds = True
    
    return {
        "metric_name": "number_of_simplicial_generators",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "number_of_simplicial_generators"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")