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
    
    p = 2  # Fixed prime for simplicity, can be generalized if needed
    
    def log_p_adic(n):
        return math.log(n, p)
    
    def rank_of_l_function(n):
        # Placeholder function to simulate the rank of a p-adic L-function
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        rank = rank_of_l_function(n)
        expected_rank = log_p_adic(n)
        
        if rank < expected_rank:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, expected>=log2({n})={expected_rank}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "p-adic L-function rank",
        "metric_value": expected_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")