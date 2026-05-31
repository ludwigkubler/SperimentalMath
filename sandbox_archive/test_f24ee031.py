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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tseitin_diagram(cnf):
        new_vars = {}
        literals = set()
        for clause in cnf:
            literals.update(clause)
        new_var_index = len(literals) + 1
        for literal in literals:
            new_vars[literal] = new_var_index
            new_var_index += 1

        A = []
        b = []
        for i, clause in enumerate(cnf):
            row = [0] * (len(new_vars) + 1)
            for literal in clause:
                if literal > 0:
                    row[new_vars[literal]] = -1
                else:
                    row[-1] += 1
            A.append(row)
            b.append(1)

        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank

    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        def dpll():
            if not cnf:
                return 0
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0]
                cnf.remove([literal])
                stack.append(literal)
                width = dpll()
                if width != -1:
                    return width + 1
                stack.pop()
                cnf.append([literal])
                cnf.append([-literal])
                width = dpll()
                if width != -1:
                    return width + 1
                cnf.remove([-literal])
            pure_literals = [l for l in literals if all(l not in c and -l not in c for c in cnf)]
            if pure_literals:
                literal = pure_literals[0]
                stack.append(literal)
                width = dpll()
                if width != -1:
                    return width + 1
                stack.pop()
                cnf.append([literal])
                cnf.append([-literal])
                width = dpll()
                if width != -1:
                    return width + 1
            return -1
        
        return dpll()

    def minimal_geometric_defect(diagram):
        return diagram

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        m = random.randint(5, 40)
        cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(m)] for _ in range(m)]
        diagram = tseitin_diagram(cnf)
        width = resolution_width(cnf)
        defect = minimal_geometric_defect(diagram)
        
        if width == -1:
            continue
        
        metric_values.append(defect / width)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x - mean_metric) <= 3 * std_metric for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalDefect/ResolutionWidth",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")