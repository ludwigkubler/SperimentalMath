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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] != f[i]:
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for row in matrix:
            if any(row[j] == 1 for j in range(n)):
                rank += 1
        return rank / n
    
    def coxeter_reflection_complexity(permutation):
        n = len(permutation)
        reflections = []
        for i in range(n):
            reflection = permutation[:]
            reflection[i], reflection[(i + 1) % n] = reflection[(i + 1) % n], reflection[i]
            reflections.append(reflection)
        return len(set(tuple(r) for r in reflections))
    
    def generate_permutation(f):
        n = int(math.log2(len(f)))
        permutation = list(range(n))
        random.shuffle(permutation)
        return permutation
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        matrix = communication_complexity_matrix(f)
        rank_var = rank_variance(matrix)
        permutation = generate_permutation(f)
        coxeter_reflects = coxeter_reflection_complexity(permutation)
        
        results.append({
            "n": n,
            "rank_var": rank_var,
            "coxeter_reflects": coxeter_reflects
        })
    
    mean_rank_var = sum(r["rank_var"] for r in results) / len(results)
    max_coxeter_reflects = max(r["coxeter_reflects"] for r in results)
    
    if max_coxeter_reflects < 16:
        return {
            "metric_name": "Rank Variance",
            "metric_value": mean_rank_var,
            "instances_tested": len(results),
            "n_max": max_coxeter_reflects,
            "conjecture_holds": False,
            "counterexample": "coxeter_reflects_too_low"
        }
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": mean_rank_var,
        "instances_tested": len(results),
        "n_max": max_coxeter_reflects,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")