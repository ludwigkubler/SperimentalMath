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
    
    def generate_cnf(n: int, num_clauses: int):
        cnf = []
        for _ in range(num_clauses):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def characteristic_polynomial(cnf):
        n = len(cnf[0])
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in cnf:
            literal = abs(clause[0]) - 1
            if clause[0] > 0:
                matrix[literal][literal] += Fraction(1)
            else:
                matrix[literal][literal] -= Fraction(1)
        return matrix
    
    def tropicalize(matrix):
        n = len(matrix)
        for row in range(n):
            for col in range(n):
                if matrix[row][col] < 0:
                    matrix[row][col] = -matrix[row][col]
        return matrix
    
    def compute_index(tropical_matrix):
        n = len(tropical_matrix)
        for i in range(n):
            tropical_matrix[i][i] += Fraction(1)
        return sum(sum(row) for row in tropical_matrix)

    def solve(lits_true, lits_false, cls):
        if not lits_true and not lits_false:
            return True
        lit = lits_true[0]
        new_lits_true = [l for l in lits_true if l != lit] + [other_lit for other_lit in lits_false if other_lit == -lit]
        new_lits_false = [l for l in lits_false if l != lit] + [other_lit for other_lit in lits_true if other_lit == -lit]
        return solve(new_lits_true, cls) or solve(new_lits_false, cls)
    
    def is_satisfiable(cnf):
        literals = set(abs(lit) for clause in cnf for lit in clause)
        return solve(list(literals), [], cnf)

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            num_clauses = random.randint(n // 2, n)
            cnf = generate_cnf(n, num_clauses)
            results.append(cnf)

    indices = [compute_index(tropicalize(characteristic_polynomial(cnf))) for cnf in results]
    clause_counts = [len(cnf) for cnf in results]

    if not indices or not clause_counts:
        return {
            "metric_name": "Index_G",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation = sum((indices[i] - mean_indices) * (clause_counts[i] - mean_clauses) for i in range(len(indices))) / len(indices)
    mean_indices = sum(indices) / len(indices)
    mean_clauses = sum(clause_counts) / len(clause_counts)

    return {
        "metric_name": "Index_G",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation < 0.8,
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

    if all(result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")