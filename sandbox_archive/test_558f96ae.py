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
    
    def generate_cnf(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice(variables) if random.random() < 0.5 else -random.choice(variables) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    def min_monomial_ideal(cnf):
        monomials = set()
        for clause in cnf:
            monomial = 1
            for var in clause:
                if var > 0:
                    monomial *= var
                else:
                    monomial //= -var
            monomials.add(monomial)
        return len(monomials)
    
    def schur_rank(cnf):
        n = max(abs(var) for var in cnf)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for clause in cnf:
            A = [[0] * n for _ in range(n)]
            for var in clause:
                if var > 0:
                    A[var-1][var-1] += 1
                else:
                    A[-var-1][-var-1] -= 1
            I = matrix_multiply(I, A)
        return rank(I)
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        pivot_row = 0
        for col in range(n):
            if all(matrix[row][col] == 0 for row in range(pivot_row, m)):
                continue
            matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
            for row in range(pivot_row + 1, m):
                factor = matrix[row][pivot_row] / matrix[pivot_row][pivot_row]
                for j in range(n):
                    matrix[row][j] -= factor * matrix[pivot_row][j]
            pivot_row += 1
        return pivot_row
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_ideal_size = min_monomial_ideal(cnf)
        schur_rank_value = schur_rank(cnf)
        results.append((n, min_ideal_size, schur_rank_value))
    
    if len(results) < 30:
        return {
            "metric_name": "schur_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n_values, min_ideal_sizes, schur_rank_values = zip(*results)
    mean_d = sum(schur_rank_values) / len(schur_rank_values)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in schur_rank_values) / len(schur_rank_values))
    
    correlation_coefficient = sum((n_values[i] - sum(n_values) / len(n_values)) * (schur_rank_values[i] - mean_d) for i in range(len(n_values))) / (len(n_values) * std_d * math.sqrt(sum((n_values[i] - sum(n_values) / len(n_values)) ** 2 for i in range(len(n_values)))))
    
    return {
        "metric_name": "schur_rank",
        "metric_value": mean_d,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8 and std_d <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_d = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")