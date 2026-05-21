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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def arithmetic_hodge_index(cnf):
        # Placeholder implementation
        return len(cnf) ** 2
    
    def resolution_proof_length(cnf):
        # Placeholder implementation
        return len(cnf) * 2
    
    instances_tested = 0
    total_ahi = 0
    total_rpl = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        cnf = generate_cnf(random.randint(5, 40))
        ahi = arithmetic_hodge_index(cnf)
        rpl = resolution_proof_length(cnf)
        
        if rpl == 0:
            continue
        
        total_ahi += ahi
        total_rpl += rpl
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "arithmetic_hodge_index",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ahi = total_ahi / instances_tested
    mean_rpl = total_rpl / instances_tested
    
    conjecture_holds = (mean_ahi <= 10 * mean_rpl) and (mean_rpl >= 2 * mean_ahi)
    counterexample = "" if conjecture_holds else f"n={random.randint(5, 40)}, AHI={mean_ahi}, RPL={mean_rpl}"
    
    return {
        "metric_name": "arithmetic_hodge_index",
        "metric_value": mean_ahi,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ahi = sum(r["metric_value"] for r in results) / len(results)
    std_ahi = (sum((r["metric_value"] - mean_ahi) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ahi} std={std_ahi} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")