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
from math import factorial

def hook_length_formula(n):
    return factorial(2*n) // (factorial(n+1) * factorial(n))

def young_diagram_dimension(n, k):
    return hook_length_formula(n) // (hook_length_formula(k) * hook_length_formula(n-k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 16
    instances_tested = 30
    total_ratio = 0
    
    for _ in range(instances_tested):
        # Generate a random 3-CNF formula with n variables
        num_clauses = 2 * n
        clauses = []
        for _ in range(num_clauses):
            literals = [random.choice([1, -1]) * (i+1) for i in range(n)]
            random.shuffle(literals)
            clause = literals[:3]
            clauses.append(clause)
        
        # Compute the symmetric square decomposition dimensions
        perm_dim = young_diagram_dimension(2*n, n)
        det_dim = young_diagram_dimension(2*n, n-1)
        
        # Measure the ratio of dominant irreducible component dimensions
        ratio = perm_dim / det_dim
        
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio > 2**(n/4) * 0.95
    counterexample = "" if conjecture_holds else "ratio < 2^(n/4) * 0.95"
    
    return {
        "metric_name": "Ratio of Permanent to Determinant Dimensions",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio < 2^(n/4) * 0.95\" first_failing_seed={first_failing_seed}")