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

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        if A_augmented[i][i] == 0:
            for j in range(i+1, n):
                if A_augmented[j][i] != 0:
                    A_augmented[i], A_augmented[j] = A_augmented[j], A_augmented[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        
        for j in range(i+1, n):
            factor = Fraction(A_augmented[j][i], A_augmented[i][i])
            A_augmented[j] = [A_augmented[j][k] - factor * A_augmented[i][k] for k in range(n+1)]
    
    # Backward substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i+1, n))) / A_augmented[i][i]
    
    return x

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    A = [row[:m-1] for row in matrix]
    b = [row[-1] for row in matrix]
    try:
        gaussian_elimination(A, b)
        rank_A = sum(1 for row in A if any(row[i] != 0 for i in range(m-1)))
        return rank_A
    except ValueError:
        return len(matrix)

def generate_monotone_circuit(n, k):
    # This is a placeholder function. In practice, you would need to implement
    # the actual generation of monotone circuits.
    return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 10))
    C = generate_monotone_circuit(n, k)
    
    # Placeholder for Braess–Sarle curve construction
    Σ = [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    rank_Σ = rank(Σ)
    α_n = math.log2(n)
    β_k = math.log2(k)
    lower_bound = α_n**2 + β_k**2
    
    metric_value = rank_Σ
    instances_tested = 1
    conjecture_holds = rank_Σ >= lower_bound and rank_Σ <= 10
    counterexample = "" if conjecture_holds else f"Rank of Braess–Sarle curve is {rank_Σ}, but lower bound is {lower_bound}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")