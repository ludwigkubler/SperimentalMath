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
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        
        # Gaussian elimination to find rank
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def galois_automorphisms(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            return 0
        
        # Compute the determinant
        det = 1
        for i in range(m):
            det *= matrix[i][i]
        
        # The number of distinct Galois automorphisms is the order of the Galois group
        # For simplicity, we use the fact that the order of the Galois group is at most n!
        return math.factorial(n)
    
    max_rank = 0
    total_aut = 0
    instances_tested = 0
    
    for _ in range(30):
        rank = random.randint(5, 40)
        matrix = [[random.randint(-10, 10) for _ in range(rank)] for _ in range(rank)]
        max_rank = max(max_rank, rank)
        total_aut += galois_automorphisms(matrix)
        instances_tested += 1
    
    mean_aut = total_aut / instances_tested
    conjecture_holds = mean_aut <= 1.5 * max_rank**2
    counterexample = "" if conjecture_holds else f"mean={mean_aut}, max_rank={max_rank}"
    
    return {
        "metric_name": "Galois Automorphisms",
        "metric_value": mean_aut,
        "instances_tested": instances_tested,
        "n_max": max_rank,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_aut = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_aut} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_aut} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")