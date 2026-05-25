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
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(1, A[i][i])
        for j in range(i+1, cols):
            A[i][j] *= factor
        A[i][i] = 1
        
        # Eliminate above
        for r in range(rows):
            if r != i:
                factor = Fraction(A[r][i], A[i][i])
                for j in range(i, cols):
                    A[r][j] -= factor * A[i][j]
                A[r][i] = 0
    
    # Back substitution
    for i in range(rows-1, -1, -1):
        for j in range(i+1, rows):
            A[i][cols-1] -= A[j][cols-1] * A[i][j]
        A[i][cols-1] /= A[i][i]
    
    return [row[cols-1] for row in A]

def compute_rho(G):
    n = len(G)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                A[i][j] = Fraction(1, math.sqrt(2))
                A[j][i] = Fraction(1, math.sqrt(2))
    
    rank = len(gaussian_elimination(A))
    return rank

def brute_force_xor_circuit(n):
    # This is a very naive approach and will not work for large n
    if n == 1:
        return 1
    return 2 * brute_force_xor_circuit(n-1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    rho_G = compute_rho(G)
    C = brute_force_xor_circuit(n)
    
    metric_name = "XOR Circuit Size"
    metric_value = C
    instances_tested = 1
    conjecture_holds = abs(C - (1/rho_G)**2) <= 3
    counterexample = "" if conjecture_holds else f"rho(G)={rho_G}, C={C}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
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
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] != "")
        counterexample_desc = next(r["counterexample"] for r in results if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")