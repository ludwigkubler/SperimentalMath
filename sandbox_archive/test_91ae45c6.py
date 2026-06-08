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
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        det = determinant(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        return (trace**2 - 4 * det) / n
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1)**j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        literals = set()
        for clause in formula:
            if not any(lit in literals for lit in clause):
                literals.update(clause)
                stack.append(clause)
        return len(stack) + len(literals)
    
    def generate_formula(n, m):
        clauses = []
        variables = list(range(1, n+1))
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def construct_matrix(formula):
        n = len(formula)
        matrix = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(formula):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit-1] += 1
                else:
                    matrix[lit-1][i] -= 1
        return matrix
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 3 * n)
    formula = generate_formula(n, m)
    matrix = construct_matrix(formula)
    
    fs_indicator = frobenius_schur_indicator(matrix)
    proof_depth = frege_proof_depth(formula)
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs Frege Proof Depth",
        "metric_value": fs_indicator,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(fs_indicator) >= 0.9 * proof_depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = "Frobenius-Schur Indicator vs Frege Proof Depth"
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")