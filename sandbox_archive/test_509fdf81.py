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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def boolean_tensor_product(x):
    n = len(x)
    tp = [1]
    for i in range(n):
        new_tp = []
        for term in tp:
            new_tp.append(term * x[i])
            new_tp.append(term * (1 - x[i]))
        tp = new_tp
    return tp

def valuation(tp):
    return math.log2(len(tp))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        total_valuation = 0
        
        while len(results) < 30:
            x = [random.randint(0, 1) for _ in range(n)]
            tp = boolean_tensor_product(x)
            rank_value = rank([[i] for i in x])
            valuation_value = valuation(tp)
            
            if rank_value == 0 and valuation_value == 0:
                continue
            
            instances_tested += 1
            total_rank += rank_value
            total_valuation += valuation_value
            
            results.append({
                "n": n,
                "x": x,
                "rank": rank_value,
                "valuation": valuation_value
            })
            
            if len(results) >= 30:
                break
        
        mean_rank = total_rank / instances_tested
        mean_valuation = total_valuation / instances_tested
        ratio = abs(mean_rank - mean_valuation)
        
        metric_name = "Rank vs Valuation Ratio"
        metric_value = ratio
        conjecture_holds = ratio <= 10 * math.log2(n)  # Θ(V(TP(x))) ≈ n log2(n)
        counterexample = "" if conjecture_holds else f"n={n}, rank={mean_rank}, valuation={mean_valuation}"
        
        results.append({
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[-1]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = f"n={results[0]['n']}, rank={results[0]['rank']}, valuation={results[0]['valuation']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")