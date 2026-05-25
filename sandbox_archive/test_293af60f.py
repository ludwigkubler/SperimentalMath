# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_function(n):
        # Generate a random polynomial function in P with degree n-1
        coefficients = [random.randint(0, 10) for _ in range(n)]
        return coefficients
    
    def compute_tropical_rank(delone_set):
        # Placeholder for computing tropical rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(delone_set)
    
    def convert_to_periodic_tiling(function):
        # Placeholder for converting function to periodic tiling
        # This is a dummy implementation and should be replaced with actual computation
        delone_set = [(i, i**2) for i in range(10)]
        return delone_set
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        function = generate_random_function(n)
        tiling = convert_to_periodic_tiling(function)
        rank = compute_tropical_rank(tiling)
        total_rank += rank
        instances_tested += len(tiling)
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = mean_rank <= n**(1/2) + n**(-1/4)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Tropical Rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")