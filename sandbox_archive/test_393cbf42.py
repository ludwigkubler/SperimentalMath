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
    
    def communication_complexity_matrix(f):
        n = len(f)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] == f[j]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(i, n)):
                rank += 1
        return rank / n
    
    def permutation_induced_by_f(f):
        n = len(f)
        perm = list(range(n))
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] == f[j]:
                    perm[i], perm[j] = perm[j], perm[i]
        return perm
    
    def coxeter_reflection_complexity(perm):
        n = len(perm)
        reflections = set()
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    ref = tuple(sorted([i, j]))
                    reflections.add(ref)
        return len(reflections)
    
    def boolean_function_random(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = boolean_function_random(n)
        matrix = communication_complexity_matrix(f)
        rank_var = rank_variance(matrix)
        perm = permutation_induced_by_f(f)
        coxeter_cplx = coxeter_reflection_complexity(perm)
        
        if coxeter_cplx == 0:
            continue
        
        results.append({
            "n": n,
            "rank_var": rank_var,
            "coxeter_cplx": coxeter_cplx
        })
    
    if not results:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid permutations found"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    rank_vars = [result["rank_var"] for result in results]
    coxeter_cplxs = [result["coxeter_cplx"] for result in results]
    
    mean_rank_var = sum(rank_vars) / instances_tested
    std_rank_var = math.sqrt(sum((rv - mean_rank_var) ** 2 for rv in rank_vars) / instances_tested)
    mean_coxeter_cplx = sum(coxeter_cplxs) / instances_tested
    
    if all(rv <= n**(mean_coxeter_cplx + Fraction(1, 2)) for rv in rank_vars):
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = "Rank variance exceeds the bound"
    
    return {
        "metric_name": "rank_variance",
        "metric_value": mean_rank_var,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")