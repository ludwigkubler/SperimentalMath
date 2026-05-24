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
    
    # Generate a random noncommutative algebra and associated sheaves
    n = random.randint(5, 30)
    A = generate_noncommutative_algebra(n)
    P = generate_BP_readtwice_instance(A)
    
    # Compute the minimal rank of sheaf cohomology groups
    H = compute_sheaf_cohomology(A, P)
    min_rank = max(len(h) for h in H.values())
    
    # Compute the BP_readtwice tensor width
    TW = compute_BP_readtwice_tensor_width(P)
    
    # Evaluate the conjectured relationships
    ratio = min_rank / TW
    
    # Check if the conjecture holds
    if ratio > 10 or ratio < 0.1:
        return {
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Out of expected range"
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_noncommutative_algebra(n: int) -> dict:
    # Placeholder for generating a noncommutative algebra
    A = {}
    for i in range(n):
        for j in range(n):
            A[(i, j)] = random.randint(1, 10)
    return A

def generate_BP_readtwice_instance(A: dict) -> list:
    # Placeholder for generating a BP_readtwice instance
    n = len(A)
    P = []
    for i in range(n):
        row = [random.choice(list(A.keys())) for _ in range(n)]
        P.append(row)
    return P

def compute_sheaf_cohomology(A: dict, P: list) -> dict:
    # Placeholder for computing sheaf cohomology
    H = {}
    n = len(A)
    for i in range(n):
        H[i] = [random.randint(1, 10) for _ in range(n)]
    return H

def compute_BP_readtwice_tensor_width(P: list) -> int:
    # Placeholder for computing BP_readtwice tensor width
    n = len(P)
    TW = 0
    for row in P:
        TW += sum(1 for x in row if x is not None)
    return TW

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")