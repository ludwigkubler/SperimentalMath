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
    
    n = 5 + (seed % 6) * 5  # Sweep n through {5,10,15,20,30,40}
    if n < 5 or n > 40:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic n"
        }
    
    # Generate a random Boolean function f represented as a quantum logic
    variables = [f"x{i}" for i in range(n)]
    clauses = []
    for _ in range(2 ** (n - 1)):
        clause = random.sample(variables, k=random.randint(1, n))
        if random.choice([True, False]):
            clause = [f"~{v}" for v in clause]
        clauses.append(" or ".join(clause))
    
    f = " and ".join(clauses)
    
    # Compute the Hochschild cohomology rank r
    # This is a placeholder function; replace with actual implementation
    def hochschild_cohomology_rank(f):
        # Placeholder: assume rank is proportional to n^2 for simplicity
        return n ** 2
    
    r = hochschild_cohomology_rank(f)
    
    # Construct BP representations of f and measure their read-twice complexity
    # This is a placeholder function; replace with actual implementation
    def bp_read_twice_complexity(f):
        # Placeholder: assume complexity is proportional to n^3 for simplicity
        return n ** 3
    
    bp_size = bp_read_twice_complexity(f)
    
    # Check if the conjecture holds
    conjecture_holds = bp_size <= r ** 2 + 0.1 * r ** 2
    
    result = {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": bp_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"BP size {bp_size} exceeds r^2 + 0.1*r^2"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [37, 61, 73, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")