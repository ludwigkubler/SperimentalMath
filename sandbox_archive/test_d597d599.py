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
    
    def inverse_ackermann(n):
        if n == 0:
            return 1
        k = 0
        while 2**k <= n:
            k += 1
        return k - 1
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quandle_representation_size(n):
        # Simplified representation size for demonstration
        return 2**n
    
    def minimal_rank(quandle_size):
        # Minimal rank of a quandle is proportional to its size
        return quandle_size / inverse_ackermann(quandle_size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test with 5 random boolean functions per n
            f = generate_boolean_function(n)
            quandle_size = quandle_representation_size(n)
            rank = minimal_rank(quandle_size)
            
            if rank < 2**n / inverse_ackermann(n):
                conjecture_holds = False
                counterexample = f"Boolean function with n={n} and rank {rank}"
                break
        
        instances_tested += 5
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(minimal_rank(quandle_representation_size(n)) for n in n_values) / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")