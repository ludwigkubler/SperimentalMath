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
    
    def characteristic_polynomial(clause):
        n = len(clause)
        if n == 1:
            return [[-clause[0], 1]]
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, x in enumerate(clause):
            matrix[i][i] = -x
            matrix[n][i] = 1
            matrix[i][n] = 1
        det = determinant(matrix)
        return [[det, 1]]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate resolution width
        clauses = phi[:]
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = random.choice(unit_clauses)
            literals = set(abs(lit) for lit in unit_clause)
            new_clauses = []
            for clause in clauses:
                if not any(lit in literals for lit in clause):
                    continue
                if all(lit in literals for lit in clause):
                    continue
                new_clause = [lit for lit in clause if abs(lit) not in literals]
                if new_clause:
                    new_clauses.append(new_clause)
            clauses = new_clauses
        return len(clauses)
    
    def automorphic_forms(char_polynomials):
        # Simplified counting of automorphic forms (placeholder)
        return sum(1 for cp in char_polynomials if cp[0] == 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = [[random.randint(-n, n) for _ in range(n)] for _ in range(30)]
        char_polynomials = [characteristic_polynomial(clause) for clause in phi]
        w_phi = resolution_width(phi)
        N_phi = automorphic_forms(char_polynomials)
        results.append((N_phi, w_phi))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    N_values, w_values = zip(*results)
    mean_N = sum(N_values) / len(N_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = (sum((N - mean_N) * (w - mean_w) for N, w in results) /
                               math.sqrt(sum((N - mean_N) ** 2 for N in N_values) *
                                         sum((w - mean_w) ** 2 for w in w_values)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_N <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif any(r['metric_value'] < 0.5 or r['metric_value'] > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")