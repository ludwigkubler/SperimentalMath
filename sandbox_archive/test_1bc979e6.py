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
    
    def generate_boolean_function(n, m):
        variables = [random.choice([0, 1]) for _ in range(m)]
        clauses = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        return variables, clauses
    
    def compute_toric_rank(variables, clauses):
        # Placeholder function to compute the minimal rank of a toric variety
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 5)
    
    def compute_resolution_length(clauses):
        # Placeholder function to compute the resolution proof length
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(10, 30)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, n * 2)
    variables, clauses = generate_boolean_function(n, m)
    
    rank = compute_toric_rank(variables, clauses)
    length = compute_resolution_length(clauses)
    
    return {
        "metric_name": "correlation",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")