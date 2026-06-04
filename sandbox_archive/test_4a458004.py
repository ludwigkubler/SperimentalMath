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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        resolvents = set()
        
        while True:
            new_resolvents = set()
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        lit = list(set(c1) ^ set(c2))[0]
                        resolvent = sorted([x for x in c1 + c2 if x != -lit and x != lit])
                        new_resolvents.add(tuple(resolvent))
            if not new_resolvents:
                break
            clauses.update(new_resolvents)
        
        return len(clauses) - len(cnf)
    
    def symplectic_leaves(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        B = [0] * (n + 1)
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    A[lit][n - lit] = 1
                else:
                    A[-lit][n - lit] = -1
        
        # Gaussian elimination to find the rank of matrix A
        rank = n
        for i in range(n):
            pivot = None
            for j in range(i, n + 1):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                rank -= 1
                continue
            
            for k in range(i, n + 1):
                A[i][k], A[pivot][k] = A[pivot][k], A[i][k]
            
            for j in range(n + 1):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        symplectic_leaves_count = symplectic_leaves(cnf)
        width = resolution_width(cnf)
        
        if symplectic_leaves_count > 3 * width:
            return {
                "metric_name": "symplectic_leaves_to_resolution_width_ratio",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, symplectic_leaves_count={symplectic_leaves_count}, width={width}"
            }
        
        results.append({
            "n": n,
            "symplectic_leaves_count": symplectic_leaves_count,
            "width": width
        })
    
    return {
        "metric_name": "symplectic_leaves_to_resolution_width_ratio",
        "metric_value": sum(result["symplectic_leaves_count"] / result["width"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(result["symplectic_leaves_count"] <= 3 * result["width"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, symplectic_leaves_count={results[0]['symplectic_leaves_count']}, width={results[0]['width']}\" first_failing_seed={first_failing_seed}")