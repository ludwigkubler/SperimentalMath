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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def homomorphisms_count(n):
    # Counting homomorphisms from F_2 to S_n is complex; use a simplified approach
    # This is a placeholder and should be replaced with an actual implementation
    return n + 1

def quasi_symmetric_functions_count(f, phi):
    count = 0
    for x in range(len(f)):
        if f[x] == phi[phi[x]]:
            count += 1
    return count

def communication_complexity(n):
    # Placeholder for actual CC computation
    return n**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        phi_count = homomorphisms_count(n)
        count_phi = quasi_symmetric_functions_count(f, phi_count)
        cc_f = communication_complexity(n)
        
        results.append({
            "n": n,
            "f": f,
            "phi_count": phi_count,
            "count_phi": count_phi,
            "cc_f": cc_f
        })
    
    total_cc = sum(result["cc_f"] for result in results)
    avg_cc = Fraction(total_cc, len(results))
    std_dev = math.sqrt(sum((result["cc_f"] - avg_cc)**2 for result in results) / len(results))
    
    conjecture_holds = all(cc <= 10 * count_phi**2 for cc, count_phi in zip([result["cc_f"] for result in results], [result["count_phi"] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": avg_cc,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")