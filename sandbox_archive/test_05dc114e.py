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
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            clauses.append(' '.join(clause) + ' 0')
        return '\n'.join(clauses)
    
    def h_norm(phi, n):
        # Convert CNF to Hodge matrix
        A = [[0] * (2*n) for _ in range(2*n)]
        for clause in phi.split('\n'):
            if not clause: continue
            literals = clause.strip().split()
            for lit in literals[:-1]:
                i, sign = int(lit[1:]) - 1, 1 if lit[0] == 'x' else -1
                A[i][sign * (i + n)] += 1
        
        # Compute Hodge matrix
        B = [[A[j][i] for i in range(2*n)] for j in range(2*n)]
        for k in range(2*n):
            for i in range(2*n):
                if i == k: continue
                factor = Fraction(B[i][k], B[k][k])
                for j in range(2*n):
                    B[i][j] -= factor * B[k][j]
        
        # Compute minimal Hodge norm
        h_n = 0
        for i in range(n, 2*n):
            for j in range(n, 2*n):
                if A[i][j] != 0:
                    h_n += abs(A[i][j])
        return h_n
    
    def resolution_width(phi):
        # Simplified version of resolution width calculation
        clauses = phi.split('\n')
        max_width = 0
        for clause in clauses:
            literals = clause.strip().split()
            if len(literals) > max_width:
                max_width = len(literals)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_cnf(n)
        h_n = h_norm(phi, n)
        w_phi = resolution_width(phi)
        results.append((h_n, w_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    h_norms = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_h_n = sum(h_norms) / len(h_norms)
    mean_w_phi = sum(widths) / len(widths)
    
    correlation_coefficient = 0
    if len(set(widths)) > 1:
        numerator = sum((h_norms[i] - mean_h_n) * (widths[i] - mean_w_phi) for i in range(len(h_norms)))
        denominator = math.sqrt(sum((h_norms[i] - mean_h_n)**2 for i in range(len(h_norms))) * sum((widths[i] - mean_w_phi)**2 for i in range(len(widths))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.9\" first_failing_seed={first_failing_seed}")