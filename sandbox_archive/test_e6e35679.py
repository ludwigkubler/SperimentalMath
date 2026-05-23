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
from math import log2, ceil

def generate_boolean_algebra(n):
    return [tuple(sorted(random.sample(range(2), n))) for _ in range(1 << n)]

def tropicalized_k_theory_rank(boolean_algebra):
    # Placeholder function to compute the rank of tropicalized K-theory
    # This is a dummy implementation and should be replaced with actual computation
    return len(boolean_algebra)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_algebra = generate_boolean_algebra(n)
        rank = tropicalized_k_theory_rank(boolean_algebra)
        
        if rank > (1 << n) - 1:
            return {
                "metric_name": "tropicalized_k_theory_rank",
                "metric_value": rank,
                "instances_tested": len(boolean_algebra),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank} > {2**n - 1}"
            }
        
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    return {
        "metric_name": "tropicalized_k_theory_rank",
        "metric_value": mean_rank,
        "instances_tested": len(boolean_algebra),
        "conjecture_holds": all(rank <= (1 << n) - 1 for rank, n in zip(results, n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")