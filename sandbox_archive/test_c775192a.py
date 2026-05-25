# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                if i == k:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = gaussian_elimination(matrix)
    rank = sum(1 for row in rref if any(row))
    return rank

def clause_indicator_polynomial(instance):
    n = len(instance)
    poly = [0] * (2 ** n)
    for assignment in range(2 ** n):
        valid = True
        for clause in instance:
            if all(poly[assignment ^ 1 << i] == 0 for i, var in enumerate(clause)):
                valid = False
                break
        if valid:
            poly[assignment] += 1
    return [x % 2 for x in poly]

def dpll(instance):
    def backtrack(assignment):
        if all(any(poly[assignment ^ 1 << i] == 0 for i, var in enumerate(clause)) for clause in instance):
            return True
        if any(all(poly[assignment ^ 1 << i] == 0 for i, var in enumerate(clause)) for clause in instance):
            return False
        var = next(i for i in range(n) if assignment & (1 << i) == 0)
        for value in [0, 1]:
            new_assignment = assignment ^ (1 << var)
            poly[var] += value
            if backtrack(new_assignment):
                return True
            poly[var] -= value
        return False
    
    n = len(instance)
    poly = [0] * n
    return backtrack(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = [[random.randint(0, n - 1) for _ in range(random.randint(2, 3))] for _ in range(n)]
    
    poly = clause_indicator_polynomial(instance)
    proof_length = dpll(instance)
    
    if proof_length == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length is 0, cannot compute rank"
        }
    
    rho = rank([[poly[assignment ^ 1 << i] for i in range(n)] for assignment in range(2 ** n)])
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30 * 1000 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")