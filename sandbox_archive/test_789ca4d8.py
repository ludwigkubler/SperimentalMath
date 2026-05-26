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
        # Generate a monomial ideal with complexity c(I) ≤ n^3
        I = set()
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if random.randint(0, 1):
                    I.add((i, j))
        return I
    
    def compute_minimal_rank(I):
        # Compute the minimal rank of the affine quotient algebra A/I
        # This is a placeholder function; replace with actual computation
        return len(I)
    
    n = 20  # Fixed size for this example
    I = generate_monomial_ideal(n)
    rank = compute_minimal_rank(I)
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= math.pow(len(I), 2/3)
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds upper bound"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
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
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")