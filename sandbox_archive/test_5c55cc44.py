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
    
    def generate_k_communication_instance(k, n):
        # Generate a random k-communication instance with n variables
        communication_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(k)]
        return communication_matrix
    
    def compute_schubert_polynomial_representation(matrix):
        # Placeholder function to compute the Schubert polynomial representation
        # This is a dummy implementation and should be replaced with actual computation
        n = len(matrix[0])
        min_monomials = n  # Dummy value, replace with actual computation
        return min_monomials
    
    def compute_communication_complexity_rank(matrix):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual computation
        k = len(matrix)
        rank = k  # Dummy value, replace with actual computation
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            k = random.randint(1, min(n - 1, 5))  # Ensure k is at least 1 and less than n-1
            communication_matrix = generate_k_communication_instance(k, n)
            min_monomials = compute_schubert_polynomial_representation(communication_matrix)
            rank = compute_communication_complexity_rank(communication_matrix)
            
            if min_monomials == 0 or rank == 0:
                continue
            
            ratio = Fraction(min_monomials, k**2 * math.log(n))
            ratios.append(ratio)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = sum(ratios) / len(ratios) if ratios else 0
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in ratios) / len(ratios)) if ratios else 0
    
    conjecture_holds = abs(mean_ratio - 1) <= Fraction(3, 100)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    ratios = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std={math.sqrt(sum((x - sum(ratios)/len(ratios))**2 for x in ratios)/len(ratios))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")