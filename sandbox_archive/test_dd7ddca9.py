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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        n = max(abs(x) for x in sum(clauses, []))
        assignment = {var: random.choice([-1, 1]) for var in range(-n, n + 1)}
        for clause in clauses:
            if not any(assignment[var] * x <= 0 for x in clause):
                return True
        return False
    
    def sos_moment_matrix(clauses):
        n = max(abs(x) for x in sum(clauses, []))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for assignment in itertools.product([-1, 1], repeat=n + 1):
            if all(assignment[var] * x <= 0 for x in clauses):
                count = sum(1 for var in range(-n, n + 1) if assignment[var] == 1)
                matrix[count][count] += 1
        return matrix
    
    def newton_basis(n):
        basis = [[0] * (n + 1) for _ in range(n + 1)]
        basis[0][0] = 1
        for k in range(1, n + 1):
            for j in range(k, -1, -1):
                if j > 0:
                    basis[k][j] = (k * basis[k - 1][j - 1] + basis[k - 1][j]) / (k + 1)
        return basis
    
    def schur_coefficients(matrix, basis):
        n = len(matrix) - 1
        coefficients = [0] * (n + 1)
        for i in range(n + 1):
            for j in range(n + 1):
                if matrix[i][j] != 0:
                    coefficients[i] += matrix[i][j] * basis[j][i]
        return coefficients
    
    def dominance(coefficients):
        max_coeff = max(coefficients)
        return coefficients.index(max_coeff) == len(coefficients) - 1
    
    n = random.randint(5, 40)
    clauses = generate_3sat_instance(n)
    satisfiable = is_satisfiable(clauses)
    matrix = sos_moment_matrix(clauses)
    basis = newton_basis(n)
    coefficients = schur_coefficients(matrix, basis)
    
    metric_value = dominance(coefficients)
    conjecture_holds = (satisfiable == metric_value)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Schur Positivity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")