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
        n = len(A)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate non-pivot elements
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] -= factor * A[i][k]
    
    def characteristic_polynomial(A):
        n = len(A)
        x = Fraction('x')
        det = Fraction(1)
        for i in range(n):
            det *= (A[i][i] - x)
        return det
    
    def min_root_separation(poly):
        roots = []
        for coeff, exp in poly.items():
            if coeff != 0:
                root = Fraction(coeff) ** (-Fraction(1, exp))
                roots.append(root)
        return min(abs(r1 - r2) for r1, r2 in itertools.combinations(roots, 2))
    
    def generate_random_cnf(size):
        cnf = []
        for _ in range(size):
            clause = [random.randint(-size, size) for _ in range(random.randint(1, size))]
            cnf.append(clause)
        return cnf
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_random_cnf(n)
    
    A = [[0] * (n + 1) for _ in range(n)]
    B = [[0] * (n + 1) for _ in range(n)]
    
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                row, col = divmod(literal - 1, n)
                A[row][col] += 1
                B[row][col] -= 1
            else:
                row, col = divmod(-literal - 1, n)
                A[row][n] += 1
                B[row][col] += 1
    
    gaussian_elimination(A)
    char_poly = characteristic_polynomial(A)
    
    min_separation = min_root_separation(char_poly)
    log_size = math.log(n)
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": min_separation <= log_size + 3,
        "counterexample": "" if min_separation <= log_size + 3 else f"n={n}, min_separation={min_separation}, log_size+3={log_size+3}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, min_separation={results[0]['metric_value']}, log_size+3={math.log(results[0]['instances_tested']) + 3}\" first_failing_seed={first_failing_seed}")