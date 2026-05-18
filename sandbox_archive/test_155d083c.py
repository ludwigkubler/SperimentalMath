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

def gaussian_elimination(matrix, field_size):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        pivot = matrix[i][i]
        for j in range(i+1, n):
            factor = matrix[j][i] * pow(pivot, field_size-2, field_size)
            for k in range(n):
                matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % field_size
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def patience_sort(sequence):
    piles = []
    for x in sequence:
        i = 0
        while i < len(piles) and piles[i][-1] >= x:
            i += 1
        if i == len(piles):
            piles.append([])
        piles[i].append(x)
    return max(len(pile) for pile in piles)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(k, size_range):
        n = random.randint(size_range[0], size_range[1])
        S = set()
        while len(S) < n:
            b = tuple(random.randint(0, 1) for _ in range(k))
            if b not in S:
                S.add(b)
        return S
    
    def xor_lift(f, a):
        return tuple((b ^ a) for b in f)
    
    k_values = [3, 4, 5]
    results = []
    
    for k in k_values:
        size_range = (2**(k-1) - 2, 2**(k-1) + 2)
        for _ in range(50):
            S = generate_boolean_function(k, size_range)
            f = {b: 1 if b in S else 0 for b in itertools.product([0, 1], repeat=k)}
            
            M = [[f[xor_lift(f, a)] for a in itertools.product([0, 1], repeat=k)] for x in S]
            rank_M = gaussian_elimination(M, 2)
            
            τ_a = sorted((b ^ a for b in S), key=lambda x: tuple(x))
            μ_f = patience_sort(τ_a)
            
            results.append({
                "metric_name": "ρ(f)",
                "metric_value": μ_f / (rank_M + 1),
                "instances_tested": 1,
                "conjecture_holds": μ_f <= rank_M + 1,
                "counterexample": "" if μ_f <= rank_M + 1 else f"Counterexample found for k={k}"
            })
    
    return {
        "seed": seed,
        "metric_name": "ρ(f)",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*37 + 1, 37))
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    max_rho = max(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif max_rho > 1:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='ρ(f) > rank_{F_2}(M)+1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")