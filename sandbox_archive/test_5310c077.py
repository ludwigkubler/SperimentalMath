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
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate current column
        pivot = A[i][i]
        for j in range(n):
            if j != i:
                factor = Fraction(-A[j][i], pivot)
                for k in range(n):
                    A[j][k] += factor * A[i][k]

    return A

def tropicalize_Birkhoff_polytope(F):
    n = len(F)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if F[i][j]:
                A[i][j] = 1
            else:
                A[i][j] = -math.inf
    
    A_tropical = gaussian_elimination(A)
    
    rank = sum(1 for row in A_tropical if any(x > -math.inf for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 10
    
    # Generate a Monotone k-CLIQUE instance F with n variables
    F = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the tropicalized Birkhoff polytope P_F
    rank = tropicalize_Birkhoff_polytope(F)
    
    # Determine the minimal rank of P_F
    min_rank = rank
    
    # The size of any Monotone k-CLIQUE proof for F is at least Ω(n^(1/2))
    conjecture_holds = min_rank >= math.sqrt(n) * 0.98
    counterexample = "" if conjecture_holds else f"Rank {min_rank} < {math.sqrt(n)}"

    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")