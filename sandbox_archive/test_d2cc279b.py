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

# Constants
A = (1, 2, 3, 4, 5)
B = (1, 3, 5, 2, 4)

def compose(p1, p2):
    return tuple(p1[p2[i] - 1] for i in range(5))

def inverse(p):
    return tuple(p.index(i + 1) + 1 for i in range(5))

def perm_matrix(p):
    M = [[0] * 5 for _ in range(5)]
    for i, j in enumerate(p):
        M[i][j - 1] = 1
    return M

def frobenius_norm(M):
    sum_of_squares = sum(sum(row) ** 2 for row in M)
    return math.sqrt(sum_of_squares)

def barrington_and(n):
    if n == 2:
        return [(0, A, B), (1, B, A)]
    else:
        subprogram = barrington_and(n // 2)
        new_program = []
        for literal_index, p1, p2 in subprogram:
            new_program.append((literal_index * 4 + 0, compose(A, p1), compose(B, p2)))
            new_program.append((literal_index * 4 + 1, compose(A, p1), inverse(p2)))
            new_program.append((literal_index * 4 + 2, inverse(p1), compose(B, p2)))
            new_program.append((literal_index * 4 + 3, inverse(p1), inverse(p2)))
        return new_program

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 16, 32]
    results = []
    
    for n in n_values:
        L = n ** 2
        total_metric_value = 0
        
        for _ in range(30):
            x = tuple(random.randint(0, 1) for _ in range(n))
            π = [() for _ in range(L + 1)]
            π[0] = ()
            
            for i in range(1, L + 1):
                literal_index, p1, p2 = barrington_and(n)[i - 1]
                if x[literal_index] == 0:
                    π[i] = compose(p1, π[i - 1])
                else:
                    π[i] = compose(p2, π[i - 1])
            
            M_bar = sum(perm_matrix(p) for p in π[1:]) / L
            J = [[1/5] * 5 for _ in range(5)]
            metric_value = frobenius_norm([M_bar[i][j] - J[i][j] for i in range(5) for j in range(5)])
            total_metric_value += metric_value
        
        mean_metric_value = total_metric_value / 30
        results.append(mean_metric_value)
    
    D_bar_values = [results[i] / results[i + 1] for i in range(len(results) - 1)]
    slopes = [math.log2(D_bar_values[i]) for i in range(len(D_bar_values))]
    
    conjecture_holds = all(slope > 0.5 and slope < 3.0 for slope in slopes)
    counterexample = "" if conjecture_holds else "slope_outside_band"
    
    return {
        "metric_name": "Frobenius Fourier Defect",
        "metric_value": results[0],
        "instances_tested": len(results) * 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**k + 1 for k in range(2, 6)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if all(r[i] <= r[i + 1] for i in range(len(r) - 1)) and all(0.5 < math.log2(r[i] / r[i + 1]) < 3.0 for i in range(len(r) - 1))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")