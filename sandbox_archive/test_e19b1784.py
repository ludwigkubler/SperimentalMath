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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            det *= matrix[i][i]
            if det == 0:
                return 0
            for j in range(rows):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return det
    
    def zeta_rank(cnf):
        n = len(cnf)
        variables = set()
        for clause in cnf:
            variables.update(clause)
        n_vars = len(variables)
        
        # Construct a lattice from the CNF formula
        lattice = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if any(var in clause for clause in cnf if var in {i, j} and -var not in clause):
                    lattice[i][j] = 1
                else:
                    lattice[i][j] = 0
        
        # Compute the determinant of the lattice matrix
        det = determinant(lattice)
        
        return abs(det)
    
    def dpll(cnf):
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        def solve(model):
            if not any(clause for clause in cnf if all(var not in model and -var not in model for var in clause)):
                return True
            unsatisfied_clauses = [clause for clause in cnf if not any(var in model or -var in model for var in clause)]
            if not unsatisfied_clauses:
                return False
            
            literal = next(iter(unsatisfied_clauses[0]))
            for value in (True, False):
                new_model = model.copy()
                new_model[literal] = value
                if solve(new_model):
                    return True
            return False
        
        return len(solve({}))

    def generate_cnf(n, m):
        cnf = []
        variables = list(range(1, n + 1))
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            cnf.append(clause)
        return cnf
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = int(n * random.uniform(0.5, 2))
            cnf = generate_cnf(n, m)
            depth = dpll(cnf)
            zeta_rk = zeta_rank(cnf)
            
            if depth == -1 or zeta_rk == 0:
                continue
            
            instances_tested += 1
            metric_values.append(zeta_rk / depth)
    
    if not metric_values:
        return {
            "metric_name": "zeta_rank_over_depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, range(len(metric_values)))) / (len(metric_values) * std_dev * math.sqrt(sum((y - mean) ** 2 for y in range(len(metric_values)))))
    
    return {
        "metric_name": "zeta_rank_over_depth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean) ** 2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results) and support_fraction >= 0.8:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")