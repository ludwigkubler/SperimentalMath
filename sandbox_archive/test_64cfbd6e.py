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
            literals = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(literals)
        return clauses
    
    def is_satisfiable(clauses):
        assignments = {i: random.choice([True, False]) for i in range(1, n + 1)}
        for clause in clauses:
            if not any(assignments[abs(lit)] == (lit > 0) for lit in clause):
                return False
        return True
    
    def sos_moment_matrix(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                count = sum(all(lit in assignment for lit in clause) for clause in clauses for assignment in [i, j])
                matrix[i][j] = count
                matrix[j][i] = count
        return matrix
    
    def newton_basis(n):
        basis = []
        for i in range(1, n + 1):
            coeff = math.factorial(i)
            for j in range(i):
                coeff //= (math.factorial(j) * math.factorial(i - j))
            basis.append(coeff)
        return basis
    
    def schur_positivity(matrix, basis):
        coeffs = [0] * len(basis)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    index = i + j
                    if index < len(coeffs):
                        coeffs[index] += matrix[i][j]
        first_non_zero_index = next((i for i, coeff in enumerate(coeffs) if coeff != 0), None)
        if first_non_zero_index is not None:
            return all(coeffs[i] <= coeffs[first_non_zero_index] for i in range(first_non_zero_index + 1))
        return False
    
    n = random.randint(5, 40)
    clauses = generate_3sat_instance(n)
    matrix = sos_moment_matrix(clauses)
    basis = newton_basis(n)
    
    if is_satisfiable(clauses):
        conjecture_holds = schur_positivity(matrix, basis)
    else:
        conjecture_holds = not schur_positivity(matrix, basis)
    
    return {
        "metric_name": "schur_positivity",
        "metric_value": 1 if conjecture_holds else 0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "unsatisfiable instance"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='unsatisfiable instance' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")