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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(-matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for j in range(rows):
                if i != j:
                    factor = Fraction(matrix[j][i])
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        
        if rows == 1:
            return matrix[0][0]
        
        det = Fraction(0)
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** (j % 2)
            det += sign * matrix[0][j] * determinant(submatrix)
        
        return det

    def hodge_norm(matrix):
        return abs(determinant(gaussian_elimination(matrix)))

    def resolution_width(cnf):
        stack = []
        assignment = {}
        for clause in cnf:
            satisfied = False
            for literal in clause:
                if literal in assignment and assignment[literal] == (literal > 0):
                    satisfied = True
                    break
            if not satisfied:
                new_assignment = {var: True for var in set(abs(lit) for lit in clause)}
                stack.append((new_assignment, cnf))
        return len(stack)

    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            literals = [random.randint(-n, -1), random.randint(1, n)]
            if all(lit not in clause for clause in cnf):
                cnf.append(literals)
        return cnf

    n = 40
    cnf = generate_cnf(n)
    
    hodge_norm_value = hodge_norm([[1 if var in assignment and assignment[var] else -1 for var in range(1, n + 1)] for assignment in [{}]])
    width_value = resolution_width(cnf)
    
    return {
        "metric_name": "Hodge Norm vs Resolution Width",
        "metric_value": hodge_norm_value * width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if hodge_norm_value == 0 else True,
        "counterexample": "" if hodge_norm_value != 0 else "Hodge Norm is zero"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'] != 'mapping_undefined')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")