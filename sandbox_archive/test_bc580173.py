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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate Tseitin encoding of an XOR gate
        for i in range(1, n+1):
            clause = [f'x{i}', f'y{i}']
            clauses.append(clause)
            
            clause = [-f'x{i}', f'y{i}']
            clauses.append(clause)
            
            clause = [-f'y{i}', f'z{i}']
            clauses.append(clause)
            
            clause = [-f'y{i}', -f'z{i}', f'w{i}']
            clauses.append(clause)
        
        # Final clause
        clause = [f'w{n}'] + variables
        clauses.append(clause)
        
        return clauses, variables
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            
            A[i], A[max_row] = A[max_row], A[i]
            
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
        
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        return A
    
    def resolution_width(clauses, variables):
        n = len(variables)
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        queue = list(clauses_set)
        seen = set(queue)
        
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 1:
                return len(clause1[0])
            
            for clause2 in clauses_set - {clause1}:
                for literal in clause1:
                    if -literal in clause2:
                        new_clause = tuple(sorted(set(clause1 + clause2) - {-literal, literal}))
                        if new_clause not in seen:
                            seen.add(new_clause)
                            queue.append(new_clause)
        
        return 0
    
    def minimal_generators(phi_G):
        n = len(phi_G[1])
        A = [[0] * (n+1) for _ in range(n+1)]
        
        for clause in phi_G[0]:
            literals = set(clause)
            for literal in literals:
                A[literal][literal] += 1
        
        A = gaussian_elimination(A)
        
        gen_count = sum(1 for row in A if any(row))
        return gen_count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            phi_G, variables = generate_tseitin_formula(n)
            gen_count = minimal_generators(phi_G)
            width = resolution_width(phi_G, variables)
            
            if gen_count < n // 2 or width > 10 * n**2:
                conjecture_holds = False
                counterexample = f"n={n}, gen_count={gen_count}, width={width}"
                break
            
            total_metric_value += width / gen_count
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "resolution_width/gen_count",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"]):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")