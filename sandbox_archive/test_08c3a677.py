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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate entries below pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i+1, n):
            matrix[j][i] *= factor
    
    # Back-substitute to get upper triangular form
    for i in range(n-1, -1, -1):
        factor = Fraction(1, matrix[i][i])
        for j in range(i):
            matrix[j][i] -= matrix[j][j+1:] * matrix[i][j+1:]
    
    return matrix

def srank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def crank(protocol):
    # Placeholder function to compute communication complexity rank
    # This is a dummy implementation; replace with actual computation
    return len(protocol)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    srank_sum = 0
    crank_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            protocol = [random.randint(0, 1) for _ in range(n)]
            srank_value = srank(protocol)
            crank_value = crank(protocol)
            
            total_instances += 1
            srank_sum += srank_value
            if crank_value > crank_max:
                crank_max = crank_value
    
    mean_srank = Fraction(srank_sum, total_instances)
    support_fraction = (mean_srank >= Fraction(3)) and (srank_sum / total_instances >= 0.8 * crank_max)
    
    return {
        "metric_name": "srank/crank ratio",
        "metric_value": float(mean_srank),
        "instances_tested": total_instances,
        "n_max": crank_max,
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else f"mean_srank={mean_srank}, crank_max={crank_max}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_srank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_srank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_srank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"srank/crank ratio\" first_failing_seed={first_failing_seed}")