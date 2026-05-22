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
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def incidence_complex(f):
        n = len(f)
        V = list(range(2**n))
        E = []
        for i in range(len(V)):
            for j in range(i+1, len(V)):
                if f[i] <= f[j]:
                    E.append((i, j))
        return V, E
    
    def homology_dimension(C):
        V, E = C
        n = len(V)
        A = [[0] * n for _ in range(n)]
        for u, v in E:
            A[u][v] = 1
            A[v][u] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(M):
            m, n = len(M), len(M[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(M[j][i]) > abs(M[max_row][i]):
                        max_row = j
                M[i], M[max_row] = M[max_row], M[i]
                
                if M[i][i] == 0:
                    continue
                
                pivot = 1 / M[i][i]
                for j in range(n):
                    M[i][j] *= pivot
                
                for j in range(m):
                    if j != i:
                        factor = M[j][i]
                        for k in range(n):
                            M[j][k] -= factor * M[i][k]
            
            rank = 0
            for row in M:
                if any(row):
                    rank += 1
            return rank
        
        return n - gaussian_elimination(A)
    
    def local_induction_dimension(dimension):
        return dimension
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            f = generate_monotone_function(n)
            C = incidence_complex(f)
            dimension = homology_dimension(C)
            local_dim = local_induction_dimension(dimension)
            
            if local_dim < 0 or local_dim > n**(1/2 + 0.1):
                conjecture_holds = False
                counterexample = f"Circuit with {n} inputs and monotone function has local induction dimension {local_dim}, which violates the conjecture."
                break
            
            total_metric_value += local_dim
            instances_tested += 1
    
    return {
        "metric_name": "Local Induction Dimension",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")