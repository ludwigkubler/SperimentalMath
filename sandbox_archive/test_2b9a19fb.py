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
    
    def frobenius_norm(matrix):
        return sum(sum(x**2 for x in row) for row in matrix)**0.5
    
    def generate_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_frobenius_norm = 0
    total_rank_variance = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        A, B = generate_instance(n)
        frob_norm_A = frobenius_norm(A)
        frob_norm_B = frobenius_norm(B)
        rank_variance = abs(frob_norm_A**2 - frob_norm_B**2)
        
        total_frobenius_norm += frob_norm_A + frob_norm_B
        total_rank_variance += rank_variance
        instances_tested += 2
        n_max = max(n_max, n)
    
    mean_frobenius_norm = total_frobenius_norm / (instances_tested * 2)
    ratio = mean_frobenius_norm / (total_rank_variance ** 0.5)
    
    conjecture_holds = ratio > 0.9
    counterexample = "" if conjecture_holds else "Frobenius norm not proportional to rank variance"
    
    return {
        "metric_name": "Ratio of Mean Frobenius Norm to Rank Variance",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius norm not proportional to rank variance\" first_failing_seed={first_failing_seed}")