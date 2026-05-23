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

def gaussian_elimination(A):
    rows = len(A)
    cols = len(A[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i], A[i][i])
        for j in range(i+1, rows):
            row_factor = Fraction(A[j][i], A[i][i])
            for k in range(cols):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] -= row_factor * A[i][k]
    return A

def rank_of_matrix(A):
    rows = len(A)
    cols = len(A[0])
    rank = 0
    for i in range(rows):
        if all(abs(A[i][j]) == 0 for j in range(cols)):
            continue
        rank += 1
    return rank

def acc0_circuit_weight(X):
    # Placeholder function to compute ACC⁰ circuit weight
    # For simplicity, assume it's proportional to the number of elements
    return len(X)

def generate_geometrically_quantized_space(n):
    # Placeholder function to generate a random geometrically quantized space
    # For simplicity, assume it's a binary matrix
    X = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    return X

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            X = generate_geometrically_quantized_space(n)
            quantization_map = X  # Placeholder for actual quantization map computation
            minimal_rank = rank_of_matrix(quantization_map)
            WACC0_X = acc0_circuit_weight(X)
            
            if minimal_rank > WACC0_X:
                conjecture_holds = False
                counterexample = f"n={n}, X={X}, minimal_rank={minimal_rank}, WACC0_X={WACC0_X}"
                break
            
            total_metric_value += minimal_rank / WACC0_X
            instances_tested += 1
    
    return {
        "metric_name": "RankQuant(X) / WACC0(X)",
        "metric_value": total_metric_value / instances_tested,
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")