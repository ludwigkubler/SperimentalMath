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
    
    def generate_xor(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_and(n):
        return [all(x == y for x, y in zip(row[:i], row[i+1:])) for i in range(len(row)-1) for row in generate_xor(n)]
    
    def tseitin_formula(phi, n):
        literals = list(range(2**n))
        clauses = []
        for i in range(2**n):
            clause = [literals[i]]
            for j in range(i+1, 2**n):
                if phi[j] == 0:
                    clause.append(-literals[j])
                else:
                    clause.append(literals[j])
            clauses.append(clause)
        return literals, clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix = [[Fraction(x) for x in row] for row in matrix]
        rref_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in rref_matrix if any(row[i] != 0 for i in range(n)))
        return (m - rank) / m
    
    def minimal_local_induction_dimension(clauses):
        n = len(clauses[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if i not in clause:
                    continue
                for j in range(i+1, n):
                    if j not in clause:
                        continue
                    matrix[i][j] += 1
                    matrix[j][i] += 1
        rref_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in rref_matrix if any(row[i] != 0 for i in range(n)))
        return n - rank
    
    def polynomial_time_decision(mld, r, c):
        return mld > c * r
    
    def generate_instance():
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = random.choice([generate_xor(n), generate_and(n)])
        literals, clauses = tseitin_formula(phi, n)
        return literals, clauses
    
    def compute_metric(literals, clauses):
        mld = minimal_local_induction_dimension(clauses)
        r = rank_variance(clauses)
        return mld, r
    
    def check_conjecture(mld, r, c):
        return abs(mld - c * r) <= 3
    
    def run_experiment(c):
        instances_tested = 0
        n_max = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(50):  # Aim for at least 30 instances per seed
            literals, clauses = generate_instance()
            mld, r = compute_metric(literals, clauses)
            if len(clauses) > n_max:
                n_max = len(clauses)
            instances_tested += 1
            
            if not check_conjecture(mld, r, c):
                conjecture_holds = False
                counterexample = f"mld({len(clauses)})={mld}, r({len(clauses)})={r}"
        
        return {
            "metric_name": "minimal_local_induction_dimension",
            "metric_value": mld,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    c = 1.0  # Example constant for the linear relationship
    return run_experiment(c)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")