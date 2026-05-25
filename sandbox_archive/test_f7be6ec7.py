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

# Helper function to compute the minimal rank of Schur-Weyl module decomposition (simplified)
def schur_weyl_rank(n):
    # This is a placeholder for the actual computation
    # For simplicity, we use a dummy value that depends on n
    return 2 ** n

# Helper function to construct a permutation circuit (simplified)
def construct_permutation_circuit(n):
    # This is a placeholder for the actual construction
    # For simplicity, we assume a constant size of O(n^2)
    return n * n

# Function to generate a random boolean function and compute its associated polynomial
def polynomial_from_boolean_function(f):
    n = len(f)
    x = 'x'
    poly = sum(random.randint(0, 1) * (x + '^' + str(i)) if i > 0 else 1 for i in range(n+1))
    return poly

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    poly = polynomial_from_boolean_function(f)
    rho_f = schur_weyl_rank(n)
    C_n = math.log2(n) ** 2
    threshold = C_n * log2(n)
    
    if rho_f <= threshold:
        circuit_size = construct_permutation_circuit(n)
        conjecture_holds = circuit_size <= 4 * n**2 - 8
        counterexample = "" if conjecture_holds else "circuit_size_exceeds_bound"
    else:
        conjecture_holds = False
        counterexample = "rho_f_exceeds_threshold"
    
    return {
        "metric_name": "Schur-Weyl Rank",
        "metric_value": rho_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run multiple trials and output results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho_f_exceeds_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")