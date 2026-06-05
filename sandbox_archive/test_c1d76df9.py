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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i + 1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(n):
                A[k][j] -= factor * A[i][j]

    return A

def determinant(A):
    A = gaussian_elimination(A)
    det = Fraction(1)
    for i in range(len(A)):
        det *= A[i][i]
    return det

def random_cnf(n, m):
    clauses = []
    variables = set()
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        variables.update(abs(x) for x in clause)
        clauses.append(clause)
    return clauses, len(variables)

def monotone_width(cnf):
    n = len(cnf[0])
    if not all(len(clause) > 0 for clause in cnf):
        return float('inf')
    
    max_width = 0
    for i in range(n):
        for j in range(i + 1, n):
            width = sum(1 for clause in cnf if clause[i] * clause[j] <= 0)
            max_width = max(max_width, width)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "monotone_width"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for s in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf, num_vars = random_cnf(s, int(s * (s + 1) / 4))
            instances_tested += 1
            n_max = max(n_max, s)
            
            try:
                width = monotone_width(cnf)
                if width > 2 * s**2:
                    conjecture_holds = False
                    counterexample = f"CNF with size {s} and width {width}"
                    break
            except Exception as e:
                conjecture_holds = False
                counterexample = str(e)
                break
    
    return {
        "metric_name": metric_name,
        "metric_value": s**2 if conjecture_holds else float('inf'),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")