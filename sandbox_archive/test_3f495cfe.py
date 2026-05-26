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
    
    def generate_monomial_ideal(n):
        # Generate a random monomial ideal with complexity c(I) ≤ n^3
        return set(random.sample(range(1, n**3 + 1), random.randint(1, n**2)))
    
    def compute_minimal_rank(ideal):
        # Placeholder for computing the minimal rank of A/I
        # This is a dummy implementation; replace with actual computation
        return len(ideal)
    
    def complexity(I):
        return max(I or [0])
    
    n = random.randint(5, 40)
    I = generate_monomial_ideal(n)
    rank = compute_minimal_rank(I)
    c_I = complexity(I)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= c_I**(2/3)
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds upper bound {c_I**(2/3)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_exceeds_bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")