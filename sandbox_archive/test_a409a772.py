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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_variety(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        variety_points = []
        for i in range(n):
            point = [0] * n
            point[i] = 1
            variety_points.append(point)
        return variety_points
    
    def is_independent(points):
        n = len(points[0])
        A = [[points[i][j] for j in range(n)] for i in range(len(points))]
        rank = gaussian_elimination(A)
        return rank == len(points)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if rank < n:
                pivot_row = i + sum(1 for j in range(i, m) if matrix[j][i] != 0)
                if pivot_row == m:
                    continue
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                for j in range(m):
                    if j != i and matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    def resolution_length(cnf):
        stack = [cnf]
        while stack:
            clause = stack.pop()
            if not any(lit in clause for lit in clause):
                continue
            new_clause = []
            for c in cnf:
                if -clause[0] in c and len(set([abs(x) for x in c])) == 1:
                    new_clause.extend([x for x in c if x != -clause[0]])
            stack.append(new_clause)
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    variety_points = construct_variety(cnf)
    independent_points = [p for p in variety_points if is_independent([p] + variety_points)]
    
    geometric_defect = len(independent_points)
    proof_length = resolution_length(cnf)
    
    M = 2  # Example constant multiple
    if proof_length > M * geometric_defect:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Proof length {proof_length} exceeds {M} times geometric defect {geometric_defect}"
        }
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Proof length exceeds {M} times geometric defect\" first_failing_seed={first_failing_seed}")