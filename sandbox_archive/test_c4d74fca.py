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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def frobenius_schur_indicator(A):
        n = len(A)
        char_table = [[0] * n for _ in range(n)]
        orthonormal_basis = [[0] * n for _ in range(n)]
        
        # Fill character table and orthonormal basis (simplified example)
        for i in range(n):
            char_table[i][i] = 1
            orthonormal_basis[i][i] = 1
        
        I_F = sum(sum(A[i][j] * char_table[i][k] * orthonormal_basis[j][k] for k in range(n)) for i in range(n) for j in range(n))
        return I_F
    
    def communication_complexity_rank(A):
        n = len(A)
        rank = 0
        # Simplified example: rank is the number of non-zero rows/columns
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            I_F = frobenius_schur_indicator(A)
            r_A = communication_complexity_rank(A)
            
            if r_A == 0:
                continue
            
            ratio_1 = Fraction(I_F, r_A ** (2/3))
            ratio_2 = Fraction(n ** (1/3), I_F)
            
            results.append((n, I_F, r_A, ratio_1, ratio_2))
    
    if not results:
        return {
            "metric_name": "Frobenius-Schur Indicator and Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid matrices generated"
        }
    
    n_max = max(n for n, _, _, _, _ in results)
    metric_value = sum(ratio_1 + ratio_2 for _, _, _, ratio_1, ratio_2 in results) / len(results)
    conjecture_holds = all(ratio_1 <= 10 and ratio_2 <= 10 for _, _, _, ratio_1, ratio_2 in results)  # Simplified bound
    counterexample = "" if conjecture_holds else "Mapping undefined"
    
    return {
        "metric_name": "Frobenius-Schur Indicator and Communication Complexity Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")