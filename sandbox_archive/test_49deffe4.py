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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = [[f[i ^ (1 << j)] for j in range(n)] for i in range(2**n)]
        return M
    
    def rank_variance(M):
        n = len(M)
        I = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                pivot = A[i][i]
                if pivot == 0:
                    continue
                
                for j in range(n):
                    A[i][j] /= pivot
                
                for j in range(m):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
            
            return A
        
        A = gaussian_elimination(M)
        
        rank = sum(1 for row in A if any(row))
        return (n - rank) / n
    
    def count_automorphic_forms(M):
        n = len(M)
        forms = set()
        
        def is_automorphic(f, M):
            for i in range(n):
                for j in range(n):
                    if f[i] != M[i][j]:
                        return False
            return True
        
        for perm in itertools.permutations(range(n)):
            form = [M[i][perm[i]] for i in range(n)]
            if is_automorphic(form, M):
                forms.add(tuple(form))
        
        return len(forms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f)
        rho_f = rank_variance(M)
        aut_forms = count_automorphic_forms(M)
        
        results.append({
            "n": n,
            "f": f,
            "M": M,
            "rho_f": rho_f,
            "aut_forms": aut_forms
        })
    
    correlation_values = [r["aut_forms"] / r["rho_f"] for r in results if r["rho_f"] != 0]
    
    if not correlation_values:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "No valid rho(f) found"
        }
    
    mean_corr = sum(correlation_values) / len(correlation_values)
    std_corr = math.sqrt(sum((x - mean_corr)**2 for x in correlation_values) / len(correlation_values))
    
    return {
        "metric_name": "Correlation",
        "metric_value": mean_corr,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": mean_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 89))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not enough valid rho(f)\" first_failing_seed={first_failing_seed}")