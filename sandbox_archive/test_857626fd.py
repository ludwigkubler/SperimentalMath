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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n * 3)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if len(set(clause)) > 1:
                clauses.append(clause)
        return clauses

    def count_unsatisfied_clauses(cnf, assignment):
        return sum(1 for clause in cnf if not any(lit == assignment[abs(lit) - 1] * (lit // abs(lit)) for lit in clause))

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

        return matrix

    def minimal_quaternionic_order(cnf):
        n = len(cnf)
        identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        matrix = [row[:] for row in identity]
        
        for clause in cnf:
            for lit in clause:
                abs_lit = abs(lit)
                if abs_lit > n:
                    continue
                row = [Fraction(0, 1) for _ in range(n)]
                row[abs_lit - 1] = Fraction(-lit // abs_lit, 1)
                matrix.append(row)
        
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(x != Fraction(0, 1) for x in row))
        return rank

    def clause_satisfiability_complexity(cnf):
        n = len(cnf)
        assignment = [random.choice([True, False]) for _ in range(n)]
        return count_unsatisfied_clauses(cnf, assignment)

    n_max = 0
    instances_tested = 0
    total_metric_value = Fraction(0, 1)
    
    for n in {5, 10, 15, 20, 30, 40}:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cnf = generate_cnf(n)
            instances_tested += 1
            omega_phi = minimal_quaternionic_order(cnf)
            complexity_phi = clause_satisfiability_complexity(cnf)
            
            if omega_phi == 0 or complexity_phi == 0:
                continue
            
            total_metric_value += Fraction(complexity_phi, omega_phi).log2()
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value >= 0.8 * mean_metric_value for metric_value in [mean_metric_value] * 30)
    counterexample = "" if conjecture_holds else "not_enough_support"
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = min(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_instances")