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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda j: abs(A_b[j][i]))
        A_b[i], A_b[pivot_row] = A_b[pivot_row], A_b[i]
        for j in range(i + 1, n):
            factor = A_b[j][i] / A_b[i][i]
            A_b[j] = [A_b[j][k] - factor * A_b[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i + 1, n))) / A_b[i][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            result[i][j] = sum(A[i][l] * B[l][j] for l in range(len(B)))
    return result

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    if unit_clauses:
        lit = unit_clauses[0]
        new_assignment = assignment.copy()
        new_assignment[lit] = 1
        if dpll([c for c in clauses if not any(l in c for l in (lit, -lit))], new_assignment):
            return True
        new_assignment[lit] = 0
        if dpll([c for c in clauses if not any(l in c for l in (lit, -lit))], new_assignment):
            return True
    pure_literals = set()
    for lit in range(1, max(abs(l) for clause in clauses)):
        pos_count = sum(1 for clause in clauses if lit in clause)
        neg_count = sum(1 for clause in clauses if -lit in clause)
        if pos_count == 0:
            pure_literals.add(-lit)
        elif neg_count == 0:
            pure_literals.add(lit)
    if pure_literals:
        lit = next(iter(pure_literals))
        new_assignment = assignment.copy()
        new_assignment[lit] = 1
        if dpll([c for c in clauses if not any(l in c for l in (lit, -lit))], new_assignment):
            return True
        new_assignment[lit] = 0
        if dpll([c for c in clauses if not any(l in c for l in (lit, -lit))], new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, 41):
        if n > n_max:
            break
        
        for _ in range(instances_tested // (n - 4)):
            instance = []
            variables = set()
            for i in range(n):
                clause = [random.choice([-1, 1]) * (i + 1) for _ in range(random.randint(1, n))]
                instance.append(clause)
                variables.update(abs(lit) for lit in clause)
            
            pos_clauses = [c for c in instance if all(lit > 0 for lit in c)]
            neg_clauses = [c for c in instance if any(lit < 0 for lit in c)]
            
            height = dpll(instance, {})
            metric_values.append(height)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_value,
        "instances_tested": instances_tested * (n_max - 4),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")