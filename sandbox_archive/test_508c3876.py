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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_satisfiability_time(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function length")
        
        def evaluate(x):
            return f[x]
        
        def dfs(current, path):
            if current == n:
                if evaluate(path):
                    return 1
                return 0
            count = 0
            for bit in [0, 1]:
                count += dfs(current + 1, path * 2 + bit)
            return count
        
        return dfs(0, 0)
    
    def permutation_group_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function length")
        
        # Find all satisfying assignments
        satisfying_assignments = [i for i in range(2**n) if f[i] == 1]
        
        # Generate the permutation group
        G = set()
        for perm in itertools.permutations(satisfying_assignments):
            G.add(tuple(perm))
        
        return len(G)
    
    def gaussian_elimination(A, b):
        n = len(A)
        m = len(b)
        if n != m:
            raise ValueError("Incompatible dimensions")
        
        A_b = [row + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                    max_row = j
            
            A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
            
            pivot = A_b[i][i]
            for j in range(i+1, m):
                A_b[i][j] /= pivot
            A_b[i][m] /= pivot
            
            for j in range(n):
                if j != i:
                    factor = A_b[j][i]
                    for k in range(m):
                        A_b[j][k] -= factor * A_b[i][k]
        
        return [row[-1] for row in A_b]
    
    def solve_linear_system(A, b):
        try:
            return gaussian_elimination(A, b)
        except Exception as e:
            return None
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        t_f = circuit_satisfiability_time(f)
        G_f = permutation_group_size(f)
        
        if t_f == 0 or G_f == 0:
            continue
        
        # Solve the linear system to find generators
        A = []
        b = []
        for i in range(2**n):
            if f[i] == 1:
                row = [i >> j & 1 for j in range(n)]
                A.append(row)
                b.append(1)
        
        generators = solve_linear_system(A, b)
        if generators is None or len(generators) != G_f:
            continue
        
        results.append({
            "n": n,
            "G_f": G_f,
            "t_f": t_f
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance size"
        }
    
    G_f_values = [result["G_f"] for result in results]
    t_f_values = [result["t_f"]**0.5 for result in results]
    
    n_tested = len(results)
    mean_G_f = sum(G_f_values) / n_tested
    mean_t_f = sum(t_f_values) / n_tested
    
    if n_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": n_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    correlation = sum((G_f - mean_G_f) * (t_f - mean_t_f) for G_f, t_f in zip(G_f_values, t_f_values)) / (n_tested * math.sqrt(sum((G_f - mean_G_f)**2 for G_f in G_f_values)) * math.sqrt(sum((t_f - mean_t_f)**2 for t_f in t_f_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")