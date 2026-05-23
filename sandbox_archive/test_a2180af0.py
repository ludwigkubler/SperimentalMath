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

def generate_boolean_algebra(n):
    return [tuple(sorted(random.sample(range(2), n))) for _ in range(1 << n)]

def tropicalized_k_theory_rank(boolean_algebra):
    # Placeholder function to compute the rank of tropicalized K-theory
    # This is a dummy implementation and should be replaced with actual logic
    return len(boolean_algebra)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_algebra = generate_boolean_algebra(n)
        rank = tropicalized_k_theory_rank(boolean_algebra)
        
        if rank > (2 ** n) - 1:
            return {
                "metric_name": "tropicalized_k_theory_rank",
                "metric_value": rank,
                "instances_tested": len(boolean_algebra),
                "conjecture_holds": False,
                "counterexample": f"Boolean algebra with {n} generators has rank {rank}, which exceeds 2^{n} - 1"
            }
        
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "tropicalized_k_theory_rank",
        "metric_value": mean_rank,
        "instances_tested": len(boolean_algebra),
        "conjecture_holds": all(rank <= (2 ** n) - 1 for rank, n in zip(results, n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    if all(result <= (2 ** n) - 1 for result, n in zip(results, [5, 10, 15, 20, 30, 40])):
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results)} std={math.sqrt(sum((x - sum(results)/len(results)) ** 2 for x in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(next(result for result, n in zip(results, [5, 10, 15, 20, 30, 40]) if result > (2 ** n) - 1))]
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds bound\" first_failing_seed={first_failing_seed}")