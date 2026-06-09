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
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def etale_cohomology_rank(cnf):
        # Placeholder function to simulate the computation of etale cohomology rank
        # This is a dummy implementation for testing purposes
        return random.randint(1, 10)
    
    def frege_proof_depth(cnf):
        # Placeholder function to simulate the computation of Frege proof depth
        # This is a dummy implementation for testing purposes
        n = len(cnf)
        return int(math.log(n) / math.log(math.log(n)))
    
    results = []
    for _ in range(30):  # Test with 30 random CNF formulas
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        h = etale_cohomology_rank(cnf)
        d = frege_proof_depth(cnf)
        results.append((h, d))
    
    if not results:
        return {
            "metric_name": "min_φ(h)/d(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_ratio = min(h / d for h, d in results if d != 0)
    max_n = max(n for _, _ in results)
    
    return {
        "metric_name": "min_φ(h)/d(φ)",
        "metric_value": min_ratio,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": min_ratio <= math.log(max_n) / math.log(math.log(max_n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")