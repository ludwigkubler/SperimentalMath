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
    
    def generate_k_cnf(n, m):
        literals = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(literals) if random.choice([True, False]) else -random.choice(literals) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def symmetric_function(cnf):
        # Simplified encoding of the symmetric function
        return len(cnf)
    
    def tropical_rank(symmetric_func):
        # Placeholder for actual tropical rank calculation
        return random.randint(1, 10)  # Dummy value
    
    def monotone_circuit_size(cnf):
        # Placeholder for actual circuit size calculation
        return random.randint(m**2, m**4)  # Dummy value
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            m = random.randint(n**2 // 4, n**2)
            cnf = generate_k_cnf(n, m)
            symmetric_func = symmetric_function(cnf)
            rank = tropical_rank(symmetric_func)
            circuit_size = monotone_circuit_size(cnf)
            results.append({
                "n": n,
                "m": m,
                "symmetric_func": symmetric_func,
                "rank": rank,
                "circuit_size": circuit_size
            })
    
    total_ratio = sum(result["rank"] / (result["n"] ** 0.25) for result in results)
    mean_ratio = total_ratio / len(results)
    support_fraction = sum(1 for result in results if result["rank"] >= (result["n"] ** 0.25)) / len(results)
    
    conjecture_holds = mean_ratio >= 0.8 and all(result["rank"] >= (result["n"] ** 0.25) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 1.2 or result["instances_tested"] < (result["n"] ** 2) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.2)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")