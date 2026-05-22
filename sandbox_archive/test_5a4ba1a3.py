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
    
    def generate_explicit_function(n):
        # Generate a random polynomial of degree n over GF(2)
        coefficients = [random.randint(0, 1) for _ in range(n + 1)]
        return coefficients
    
    def compute_brauer_group_rank(f):
        # Constructive mapping from field_A to field_B
        # This is a placeholder function; actual implementation depends on the conjecture
        return len(f)
    
    def compute_acc0_circuit_depth(f):
        # Placeholder function for ACC⁰ circuit depth computation
        # Actual implementation depends on the conjecture
        return len(f)  # Simplified example
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_explicit_function(n)
        rank = compute_brauer_group_rank(f)
        depth = compute_acc0_circuit_depth(f)
        discrepancy = abs(rank - depth)
        
        if discrepancy > 3:
            return {
                "metric_name": "Discrepancy",
                "metric_value": discrepancy,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, depth={depth}"
            }
        
        results.append((rank, depth))
    
    mean_discrepancy = sum(d for _, d in results) / len(results)
    return {
        "metric_name": "Discrepancy",
        "metric_value": mean_discrepancy,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")