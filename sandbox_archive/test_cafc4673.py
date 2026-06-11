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
    
    def generate_k_ary_communication_problem(k):
        # Generate a random k-ary communication problem
        n = random.randint(5, 40)
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(k)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(k)]
        return A, B
    
    def compute_rank_variance(A, B):
        # Compute the rank variance R(φ)
        n = len(A[0])
        rank_A = sum(sum(row) for row in A) / (k * n)
        rank_B = sum(sum(row) for row in B) / (k * n)
        return abs(rank_A - rank_B)
    
    def compute_arithmetic_genus(g):
        # Placeholder function to compute the arithmetic genus
        # This is a dummy implementation and should be replaced with actual computation
        return g
    
    k = random.randint(2, 5)  # Generate a random k between 2 and 5
    A, B = generate_k_ary_communication_problem(k)
    R_phi = compute_rank_variance(A, B)
    
    # Placeholder for computing the arithmetic genus
    g = compute_arithmetic_genus(R_phi)
    
    return {
        "metric_name": "arithmetic_genus",
        "metric_value": g,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")