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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i + max(range(i, n), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    rank = sum(1 for row in matrix if any(row))
    return rank

def sipser_function(n, x):
    result = 0
    for i in range(n):
        result ^= (x >> i) & 1
    return result ^ (x & 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        rank_sum = 0
        
        for _ in range(30):
            x = random.getrandbits(n)
            truth_table = [[sipser_function(n, i) ^ sipser_function(n, j) for j in range(n)] for i in range(2**n)]
            
            rank = gaussian_elimination(truth_table)
            rank_sum += rank
            instances_tested += 1
        
        avg_rank = rank_sum / instances_tested
        conjecture_holds = avg_rank >= 2**(n/2)
        
        results.append({
            "metric_name": "average_rank",
            "metric_value": avg_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"avg_rank={avg_rank} < 2^{n/2}"
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    avg_rank = sum(r["metric_value"] for r in all_results) / len(all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=avg_rank < 2^{n/2} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")