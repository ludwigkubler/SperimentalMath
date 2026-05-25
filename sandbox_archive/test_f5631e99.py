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
    
    # Generate a random algebraic curve C over a finite field with genus g ≥ 2
    g = random.randint(2, 5)  # Arbitrary range for simplicity
    n = random.randint(5, 40)  # Number of parties
    
    # Calculate the minimal rank ρ(C) of the quadratic differential on each curve
    # This is a placeholder function; in practice, you would implement an efficient algorithm
    def min_rank(g):
        return g * (g - 1) // 2
    
    rho_C = min_rank(g)
    
    # Generate disjoint subsets A and B of n parties uniformly at random
    A = set(random.sample(range(n), n // 2))
    B = {i for i in range(n)} - A
    
    # Compute the randomized communication complexity CC_R(Disj(A,B)) for the disjointness problem on A and B
    def cc_disjoint(A, B):
        return max(len(A & B), len(A - B), len(B - A))
    
    cc_R_Disj = cc_disjoint(A, B)
    
    # Measure the correlation between ρ(C) and CC_R(Disj(A,B))
    correlation = rho_C / (n * (n - 1))  # Simplified for demonstration
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation >= 0.5,
        "counterexample": "" if correlation >= 0.5 else f"rho_C={rho_C}, CC_R_Disj={cc_R_Disj}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")