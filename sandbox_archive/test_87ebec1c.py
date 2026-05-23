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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            return None  # Singular matrix, no unique solution
        for j in range(i + 1, n):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(n - 1):
        clauses.append([variables[i], variables[i + 1]])
    clauses.append([-variables[-2], variables[-1]])
    clauses.append([variables[0]])
    return clauses

def resolution_length(clauses):
    # Simplified version of DPLL algorithm to estimate resolution length
    stack = []
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        clauses = [c for c in clauses if literal not in c and -literal not in c]
        stack.append(literal)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = tseitin_formula(n)
    rank = gaussian_elimination(G)
    if rank is None:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Singular matrix"
        }
    
    resolution_len = resolution_length(G)
    ratio = resolution_len / (2 ** rank)
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results if r["instances_tested"] > 0):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")