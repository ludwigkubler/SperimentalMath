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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(c > 0 for c in clause):  # Ensure at least one negative literal
                clause[random.randint(0, len(clause)-1)] *= -1
            clauses.append(tuple(sorted(clause)))
        return tuple(set(clauses))
    
    def diophantine_equation(cnf):
        n = max(abs(lit) for lit in cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    A[lit][lit] += 1
                else:
                    A[-lit][-lit] += 1
        
        for i in range(1, n + 1):
            b[i] = -sum(A[i][j] for j in range(1, n + 1) if j != i)
        
        return A, b
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            # Find the pivot
            max_row = i
            for r in range(i+1, n):
                if abs(A[r][i]) > abs(A[max_row][i]):
                    max_row = r
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            # Eliminate below the pivot
            for r in range(i+1, n):
                factor = A[r][i] / A[i][i]
                for c in range(i, n):
                    A[r][c] -= factor * A[i][c]
                b[r] -= factor * b[i]
        
        # Back-substitute
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        
        return x
    
    def resolution_width(cnf):
        queue = list(cnf)
        seen = set()
        while queue:
            clause = queue.pop(0)
            if clause in seen:
                continue
            seen.add(clause)
            
            for other_clause in cnf:
                if len(set(clause) & set(other_clause)) == 1:
                    new_clause = tuple(sorted(list(set(clause) ^ set(other_clause))))
                    if new_clause not in queue and new_clause not in seen:
                        queue.append(new_clause)
        
        return len(seen)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        A, b = diophantine_equation(cnf)
        x = gaussian_elimination(A, b)
        
        width = resolution_width(cnf)
        order = sum(abs(x[i]) for i in range(1, len(x)))
        
        results.append({
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": width >= n**2,
            "counterexample": "" if width >= n**2 else f"n={n}, width={width}"
        })
    
    return results[0]

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n_max']}, width={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")