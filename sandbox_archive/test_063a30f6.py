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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf[0]) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        if propagate(literal):
            assignment[literal] = True
            if dpll(new_cnf, assignment):
                return True
            del assignment[literal]
        if propagate(-literal):
            assignment[-literal] = True
            if dpll(new_cnf, assignment):
                return True
            del assignment[-literal]
        return False
    
    def polynomial_from_cnf(cnf):
        n = len(cnf[0])
        f = [1] * (2**n)
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 + x[literal - 1])
                else:
                    term *= (1 - x[-literal - 1])
            f = [fi + ti for fi, ti in zip(f, term)]
        return f
    
    def tensor_product_coefficient_matrix(poly):
        m = len(poly)
        T = [[0] * (m - 1) for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                T[i][j] = poly[i] * poly[j]
        return T
    
    def rank(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        if rows == 0 or cols == 0:
            return 0
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return rank(matrix[:i] + matrix[i+1:])
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    x = [random.choice([-1, 1]) for _ in range(n)]
    f = polynomial_from_cnf(cnf)
    T = tensor_product_coefficient_matrix(f)
    r_f = rank(T)
    
    if r_f == 0:
        return {
            "metric_name": "log2(r(f))",
            "metric_value": float('-inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_length = dpll(cnf)
    if not proof_length:
        return {
            "metric_name": "log2(r(f))",
            "metric_value": float('-inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_r_f = math.log2(r_f)
    diff = abs(log2_r_f - proof_length)
    
    return {
        "metric_name": "log2(r(f))",
        "metric_value": log2_r_f,
        "instances_tested": 1,
        "conjecture_holds": diff <= 1,
        "counterexample": "" if diff <= 1 else f"diff={diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")