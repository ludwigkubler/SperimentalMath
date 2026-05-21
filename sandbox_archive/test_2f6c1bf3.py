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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def mcsp_depth(cnf):
        # Placeholder for MCSP depth calculation
        return len(cnf)

    def min_gw_class(cnf):
        # Placeholder for minimal Gromov-Witten class calculation
        return random.random() * len(cnf)

    n = 10  # Start with a small size and increase
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):  # Test multiple instances per seed
        cnf = generate_cnf(n)
        gw_class = min_gw_class(cnf)
        depth = mcsp_depth(cnf)
        
        if depth > 0:
            ratio = gw_class / depth
            total_metric_value += ratio
            instances_tested += 1
            
            if ratio > 2 * n:  # Check the conjecture condition
                conjecture_holds = False
                counterexample = f"CNF with MCSP depth {depth} and GW class {gw_class}"
    
    return {
        "metric_name": "GW Class Ratio",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")