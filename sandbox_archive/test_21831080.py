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
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        
        return x
    
    def spectral_radius(A):
        n = len(A)
        max_radius = 0
        for _ in range(10):  # Power iteration method
            v = [random.uniform(-1, 1) for _ in range(n)]
            v_norm = sum(x**2 for x in v)**0.5
            v = [x / v_norm for x in v]
            
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            Av_norm = sum(x**2 for x in Av)**0.5
            
            max_radius = max(max_radius, Av_norm)
        
        return max_radius
    
    def dpll(phi):
        n = len(phi)
        clauses = [set(clause) for clause in phi]
        literals = set(lit for clause in clauses for lit in clause)
        
        def dfs(model):
            if not clauses:
                return True
            literal = next(lit for lit in literals if all(lit not in m and -lit not in m for m in model))
            if literal is None:
                return False
            
            model.append(literal)
            if dfs(model):
                return True
            model.pop()
            
            model.append(-literal)
            if dfs(model):
                return True
            model.pop()
        
        return dfs([])
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_cnf(n)
        H_n = [[int(phi[i][j] == 'x' or phi[j][i] == 'x') for j in range(n)] for i in range(n)]
        
        sigma_max_H_n = spectral_radius(H_n)
        h_phi = dpll(phi)
        
        results.append({
            "n": n,
            "sigma_max_H_n": sigma_max_H_n,
            "h_phi": h_phi
        })
    
    correlation_sum = 0
    for i in range(len(n_values)):
        for j in range(i+1, len(n_values)):
            rho = (results[i]["sigma_max_H_n"] * results[j]["sigma_max_H_n"] +
                    results[i]["h_phi"] * results[j]["h_phi"]) / 2
            correlation_sum += abs(rho)
    
    mean_correlation = correlation_sum / (len(n_values) * (len(n_values) - 1))
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": mean_correlation > 0.7,
        "counterexample": "" if mean_correlation > 0.7 else "mean_correlation <= 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_correlation <= 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 80%")