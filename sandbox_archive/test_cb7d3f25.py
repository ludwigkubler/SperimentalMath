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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def boolean_function_to_matrix(f, n):
    matrix = []
    for i in range(2**n):
        row = [f[i >> j & 1] for j in range(n)]
        matrix.append(row)
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if matrix[j][i] == 1:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(m):
            if j != rank and matrix[j][i] == 1:
                for k in range(n):
                    matrix[j][k] ^= matrix[rank][k]
        rank += 1
    return rank

def entropic_complexity(f, n):
    counts = [f.count(i) for i in range(2)]
    total = len(f)
    entropy = 0
    for count in counts:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matrix = boolean_function_to_matrix(f, n)
        rank_quot = gaussian_elimination(matrix)
        entropy_complexity_val = entropic_complexity(f, n)
        
        if entropy_complexity_val == 0:
            continue
        
        results.append({
            "n": n,
            "rank_quot": rank_quot,
            "entropy_complexity": entropy_complexity_val
        })
    
    if not results:
        return {
            "metric_name": "Rank_quot vs Entropy_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    max_n = max(result["n"] for result in results)
    min_n = min(result["n"] for result in results)
    if max_n - min_n < 4:
        return {
            "metric_name": "Rank_quot vs Entropy_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Sub-asymptotic n"
        }
    
    rank_quots = [result["rank_quot"] for result in results]
    entropy_complexities = [result["entropy_complexity"] for result in results]
    ratio_mean = sum(rank / entropy for rank, entropy in zip(rank_quots, entropy_complexities)) / len(results)
    ratio_std = math.sqrt(sum((rank / entropy - ratio_mean) ** 2 for rank, entropy in zip(rank_quots, entropy_complexities)) / len(results))
    
    return {
        "metric_name": "Rank_quot vs Entropy_complexity",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "conjecture_holds": ratio_std < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")