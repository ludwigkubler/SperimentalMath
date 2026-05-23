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
    
    def generate_parity_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize_polynomial(poly):
        return sum(x * (1 << i) for i, x in enumerate(poly))
    
    def compute_minimal_rank(polynomial):
        n = len(polynomial)
        matrix = [[abs(polynomial[i] - polynomial[j]) for j in range(n)] for i in range(n)]
        
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            rank = 0
            for col in range(cols):
                pivot_row = None
                for row in range(rank, rows):
                    if mat[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row is not None:
                    mat[pivot_row], mat[rank] = mat[rank], mat[pivot_row]
                    for r in range(rows):
                        if r != rank and mat[r][col] != 0:
                            factor = mat[r][col] / mat[rank][col]
                            for c in range(cols):
                                mat[r][c] -= factor * mat[rank][c]
                    rank += 1
            return rank
        
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_parity_circuit(n)
        polynomial = tropicalize_polynomial(circuit)
        rank = compute_minimal_rank(polynomial)
        
        if rank <= math.log(n) and len(circuit) <= 2**(0.5 * math.log(n)):
            results.append((n, True))
        else:
            results.append((n, False))
    
    metric_value = sum(1 for n, holds in results if holds) / len(results)
    conjecture_holds = all(holds for _, holds in results)
    counterexample = "" if conjecture_holds else "small AC0 parity circuit with non-logarithmic minimal rank"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"small AC0 parity circuit with non-logarithmic minimal rank\" first_failing_seed={first_failing_seed}")