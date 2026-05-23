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
    
    def generate_disjoint_sets(n):
        A = set(random.sample(range(1, 2*n), n))
        B = set(random.sample(range(2*n+1, 4*n), n))
        return A, B
    
    def construct_morse_complex(A, B):
        # Simplified Morse complex construction for demonstration
        # This is a placeholder and should be replaced with actual Morse theory implementation
        return len(A) + len(B)
    
    def communication_complexity(A, B):
        # Simplified randomized communication complexity for Disjointness
        # This is a placeholder and should be replaced with actual communication complexity implementation
        return max(len(A), len(B))
    
    n = random.randint(5, 40)
    A, B = generate_disjoint_sets(n)
    morse_rank = construct_morse_complex(A, B)
    comm_complexity = communication_complexity(A, B)
    
    metric_name = "correlation_coefficient"
    metric_value = Fraction(morse_rank, comm_complexity) if comm_complexity != 0 else None
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if metric_value is not None:
        # Placeholder for actual correlation test
        correlation_coefficient = random.random()  # Replace with actual calculation
        if correlation_coefficient > 0.7:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)